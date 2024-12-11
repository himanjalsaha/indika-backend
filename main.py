from flask import Flask
from flask_cors import CORS
from config import Config
from db import mongo  
from routes.file_routes import file_routes

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)


mongo.init_app(app)




app.register_blueprint(file_routes)

if __name__ == "__main__":
    app.run(debug=True)
