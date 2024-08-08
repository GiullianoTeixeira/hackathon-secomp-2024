from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import base64
import os
import tempfile
import json
import os
import requests


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def chatGPT_response_PT(json_data):
    key = os.environ["api_key"]

    client = OpenAI(api_key=key)
    prompt_images = {}

    for key in json_data["image_urls"].items():
        prompt_images[key] = encode_image(key[1])


    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Você é um especialista em máquinas que está montando a ficha técnica delas, baseado em fotos (no máximo 3 fotos) de cada uma."
                "Retorne, um arquivo em formato .json, as informações que conseguir obter a partir das informações e foto(s) enviadas pelo usuário." 
                "Cada informação que você conseguir obter, escreva apenas ela em cada campo e mais nada (por exemplo, se identificar o modelo da máquina, escreva no .json algo"
                "como 'model: #nome_do_modelo#'). Agora que está especificado como o modelo deve ser, escreva o .json nessa ordem e com os seguintes nomes para os id's:"
                "'name' (o nome da máquina, que deve ser escrito pelo usuário em formato de texto), 'type' (que tipo a máquina é; também se espera que o usuário dê essa informação)," 
                "'manufacturer' (qual é o fabricante da máquina, que deve ser identificado em alguma imagem), 'model' (qual o modelo da máquina, também identificado nas imagens)," 
                "'identification' (qual o número de identificação da máquina, identificado nas imagens), 'location' (onde foi fabricado), 'technical_info' (um objeto JSON que"
                "possuirá chaves em que cada uma delas é uma informação mais técnica e um valor associado a ela. Por exemplo, caso o tipo de máquina seja motor, o 'technical_info'"
                "irá armazenar algo como #'power': #potencia_do_motor#, 'frequency': #frequencia_do_motor#, (...)#. Em qualquer um desses campos, caso não tenha sido possível obter"
                "alguma informação ou identificar que o usuário não inseriu alguma informação (ou seja, o campo de nome ou tipo de máquina estão vazios, ou não colocou nenhuma imagem)," 
                "preencha-os com uma String contendo um único hífen (-), e no caso do campo 'technical_info' apenas faça isso quando não foi possível achar nenhuma especificação técnica" 
                "baseada nas imagens (ou seja, apenas se o objeto JSON estiver vazio). Caso o usuário não preencher no mínimo o nome, o tipo e uma foto da máquina," 
                "descarte o .json e não escreva nada."},
        {"role": "user", "content": [
            {"type": "text", "text": "teste, testando, filler..."},
            {"type": "image_url", "image_url": {
                "url": f"data:image/jpeg;base64,{prompt_images["image1"]}"
            }},
            {"type": "image_url", "image_url": {
                "url": f"data:image/jpeg;base64,{prompt_images["image2"]}"
            }},
            {"type": "image_url", "image_url": {
                "url": f"data:image/jpeg;base64,{prompt_images["image3"]}"
            }}
        ]}
    ]
    )
    print(completion.choices[0].message.content)

    return completion.choices[0].message.content


def chatGPT_response_EN(json_data):
    key = os.environ["api_key"]

    client = OpenAI(api_key=key)

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Você é um especialista em máquinas que está montando a ficha técnica delas, baseado em fotos (no máximo 3 fotos) de cada uma."
                "Retorne, um arquivo em formato .json, as informações que conseguir obter a partir das informações e foto(s) enviadas pelo usuário." 
                "Cada informação que você conseguir obter, escreva apenas ela em cada campo e mais nada (por exemplo, se identificar o modelo da máquina, escreva no .json algo"
                "como 'model: #nome_do_modelo#'). Agora que está especificado como o modelo deve ser, escreva o .json nessa ordem e com os seguintes nomes para os id's:"
                "'name' (o nome da máquina, que deve ser escrito pelo usuário em formato de texto), 'type' (que tipo a máquina é; também se espera que o usuário dê essa informação)," 
                "'manufacturer' (qual é o fabricante da máquina, que deve ser identificado em alguma imagem), 'model' (qual o modelo da máquina, também identificado nas imagens)," 
                "'identification' (qual o número de identificação da máquina, identificado nas imagens), 'location' (onde foi fabricado), 'technical_info' (um objeto JSON que"
                "possuirá chaves em que cada uma delas é uma informação mais técnica e um valor associado a ela. Por exemplo, caso o tipo de máquina seja motor, o 'technical_info'"
                "irá armazenar algo como #'power': #potencia_do_motor#, 'frequency': #frequencia_do_motor#, (...)#. Em qualquer um desses campos, caso não tenha sido possível obter"
                "alguma informação ou identificar que o usuário não inseriu alguma informação (ou seja, o campo de nome ou tipo de máquina estão vazios, ou não colocou nenhuma imagem)," 
                "preencha-os com uma String contendo um único hífen (-), e no caso do campo 'technical_info' apenas faça isso quando não foi possível achar nenhuma especificação técnica" 
                "baseada nas imagens (ou seja, apenas se o objeto JSON estiver vazio). Caso o usuário não preencher no mínimo o nome, o tipo e uma foto da máquina," 
                "descarte o .json e não escreva nada. Responda INTEIRAMENTE em inglês."},
        {"role": "user", "content": [
            {"type": "text", "text": "teste, testando, filler..."},
            {"type": "image_url", "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }}
        ]}
    ]
    )
    print(completion.choices[0].message.content)



app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
           
@app.route('/index', methods=['GET'])
def index_html():
    return render_template('index.html')

@app.route('/insert_info_pt', methods=['GET'])
def info_pt():
    return render_template('insert_info_pt.html')

@app.route('/insert_info_en', methods=['GET'])
def info_en():
    return render_template('insert_info_en.html')

@app.route('/results_pt', methods=['GET'])
def results_pt():
    return render_template('results_pt.html')

@app.route('/results_en', methods=['GET'])
def results_en():
    return render_template('results_en.html')


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


@app.route('/inserir_info_pt', methods=['GET', 'POST'])
def info_pt_html():
    if request.method == 'POST':
        print("filler")
    return render_template('inserir_info_pt.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    form_data = {}
    image_urls = {}

    if request.method == 'POST':
        # Creating a temporary directory for this request
        temp_dir = tempfile.mkdtemp()

        # Handling text data
        form_data['machine_name'] = request.form.get('machineName')
        form_data['machine_type'] = request.form.get('machineType')

        # Handling image uploads
        for key in request.files:
            file = request.files[key]
            if file and allowed_file(file.filename):
                filename = file.filename
                filepath = os.path.join(temp_dir, filename)
                file.save(filepath)
                image_urls[key] = filename  # Storing image filenames

        json_data = {
            'form_data': form_data,
            'image_urls': image_urls
        }

        print(json_data)
        chatGPT_response_PT(json_data)
        
        with open('user_info.json', 'w') as json_file:
            json.dump(json_data, json_file)


        return jsonify(json_data)

    return render_template('index.html')

@app.route('/data_pt', methods=['GET'])
def get_data_pt(json_data):
    data = chatGPT_response_PT(json_data)
    return jsonify(data)


@app.route('/data_en', methods=['GET'])
def get_data_en(json_data):
    data = chatGPT_response_EN(json_data)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
