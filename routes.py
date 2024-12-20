from flask_cors import CORS
from db import db
from utils.parseHtml import parse_html
from flask import Blueprint, json, jsonify, request
from ai import VectorDB
from ai import Model
import uuid

blueprint = Blueprint('routes', __name__)
CORS(blueprint, origins=[
     "chrome-extension://ljdpmpahkhiplmmchgjekbcdbimidlnk"])


@blueprint.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'Hello, World!'})


@blueprint.route('/ingest', methods=['POST'])
def ingest_data():
    data = json.loads(request.data)
    d_b = db.DataBase()
    domain = data['domain']
    route = data['route']
    data = {
        "domain": data["domain"],
        "content": parse_html(data["content"]),
        "id": str(uuid.uuid4())
    }
    d__b = VectorDB()
    d__b.add(data)
    d_b.insert(domain, route)
    return jsonify({'message': 'Data ingested successfully'})


@blueprint.route('/search', methods=['POST'])
def get_data():
    data = json.loads(request.data)
    db = VectorDB()
    res = db.search(data['query'], data['domain'])
    return jsonify({"message": "Data retrieved successfully", "data": res})


@blueprint.route('/insert-route', methods=['POST'])
def insert_route():
    data = json.loads(request.data)
    d_b = db.DataBase()
    domain = data.get('domain')
    route = data.get('route')

    if not domain or not route:
        return jsonify({'error': 'Both domain and route are required'}), 400

    d_b.insert(domain, route)
    return jsonify({'message': 'Route inserted successfully'})


@blueprint.route('/fetch-route', methods=['POST'])
def fetch_routes():
    data = json.loads(request.data)
    d_b = db.DataBase()
    domain = data.get('domain')
    route = data.get('route')

    if not domain or not route:
        return jsonify({'error': 'Both domain and route are required'})

    res = d_b.check(domain, route)
    return jsonify({'message': 'Data retrieved successfully', 'data': res})


@blueprint.route('/chat', methods=['POST'])
def chat():
    data = json.loads(request.data)
    model = Model()
    res = model.rag(data['content'], data['domain'])
    return jsonify({"message": "Chat response retrieved successfully", "data": res})
