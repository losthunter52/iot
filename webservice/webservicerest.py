from flask import Flask, jsonify, make_response, request, abort
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# DADOS ---------------------------
leituras_esp8266 = []
leituras_arduino = []
#----------------------------------

# ESP8266 -------------------------

@app.route('/leituras-esp8266', methods=['GET'])
def obtem_leituras_esp8266():
    aux = []
    for x in range(5):
        aux.append(leituras_esp8266[-(x+1)])
    return jsonify({'esp8266': aux})

@app.route('/leituras-esp8266/data', methods=['POST'])
def obtem_leituras_esp8266_por_data():
    if not request.json or not 'data' in request.json:
        abort(400)
    data = request.json['data']
    resultado = [resultado for resultado in leituras_esp8266 if data == resultado['leitura_data']]
    aux = []
    for x in range(5):
        aux.append(resultado[-(x+1)])
    return jsonify({'esp8266': aux })

@app.route('/leituras-esp8266/<int:idLeitura>', methods=['GET'])
def detalhe_leitura_esp8266(idLeitura):
    resultado = [resultado for resultado in leituras_esp8266 if resultado['id'] == idLeitura]
    if len(resultado) == 0:
        abort(404)
    return jsonify({'leitura': resultado[0]})

@app.route('/leituras-esp8266/<int:idLeitura>', methods=['DELETE'])
def excluir_leitura_esp8266(idLeitura):
    resultado = [resultado for resultado in leituras_esp8266 if resultado['id'] == idLeitura]
    if len(resultado) == 0:
        abort(404)
    leituras_esp8266.remove(resultado[0])
    return jsonify({'resultado': True})

@app.route('/leituras-esp8266', methods=['POST'])
def criar_leitura_esp8266():
    if not request.json or not 'luminosidade' in request.json:
        abort(400)
    if len(leituras_esp8266) > 0:
        id = leituras_esp8266[-1]['id'] + 1
    else:
        id = 1
    data = datetime.datetime.now()
    data = str(data.date())
    leitura = {
        'id': id,
        'luminosidade': request.json['luminosidade'],
        'leitura_data' : data
    }
    leituras_esp8266.append(leitura)
    return jsonify({'leitura': leitura}), 201

@app.route('/leituras-esp8266/<int:idLeitura>', methods=['PUT'])
def atualizar_leitura_esp8266(idLeitura):
    resultado = [resultado for resultado in leituras_esp8266 if resultado['id'] == idLeitura]
    if len(resultado) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'luminosidade' in request.json and type(request.json['luminosidade']) != "<type 'unicode'>":
        abort(400)
    resultado[0]['luminosidade'] = request.json.get('luminosidade', resultado[0]['luminosidade'])
    resultado[0]['leitura_data'] = datetime.datetime.now()
    return jsonify({'leitura': resultado[0]})

#----------------------------------


# ARDUINO -------------------------

@app.route('/leituras-arduino', methods=['GET'])
def obtem_leituras_arduino():
    aux = []
    for x in range(5):
        aux.append(leituras_arduino[-(x+1)])
    return jsonify({'arduino': aux})

@app.route('/leituras-arduino/data', methods=['POST'])
def obtem_leituras_arduino_por_data():
    if not request.json or not 'data' in request.json:
        abort(400)
    data = request.json['data']
    resultado = [resultado for resultado in leituras_arduino if data == resultado['leitura_data']]
    aux = []
    for x in range(5):
        aux.append(resultado[-(x+1)])
    return jsonify({'arduino': aux })

@app.route('/leituras-arduino/<int:idLeitura>', methods=['GET'])
def detalhe_leitura_arduino(idLeitura):
    resultado = [resultado for resultado in leituras_arduino if resultado['id'] == idLeitura]
    if len(resultado) == 0:
        abort(404)
    return jsonify({'leitura': resultado[0]})

@app.route('/leituras-arduino/<int:idLeitura>', methods=['DELETE'])
def excluir_leitura_arduino(idLeitura):
    resultado = [resultado for resultado in leituras_arduino if resultado['id'] == idLeitura]
    if len(resultado) == 0:
        abort(404)
    leituras_arduino.remove(resultado[0])
    return jsonify({'resultado': True})

@app.route('/leituras-arduino', methods=['POST'])
def criar_leitura_arduino():
    if not request.json or not 'temperatura' in request.json:
        abort(400)
    if not request.json or not 'umidade' in request.json:
        abort(400)
    if len(leituras_arduino) > 0:
        id = leituras_arduino[-1]['id'] + 1
    else:
        id = 1
    data = datetime.datetime.now()
    data = str(data.date())
    leitura = {
        'id': id,
        'temperatura': request.json['temperatura'],
        'umidade' : request.json['umidade'],
        'leitura_data' : data
    }
    leituras_arduino.append(leitura)
    return jsonify({'leitura': leitura}), 201

@app.route('/leituras-arduino/<int:idLeitura>', methods=['PUT'])
def atualizar_leitura_arduino(idLeitura):
    resultado = [resultado for resultado in leituras_arduino if resultado['id'] == idLeitura]
    if len(resultado) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'temperatura' in request.json and type(request.json['temperatura']) != "<type 'unicode'>":
        abort(400)
    if 'umidade' in request.json and type(request.json['umidade']) != "<type 'unicode'>":
        abort(400)
    resultado[0]['temperatura'] = request.json.get('temperatura', resultado[0]['temperatura'])
    resultado[0]['umidade'] = request.json.get('umidade', resultado[0]['umidade'])
    resultado[0]['leitura_data'] = datetime.datetime.now()
    return jsonify({'leitura': resultado[0]})

#----------------------------------

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'erro': 'Recurso Nao encontrado'}), 404)


if __name__ == "__main__":
    print('Servidor executando...')
    app.run(debug=True)
