# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import json
import os

from flask import request, send_file, render_template, flash, redirect, url_for
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

# Flask constructor takes the name of

# current module (__name__) as argument.

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
# store a value
# Get a value
from flask import Flask
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Check Configuration section for more details
# app.config['./aci-hackathon/enc']



# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return redirect(url_for('download_file', name=filename))


@app.route('/')
def start():
    return "START APPLICATION"
@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploaderA', methods = ['POST'])
def upload_file_A():
    if request.method == 'POST':
        f = request.files['file']
        file_content = json.loads(encrypt_decrypt_file(f, is_encrypted=True))
        f = open("txt_a.txt", "w")
        f.write(str(file_content.get("num")))
        f.close()
        return "Successfully upload file"

@app.route('/uploaderB', methods = ['POST'])
def upload_file_B():
    if request.method == 'POST':
        f = request.files['file']
        file_content = json.loads(encrypt_decrypt_file(f, is_encrypted=True))
        f = open("txt_b.txt", "w")
        f.write(str(file_content.get("num")))
        f.close()
        return "Successfully upload file"
#
# @app.route('/insertA', methods=['POST'])
# def insert_a():
#     return insert("txt_a.txt")
#
#
# @app.route('/insertB', methods=['POST'])
# def insert_b():
#     return insert("txt_b.txt")
#
#
# def insert(file_name):
#     url='http://nesssi.cacr.caltech.edu/cgi-bin/getmulticonedb_release2.cgi/post'
#     files={'files': open('file.txt','rb')}
#     values={'upload_file' : 'file.txt' , 'DB':'photcat' , 'OUT':'csv' , 'SHORT':'short'}
#     r=request.post(url,files=files,data=values)
#
#     r = request.get_data()
#     request_j = request.get_json()
#     f = open(file_name, "w")
#     f.write(str(request_j.get("num")))
#     f.close()
#     app.logger.info(f'FILE {file_name}')
#     return file_name


@app.route('/get_result', methods=['GET'])
def get_sum():
    f = open("result.txt", "w")
    f.write(str(read_to_int("txt_a.txt") + read_to_int("txt_b.txt")))
    f.close()
    return send_file("result.txt", as_attachment=True)

def encrypt_decrypt_file(file_name, is_encrypted):
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url="https://hackathon2023vault.vault.azure.net/", credential=credential)
    key = key_client.get_key("testK")
    crypto_client = CryptographyClient(key, credential=credential)

    if is_encrypted:
        return crypto_client.decrypt(file_name.algorithm, file_name.ciphertext)
    else:
        f = open(file_name, "r")
        res = int(f.read())
        f.close()
        return crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, res)


def read_to_int(file_name):
    f = open(file_name, "r")
    res = int(f.read())
    f.close()
    return res

@app.route('/get_encrypted_result', methods=['GET'])
def get_encrypted_result():
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url="https://hackathon2023vault.vault.azure.net/", credential=credential)
    keys = key_client.list_properties_of_keys()

    for key in keys:
        # the list doesn't include values or versions of the keys
        f = open("key.txt", "a")
        f.write(key.name)
        f.close()
        return send_file("key.txt", as_attachment=True)

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='0.0.0.0', port=80)
