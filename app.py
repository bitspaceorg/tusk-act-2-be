from flask import Flask
from routes import blueprint
from flask_cors import CORS


app = Flask(__name__)


app.register_blueprint(blueprint)

cors = CORS(
    app, origins=["chrome-extension://ljdpmpahkhiplmmchgjekbcdbimidlnk"])


if __name__ == '__main__':
    app.run(debug=True, port=6969)
