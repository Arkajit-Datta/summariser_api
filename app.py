from flask import Flask, render_template, request, redirect, send_file,url_for,jsonify
import os
from custom_important_message import custom_important_message_recon
from text_file_clean_up import *
from summariser import *
from important_message import *
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

upload_path_txt = r"C:\Users\ARKAJIT DATTA\Desktop\machine learning\DSC_hackathon_summariser\txt_file_upload"

@app.route("/summarise/",methods = ["POST"])
@cross_origin()
def summary():
    if request.method == 'POST':
        txt_file = request.files['input_txt']
        txt_file_path = os.path.join(upload_path_txt,txt_file.filename)

        if txt_file.filename.rsplit(".",1)[1] == "txt":
            txt_file.save(txt_file_path)
        else:
            return False
        
        clean_text_file(txt_file_path)
        ret = summarise()
        
        return jsonify(ret)

@app.route("/important/",methods = ["POST"])
def important_message_1():
   if request.method == 'POST':
        txt_file = request.files['input_txt']
        txt_file_path = os.path.join(upload_path_txt,txt_file.filename)

        if txt_file.filename.rsplit(".",1)[1] == "txt":
            txt_file.save(txt_file_path)
        else:
            return False
        ret = important_message_recon(txt_file_path)
        
        return jsonify(ret)  

@app.route("/custom/",methods = ["POST"])
def important_message():
   if request.method == 'POST':
        string = request.form("string")
        txt_file = request.files['input_txt']
        txt_file_path = os.path.join(upload_path_txt,txt_file.filename)

        if txt_file.filename.rsplit(".",1)[1] == "txt":
            txt_file.save(txt_file_path)
        else:
            return False
        ret = custom_important_message_recon(string,txt_file_path)
        
        return jsonify(ret)  

if __name__ == "__main__":
    app.run(debug=False)