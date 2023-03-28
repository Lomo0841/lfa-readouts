from flask import Flask, render_template, url_for, request, redirect, Response
import cv2 as cv
import numpy as np
import base64

from lfa_project.Utility.ConfigReader import ConfigReader
from lfa_project.Main.GuiClient import GuiClient

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
        client = GuiClient(frame)
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
        client = GuiClient(frame)
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
    
    section = "FiltrationVariables"

    x = request.form['center_x']
    y = request.form['center_y']
    max_dist = request.form['max_dist']
    min_area = request.form['min_area']
    max_defect = request.form['max_defect']
    
    config.write_to_config(section, "expectedCentrumX", x)
    config.write_to_config(section, "expectedCentrumY", y)
    config.write_to_config(section, "maxDistanceFromCentrum", max_dist)
    config.write_to_config(section, "minAreaOfContour", min_area)
    config.write_to_config(section, "maxDepthOfConvex", max_defect)

    return redirect('/')
   



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
    
    """ inputImage = cv.imread("lfa_readouts_package\lfa_project\Images\\" + "green.png")
    _, buffer = cv.imencode('.png', inputImage) """
    b64_frame = None
    if frame is not None and not isinstance(frame, str):
        _, encoded_frame = cv.imencode('.png', frame)
        #BAD ENCODING! Maybe use tobytes aswell?
        b64_frame = base64.b64encode(encoded_frame).decode('utf-8')
    
    
    return render_template('main-page.html', input_image=b64_frame, is_video=is_video, x=x, y=y, maxDist=max_dist, minArea=min_area, maxDefect=max_defect)


if __name__ == "__main__":
    host_ip = '10.209.173.87'
    app.run(debug=True)