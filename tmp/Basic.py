import os
import uuid
import requests
from flask import Flask, request, json, jsonify
from keras.models import load_model

from method import Model

model = Model({{shape}} , 224 ,0.0001 ,'../Models/{{ fileName }}.h5')

app = Flask(__name__)
UPLOAD_FOLDER = '../imgs'
redirectPorts ={}
redirectPorts = json.load(open('ip.json'))

data = {}
data = json.load((open('../Labels/{{ fileName }}.json')))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['img']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        path = os.path.join(UPLOAD_FOLDER, f_name)
        file.save(path)
        resultFromModel = model.simulation(path)

        basicDeasese = []
        secondDeasese = []
        print(resultFromModel)

        for i in range(len(resultFromModel)):
            basicDeasese.append(int(resultFromModel[i]))

        resultDict = {}
        for result in basicDeasese:
            resultDict[data[str(result)]] = []
            try:
                port = result + 5001
                levelTwoRequest = requests.post(f'http://{redirectPorts[str(result)]}:{port}', data={'imgPath': path})
                resultDict[data[str(result)]] = levelTwoRequest.json()['data']
            except:
                pass
        os.remove(path)
        resultDictTmp = []
        #category:"cat-name",predection:[d1,d2]
        for  i in resultDict :
            resultDictTmp.append({'category':i, 'predection' : resultDict[i] })
        return jsonify({'status': 'success', 'Data': resultDictTmp})
    else:
        return jsonify(status='fail', data=[])


if __name__ == '__main__':
    app.run(host='{{ip}}' , port={{port}} , debug =True )