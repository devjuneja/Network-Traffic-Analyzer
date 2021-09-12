from flask import Flask,send_file,render_template,render_template_string,url_for
from flask import request
from flask_cors import CORS, cross_origin
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from source import host_name_ip,begin
import json,os

# src = '192.168.1.50'
# dst = '192.168.1.1'

src,dst = begin()
hostnames, ips, device_type = host_name_ip(src, dst)

print("hostnames:",hostnames)
print("device_types:",device_type)

# hostnames = ['hbg-Switch1','hbg-Router1','hbg-Router2','unip-Router1','unip-Switch1']
# device_type = [4,3,3,3,1]

logs_folder = os.path.join('static','logs')
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['logs'] = logs_folder


@app.route('/')
def my_view():
    return render_template('index.html',len = len(hostnames),hostnames = hostnames)


@app.route('/network_device', methods=['GET'])
def cool_form():

    variable = request.args.get('variable')
    path = str(variable) + ".txt"
    with app.open_resource(os.path.join(app.config['logs'],path),mode="r") as f:
        con = f.readlines()

    data = []
    for i in con:
        if i != '\n':
            data.append(i[:-1])

    keys = [str(text) for text in data if "---" in text]

    original_keys = []

    for i in range(len(keys)):
        temp = keys[i].split("---")
        original_keys.append(temp[1])

    values = []
    temp = []
    i = 1
    while (i < len(data)):
        if data[i] not in keys and i != len(data) - 1:
            temp.append(data[i])

        else:
            values.append(temp)
            temp = []
        i += 1
    contents = dict(zip(original_keys, values))

    return render_template('test.html',contents = contents)


@app.route('/ImgControl')
def control():
    str = ""

    for i in device_type:
        if i==1:
            str = str + "image1 "
        elif i==2:
            str = str + "image2 "
        elif i==3:
            str = str + "image3 "
        elif i==4:
            str = str + "image4 "

    for i in hostnames:
        str += i

    return str


@app.route('/image1', methods=['GET'])
def image1():

    try:
        return send_file('static\img\Rg.png',
                         attachment_filename='Rg.png')
    except Exception as e:
        return str(e)

@app.route('/image2', methods=['GET'])
def image2():

    try:
        return send_file('static\img\Sg.png',
                         attachment_filename='Sg.png')
    except Exception as e:
        return str(e)

@app.route('/image3', methods=['GET'])
def image3():

    try:
        return send_file('static\img\Rr.png',
                         attachment_filename='Rr.png')
    except Exception as e:
        return str(e)

@app.route('/image4', methods=['GET'])
def image4():

    try:
        return send_file('static\img\Sr.png',
                         attachment_filename='Sr.png')
    except Exception as e:
        return str(e)

# if __name__ == '__main__':
#     app.run(debug=True)