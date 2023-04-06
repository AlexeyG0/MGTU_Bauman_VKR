import flask
from flask import render_template, url_for


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

@app.route('/', methods = ['POST', 'GET'])

@app.route('/index', methods = ['POST', 'GET'])
def main():
    if flask.request.method == 'GET':
        return render_template('index.html')

    if flask.request.method == 'POST':

        var_request =  flask.request.form['var_value_1']
        # var_request = var_list_request[0]
        try:
            print('try', var_request)
            number = float(var_request)

            if str(number) == var_request:
                return render_template('index.html', result = 'Введено действительное число')
            if str(int(number)) == var_request:
                return render_template('index.html', result = 'Введено целое число')
            else:
                return render_template('index.html', result = 'Введено не число')

        except:
            return render_template('index.html', result = 'Введено не число')



@app.route('/user/<string:name>/<int:id>', methods = ['POST', 'GET'])
def user(name, id):
    return render_template('index.html', name = name, id = id)

if __name__ == '__main__':
    # with open('VisualStudio/lr_model.pkl', 'rb') as f:
    #     loaded_model = pickle.load(f)
    app.run()
