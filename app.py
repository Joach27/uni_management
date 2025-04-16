from config import app
from flask_migrate import Migrate
from routes import *  # Importation des routes définies dans routes.py
from models import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from note_examen_bp import examen_bp  # le blueprint défini plus haut

app.register_blueprint(examen_bp)


bcrypt = Bcrypt()
jwt = JWTManager()

# Initialiser Migrate
migrate = Migrate(app, db)

bcrypt.init_app(app)
jwt.init_app(app)

# Créer les tables avec db.create_all()
with app.app_context(): 
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
