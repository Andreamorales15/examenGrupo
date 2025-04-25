from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask import session, flash
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
app = Flask(__name__)  
app.config['SECRET_KEY'] = 'grupo'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'andreatumina1m@gmail.com' 
app.config['MAIL_PASSWORD'] = 'xqipwosetvldafjz'    
app.config['MAIL_DEFAULT_SENDER'] = 'andreatumina1m@gmail.com'

mail = Mail(app)


CORS(app)
app.config["UPLOAD_FOLDER"] = "./static/img"

app.config["MONGODB_SETTINGS"] = [{
    "db": "ActividaddExamen",
    "host": os.getenv("MONGO_URI"),
    "port": 27017
}]

db = MongoEngine(app)


from routers.sena import *
from routers.instrutor import * 
from routers.login import * 
from routers.guias import * 
from routers.programas import * 


if __name__ == "__main__":
    app.run(port=6510, host="0.0.0.0", debug=True)
