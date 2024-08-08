from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import base64
import os
import tempfile
import json
import os


def chatGPT_response_PT(json_data):
    key = os.environ["api_key"]

    client = OpenAI(api_key=key)

    print(len(json_data["image_urls"]))

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
                "url": f"data:image/jpeg;base64,{base64_image}"
            }}
        ]}
    ]
    )
    print(completion.choices[0].message.content)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


@app.route('/index', methods=['GET'])
def index_html():
    return render_template('index.html')


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
        # Create a temporary directory for this request
        temp_dir = tempfile.mkdtemp()

        # Handle text data
        form_data['nome_maquina'] = request.form.get('nomeMaquina')
        form_data['tipo_maquina'] = request.form.get('tipoMaquina')

        # Handle image uploads
        for key in request.files:
            file = request.files[key]
            if file and allowed_file(file.filename):
                filename = file.filename
                filepath = os.path.join(temp_dir, filename)
                file.save(filepath)
                image_urls[key] = filename  # Store image filenames

        json_data = {
            'form_data': form_data,
            'image_urls': image_urls
        }

        print(json_data)
        chatGPT_response_PT(json_data)
        
        with open('data.json', 'w') as json_file:
            json.dump(json_data, json_file)


        return jsonify(json_data)

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug = True)

