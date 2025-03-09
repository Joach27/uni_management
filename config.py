from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/universityDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = "f814916eac24771e9a1e3df7fe9cb32e"

app.config['JWT_SECRET_KEY'] = "f0e9bd4bb31e9715a899f754aaa679b414fade22aa44c8d17ed111e848985be8242625ae3fe5293d5db09b694d45d4e5b31255c585dc427e07624f35706e1010"

db = SQLAlchemy(app)