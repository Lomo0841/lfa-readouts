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

""" 
Title: Video Streaming in Web Browsers with OpenCV & Flask
Author: Nakul Lakhotia
Date: 20/10 2020
Located: 22/4 2023
URL: https://towardsdatascience.com/video-streaming-in-web-browsers-with-opencv-flask-93a38846fe00 
"""
def gen_frames():  
    global is_video, frame
    camera = cv.VideoCapture(0)

    while True:
        _, frame = camera.read()
        if is_video:
            #encode a frame from OpenCV as a PNG image and yields it as a byte string with a MIME message format.
            _, encoded_frame = cv.imencode('.png', frame)
            byteFrame = encoded_frame.tobytes()
            yield (b'--byteFrame\r\n'
                    b'Content-Type: image/png\r\n\r\n' + byteFrame + b'\r\n')
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

    #Special handling of writing to config file whether we should save results locally
    try:
        variable = request.form['should_print']
    except:
        variable = None
    config.write_to_config("Print", "print", "True") if variable else config.write_to_config("Print", "print", "False")
    

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
    print(roi_extractor)

    kernel_size = config.get_config_int("ContourDetection", "kernelSize")
    should_print = config.get_config_boolean("Print", "print")

    b64_frame = None
    if frame is not None and not isinstance(frame, str):
        _, encoded_frame = cv.imencode('.png', frame)
        b64_frame = base64.b64encode(encoded_frame).decode('utf-8')

    implementation_options = [
        {"step": "Roi Extractor", 
         "group": "RoiOptions",
         "checked": roi_extractor,
         "options": [
                     {"value": "AprilTagsExtractor", "name": "AprilTags"}]
        },
        {"step": "White Balancing", 
         "group": "WhiteOptions", 
         "checked": white_balancer,
         "options": [
                     {"value": "MaxRGB", "name": "Max RGB"}, 
                     {"value": "GreyWorld", "name": "Grey World"}, 
                     {"value": "None", "name": "None"}]
        },
        {"step": "Contour Detector", 
         "group": "DetectorOptions", 
         "checked": contour_detector,
         "options": [
                     {"value": "BlurThresholdContourDetector", "name": "Gaussian Blur"}, 
                     {"value": "AltContourDetector", "name": "Median Blur"}]
        },
        {"step": "Contour Filtrator", 
         "group": "FiltratorOptions", 
         "checked": contour_filtrator,
         "options": [
                     {"value": "FilterOnConditions", "name": "Use Conditions"}]
        },
        {"step": "Contour Selector", 
         "group": "SelectorOptions", 
         "checked": contour_selector,
         "options": [
                     {"value": "HierarchicalSelector", "name": "Hierarchical"}]
        }
    ]

    settings_variables = {'x': x, 'y': y, 'maxDist': max_dist, 'minArea': min_area,
           'maxDefect': max_defect, 'kernelSize': kernel_size, 'should_print': should_print}
    
    return render_template('main-page.html', input_image=b64_frame, is_video=is_video, implementations = implementation_options, settings_variables=settings_variables)


if __name__ == "__main__":
    app.run(debug=True)