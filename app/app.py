import flask
from flask import render_template, url_for
import keras
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler
import os
import pandas as pd

path = os.path.dirname(os.path.abspath(__file__))
app = flask.Flask(__name__, template_folder='templates')


columns = ["Соотношение матрица-наполнитель",
           "Плотность, кг/м3",
           "модуль упругости, ГПа",
           "Количество отвердителя, м.%",
           "Содержание эпоксидных групп,%_2",
           "Температура вспышки, С_2",
           "Поверхностная плотность, г/м2",
           "Модуль упругости при растяжении, ГПа",
           "Прочность при растяжении, МПа",
           "Потребление смолы, г/м2",
           "Угол нашивки, град",
           "Шаг нашивки",
           "Плотность нашивки"]


def get_input_value_block():
    out = ''
    for i, column in enumerate(columns):
        var_pol = 'var_pol_' + str(i)
        out +='<div class="input_box"><div class="input_text">' + column + '</div><div class="input_val"><input name="' + var_pol + '" type="number" step="0.001"></div></div>'
    return out

load_model = keras.models.load_model(path + '/model')

def model_predict(data):
    with open(path + '/minmax.pkl', 'rb') as minmax_f:
        minmax = pickle.load(minmax_f)
        dataf = minmax.transform(data)
        
        return load_model.predict(dataf[0, 1:].reshape(1,12))

#@app.route('/index', methods = ['POST', 'GET'])
# def main_1():
#     if flask.request.method == 'GET':
#         return render_template('index.html')

#     if flask.request.method == 'POST':

#         # var_request =  flask.request.form['var_value_1']
#         # var_request_1 =  flask.request.form['var_value_2']
#         var_request = 1
#         var_request_1 = 2
#         # var_request = var_list_request[0]
#         # try:
#         #     print('try', var_request)
#         #     number = float(var_request)

#         #     if str(number) == var_request:
#         #         return render_template('index.html', result = 'Введено действительное число')
#         #     if str(int(number)) == var_request:
#         #         return render_template('index.html', result = 'Введено целое число')
#         #     else:
#         #         return render_template('index.html', result = 'Введено не число')

#         # except:
#         #     return render_template('index.html', result = 'Введено не число')
#         return render_template('index.html', result = 'Введены числа:' + str(var_request) + ' ' + str(var_request_1))


@app.route('/', methods = ['POST', 'GET'])
@app.route('/index', methods = ['POST', 'GET'])
def pred():
    if flask.request.method == 'GET':
        return render_template('index.html')

    if flask.request.method == 'POST':

        var_list = [0]
        for i in range(1,13):
            val = flask.request.form['var_pol_' + str(i)]
            var_list.append(val)

        var_list = pd.DataFrame([var_list], columns=columns)
        print(var_list)
        predict = model_predict(var_list)

        return render_template('index.html', pred_result = predict)


@app.route('/user/<string:name>/<int:id>', methods = ['POST', 'GET'])
def user(name, id):
    return render_template('index.html', name = name, id = id)



if __name__ == '__main__':
    
    
    
    app.run()