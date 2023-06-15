from flask import Flask, render_template , request , jsonify
from PIL import Image
import os , io , sys
import numpy as np 
import cv2
import base64
from yolo_detection_images import runModel

app = Flask(__name__)

############################################## THE REAL DEAL ###############################################
@app.route('/detectObject' , methods=['POST'])
def mask_image():
	# print(request.files , file=sys.stderr)
	tthresh = request.form.get('tthresh')
	nthresh = request.form.get('nthresh')
	print("ini nilai threshold ", tthresh)
	print("ini nilai nms threshold", nthresh)
	tthresh = float(tthresh)
	nthresh = float(nthresh)

	file = request.files['image'].read() ##0 byte file
	
	#thresh = int(thresh)
	# if thresh>0:
	# 	msg = "ada threshold"
	npimg = np.frombuffer(file, np.uint8)
	img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
	######### Do preprocessing here ################
	# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	################################################

	img = runModel(img,tthresh,nthresh)

	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

	img = Image.fromarray(img.astype('uint8'))
	rawBytes = io.BytesIO()
	img.save(rawBytes, 'JPEG')
	rawBytes.seek(0)
	img_base64 = base64.b64encode(rawBytes.read())
	return jsonify({'status':str(img_base64)})
######################################## THE REAL DEAL HAPPENS ABOVE ######################################

# def template(title = "HELLO!", text = ""):
#     templateDate = {
#         'text' : text,
#         'tvalues' : getTValues(),
#         'selected_tvalue' : -1
#     }
#     return templateDate

# def getTValues():
#     return (10, 11, 15, 2, 1)

@app.route('/test' , methods=['GET','POST'])
def test():
	print("log: got at test" , file=sys.stderr)
	return jsonify({'status':'succces'})

@app.route('/')
def home():
	return render_template(
		'./index.html',
		tValues=[{'value':0.1}, {'value':0.2}, {'value':0.3}, {'value':0.4}, {'value':0.5}],
		nValues=[{'value':0.01}, {'value':0.05}, {'value':0.1}, {'value':0.2}, {'value':0.2}, {'value':0.3}, {'value':0.4}, {'value':0.5}]
		)

	
@app.after_request
def after_request(response):
    print("log: setting cors" , file = sys.stderr)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)