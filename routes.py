from flask import Blueprint, json, jsonify, request
# from ai import VectorDB

blueprint = Blueprint('routes', __name__)


@blueprint.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'Hello, World!'})


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
