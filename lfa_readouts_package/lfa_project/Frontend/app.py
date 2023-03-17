from flask import Flask, render_template, url_for, request, redirect, Response
import cv2 as cv
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
    client = GuiClient(frame)
    frame = client.findRoi()
    return redirect('/')


@app.route('/run_algorithm') 
def run_algorithm():
    global isVideo, frame, client
    isVideo = True
    try:
        client.runTheAlgorithmToFindTheContoursAndThenTheColorAndThenTheResult(frame)
        return redirect('/')
    except Exception as e:
        print(e)
        return redirect(url_for('error', errorMessage=e))
    


@app.route('/error/<errorMessage>')
def error(errorMessage):
    
    return  render_template('error-page.html', errorMessage=errorMessage)

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
    app.run(debug=True)