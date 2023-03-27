from flask import Flask, render_template, url_for, request, redirect, Response
import cv2 as cv
import numpy as np
import base64

from lfa_project.Utility.ConfigReader import ConfigReader
from lfa_project.Main.GuiClient import GuiClient

app = Flask(__name__)

config = ConfigReader()
client = None
isVideo = True
frame = None

#https://towardsdatascience.com/video-streaming-in-web-browsers-with-opencv-flask-93a38846fe00
def gen_frames():  
    global isVideo, frame
    camera = cv.VideoCapture(0)

    while True:
        _, frame = camera.read()  # read the camera frame
        if isVideo:
            
            _, encodedFrame = cv.imencode('.png', frame)
            byteFrame = encodedFrame.tobytes()
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
    global isVideo, frame, client
    isVideo = False
    try:
        client = GuiClient(frame)
        frame = client.findRoi()
        return redirect('/')
    except Exception as e:
        print(e)
        client = None
        return redirect(url_for('error', errorMessage=e))
    
@app.route('/load_image', methods=['POST']) 
def load_image():
    global isVideo, frame, client
    isVideo = False
    #file = request.files['file']
    encodedImage = request.files['file'].read()
    npImage = np.frombuffer(encodedImage, np.uint8)

    frame = cv.imdecode(npImage, cv.IMREAD_COLOR)
    try:
        client = GuiClient(frame)
        frame = client.findRoi()
        return redirect('/')
    except Exception as e:
        print(e)
        client = None
        return redirect(url_for('error', errorMessage=e))




@app.route('/run_algorithm') 
def run_algorithm():
    global isVideo, frame, client
    isVideo = True
    try:
        if client is None:
            raise Exception("No valid image to analyze. Try capturing or choosing a new image")
        result = client.runTheAlgorithmToFindTheContoursAndThenTheColorAndThenTheResult(frame)
        client = None
        cv.drawContours(frame, result[0], -1, (0, 255, 0), 3)

        return redirect(url_for('result', red=round(result[1][2],3), green=round(result[1][1],3), blue=round(result[1][0],3)))
    except Exception as e:
        print(e)
        client = None
        return redirect(url_for('error', errorMessage=e))
    

@app.route('/result/<red>/<green>/<blue>') 
def result(red,green,blue):
    global frame
    
    b64Frame = None
    if frame is not None and not isinstance(frame, str):
        _, encodedFrame = cv.imencode('.png', frame)
        #BAD ENCODING! Maybe use tobytes aswell?
        b64Frame = base64.b64encode(encodedFrame).decode('utf-8')
    return render_template('result-page.html', inputImage=b64Frame, red=red, green=green, blue=blue)
  

@app.route('/error/<errorMessage>')
def error(errorMessage):
    global isVideo
    isVideo = True
    return  render_template('error-page.html', errorMessage=errorMessage)

@app.route('/reset')
def reset():
    global isVideo
    isVideo = True
    return redirect('/')

@app.route('/post_data', methods=['POST'])
def post_data():
    
    section = "FiltrationVariables"

    x = request.form['center_x']
    y = request.form['center_y']
    maxDist = request.form['max_dist']
    minArea = request.form['min_area']
    maxDefect = request.form['max_defect']
    
    config.writeToConfig(section, "expectedCentrumX", x)
    config.writeToConfig(section, "expectedCentrumY", y)
    config.writeToConfig(section, "maxDistanceFromCentrum", maxDist)
    config.writeToConfig(section, "minAreaOfContour", minArea)
    config.writeToConfig(section, "maxDepthOfConvex", maxDefect)
    return redirect('/')
   



@app.route('/', methods=['POST', 'GET'])
def index():
    global frame, isVideo
    
    section = "FiltrationVariables"
    
    #Maybe one big wierd method for collecting all data?
    x = config.getConfigInt(section, "expectedCentrumX")
    y = config.getConfigInt(section, "expectedCentrumY")
    maxDist = config.getConfigInt(section, "maxDistanceFromCentrum")
    minArea = config.getConfigInt(section, "minAreaOfContour")
    maxDefect = config.getConfigInt(section, "maxDepthOfConvex")
    
    """ inputImage = cv.imread("lfa_readouts_package\lfa_project\Images\\" + "green.png")
    _, buffer = cv.imencode('.png', inputImage) """
    b64Frame = None
    if frame is not None and not isinstance(frame, str):
        _, encodedFrame = cv.imencode('.png', frame)
        #BAD ENCODING! Maybe use tobytes aswell?
        b64Frame = base64.b64encode(encodedFrame).decode('utf-8')
    
    
    return render_template('main-page.html', inputImage=b64Frame, isVideo=isVideo, x=x, y=y, maxDist=maxDist, minArea=minArea, maxDefect=maxDefect)


if __name__ == "__main__":
    host_ip = '10.209.173.87'
    app.run(host=host_ip, port=5000, debug=True)