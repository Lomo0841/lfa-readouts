from flask import Flask, render_template, url_for, request, redirect, Response
import cv2 as cv
import numpy as np
import base64

from lfa_project.Utility.ConfigReader import ConfigReader
from lfa_project.Main.GuiClient import GuiClient
from lfa_project.Main.GuiWorkFlowClient import GuiWorkFlowClient

app = Flask(__name__)

config = ConfigReader()
client = None
is_video = True
frame = None

# https://towardsdatascience.com/video-streaming-in-web-browsers-with-opencv-flask-93a38846fe00
def gen_frames():  
    global is_video, frame
    camera = cv.VideoCapture(0)

    while True:
        _, frame = camera.read()  # read the camera frame
        if is_video:
            
            _, encoded_frame = cv.imencode('.png', frame)
            byteFrame = encoded_frame.tobytes()
            yield (b'--byteFrame\r\n'
                    b'Content-Type: image/png\r\n\r\n' + byteFrame + b'\r\n')  # iterate over all bytes and concatenate
        else:
            camera.release()
            print("camera released")
            break


@app.route('/live_image')
def live_image():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=byteFrame')


@app.route('/cap_image') 
def cap_image():
    global is_video, frame, client
    is_video = False
    try:
        client = GuiWorkFlowClient(frame)
        frame = client.find_roi()
        return redirect('/')
    except Exception as e:
        print(e)
        client = None
        return redirect(url_for('error', error_message=e))
    
@app.route('/load_image', methods=['POST']) 
def load_image():
    global is_video, frame, client
    is_video = False
    # file = request.files['file']
    encoded_image = request.files['file'].read()
    np_image = np.frombuffer(encoded_image, np.uint8)

    frame = cv.imdecode(np_image, cv.IMREAD_COLOR)
    try:
        client = GuiWorkFlowClient(frame)
        frame = client.find_roi()
        return redirect('/')
    except Exception as e:
        print(e)
        client = None
        return redirect(url_for('error', error_message=e))




@app.route('/run_algorithm') 
def run_algorithm():
    global is_video, frame, client
    is_video = True
    try:
        if client is None:
            raise Exception("No valid image to analyze. Try capturing or choosing a new image")
        result = client.run_algorithm_on_roi(frame)
        client = None
        cv.drawContours(frame, result[0], -1, (0, 255, 0), 3)

        return redirect(url_for('result', red=round(result[1][2], 3), green=round(result[1][1], 3), blue=round(result[1][0], 3)))
    except Exception as e:
        print(e)
        client = None
        return redirect(url_for('error', error_message=e))
    

@app.route('/result/<red>/<green>/<blue>') 
def result(red, green, blue):
    global frame
    
    b64_frame = None
    if frame is not None and not isinstance(frame, str):
        _, encoded_frame = cv.imencode('.png', frame)
        # BAD ENCODING! Maybe use tobytes as well?
        b64_frame = base64.b64encode(encoded_frame).decode('utf-8')
    return render_template('result-page.html', input_image=b64_frame, red=red, green=green, blue=blue)

@app.route('/error/<error_message>')
def error(error_message):
    global is_video
    is_video = True
    return  render_template('error-page.html', error_message=error_message)

@app.route('/reset')
def reset():
    global is_video
    is_video = True
    return redirect('/')

@app.route('/post_data', methods=['POST'])
def post_data():
    
    #Settings
    section = "FiltrationVariables"

    write_if_not_null(section, "expectedCentrumX", "center_x")
    write_if_not_null(section, "expectedCentrumY", "center_y")
    write_if_not_null(section, "maxDistanceFromCentrum", "max_dist")
    write_if_not_null(section, "minAreaOfContour", "min_area")
    write_if_not_null(section, "maxDepthOfConvex", "max_defect")

    #Advanced Settings
    section = "Implementations"
    
    write_if_not_null(section, "iRoiExtractor", "RoiOptions")
    write_if_not_null(section, "iWhiteBalancer", "WhiteOptions")
    write_if_not_null(section, "icontourdetector", "DetectorOptions")
    write_if_not_null(section, "icontourfiltrator", "FiltratorOptions")
    write_if_not_null(section, "iContourSelector", "SelectorOptions")

    write_if_not_null("ContourDetection", "kernelsize", "kernel_size")
    #write_if_not_null("Write", "write", "should_write")
    try:
        variable = request.form['should_write']
    except:
        variable = None
    #print("var is: " + str(variable))
    config.write_to_config("Write", "write", "True") if variable else config.write_to_config("Write", "write", "False")
    

    return redirect('/')

def write_if_not_null(section, name, options):
    try:
        variable = request.form[options]
    except:
        variable = None
    if variable:
        config.write_to_config(section, name, variable)


@app.route('/', methods=['POST', 'GET'])
def index():
    global frame, is_video
    
    section = "FiltrationVariables"
    #Maybe one big wierd method for collecting all data?
    x = config.get_config_int(section, "expectedCentrumX")
    y = config.get_config_int(section, "expectedCentrumY")
    max_dist = config.get_config_int(section, "maxDistanceFromCentrum")
    min_area = config.get_config_int(section, "minAreaOfContour")
    max_defect = config.get_config_int(section, "maxDepthOfConvex")

    section = "Implementations"
    roi_extractor = config.get_config_string(section, "iroiextractor")
    white_balancer = config.get_config_string(section, "iwhitebalancer")
    contour_detector = config.get_config_string(section, "icontourdetector")
    contour_filtrator = config.get_config_string(section, "icontourfiltrator")
    contour_selector = config.get_config_string(section, "icontourselector")


    kernel_size = config.get_config_int("ContourDetection", "kernelSize")
    should_write = config.get_config_boolean("Write", "write")

    
    """ inputImage = cv.imread("lfa_readouts_package\lfa_project\Images\\" + "green.png")
    _, buffer = cv.imencode('.png', inputImage) """
    b64_frame = None
    if frame is not None and not isinstance(frame, str):
        _, encoded_frame = cv.imencode('.png', frame)
        #BAD ENCODING! Maybe use tobytes aswell?
        b64_frame = base64.b64encode(encoded_frame).decode('utf-8')


    settings_variables = {'x': x, 'y': y, 'maxDist': max_dist, 'minArea': min_area,
           'maxDefect': max_defect, 'kernelSize': kernel_size, 'should_write': should_write, 'roi_extractor': roi_extractor,
           'white_balancer': white_balancer, 'contour_detector': contour_detector, 'contour_filtrator': contour_filtrator,
           'contour_selector': contour_selector}
    
    return render_template('main-page.html', input_image=b64_frame, is_video=is_video, settings_variables=settings_variables)

if __name__ == "__main__":
    host_ip = '10.209.173.87'
    app.run(debug=True)