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
    f = open("parse.out", 'w')
    f.write(parse_html(data["html"]))
    f.close()
    return jsonify({'message': 'parse route!!!'})
