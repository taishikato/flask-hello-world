from flask import Flask, render_template
import json
from flask import Flask,request
import whisper
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = './'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/download", methods=['POST'])
def download():
  file = request.files['file']
  print(file)

  if file.filename != None:
    print(file.filename)
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    model = whisper.load_model("base")
    result = model.transcribe('./' + filename, verbose=True, language='en')
    print(result)
    os.remove('./' + filename)
    model.cpu()
    del model

    # requests.post("http://localhost:3000/api/save-transcriptions-test", data=json.dumps(result))

    return json.dumps(result)

  return 'hello'