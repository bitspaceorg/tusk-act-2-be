from flask import Blueprint, jsonify, request
from flask_cors import CORS

from utils.parseHtml import parse_html

blueprint = Blueprint('routes', __name__)
CORS(blueprint, origins=[
     "chrome-extension://ljdpmpahkhiplmmchgjekbcdbimidlnk"])


@blueprint.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'Hello, World!'})


@blueprint.route('/parse', methods=['POST'])
def parseHtml():
    data = request.get_json()
    # os.system(f"echo {parse_html(data["html"])} > parse.out")
    return jsonify({'message': 'parse route!!!'})

# @blueprint.route('/ingest', methods=['POST'])
# def ingest_data(data):
#     data = json.loads(request.data)
#     db = VectorDB()
#     db.add(data)
#     return jsonify({'message': 'Data ingested successfully'})
#
#
# @blueprint.route('/search', methods=['POST'])
# def get_data():
#     data = json.loads(request.data)
#     db = VectorDB()
#     return jsonify({'data': db.search(data)})
