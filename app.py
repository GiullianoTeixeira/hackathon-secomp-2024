from flask import Flask, request, render_template, redirect, url_for
from openai import OpenAI
import tempfile
import os
import shutil
import base64
import requests


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def prompt_image(base64_image):
    if base64_image:
        return {"type": "image_url", "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
            }}
    else:
        return


image_path = "5bbda606-920f-420a-b840-fd1646aee957.jpg"

base64_image = encode_image(image_path)

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

client = OpenAI()

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
            "alguma informação, preencha-os com uma String contendo um único hífen (-), e no caso do campo 'technical_info' apenas faça isso quando não foi possível achar"
            "nenhuma especificação técnica baseada nas imagens (ou seja, apenas se o objeto JSON estiver vazio). Caso o usuário não preencher no mínimo o nome, o tipo e uma"
            "foto da máquina, descarte o .json e não escreva nada."},
    {"role": "user", "content": [
        {"type": "text", "text": "teste, testando, filler..."},
        prompt_image(base64_image)
    ]}
  ]
)

print(completion.choices[0].message.content)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Create a temporary directory for this request
            temp_dir = tempfile.mkdtemp()
            filename = file.filename
            filepath = os.path.join(temp_dir, filename)
            file.save(filepath)
            
            # Pass the temp_dir and filename to the template
            return redirect(url_for('index', filename=filename, temp_dir=temp_dir))
        else:
            return redirect(request.url)
    
    filename = request.args.get('filename')
    temp_dir = request.args.get('temp_dir')
    
    # Render the template with the filename and temp_dir
    if filename and temp_dir:
        filepath = os.path.join(temp_dir, filename)
        if os.path.exists(filepath):
            # Clean up the temporary directory after use
            os.remove(filepath)
            shutil.rmtree(temp_dir)
        return render_template('index.html', filename=filename, temp_dir=temp_dir)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
