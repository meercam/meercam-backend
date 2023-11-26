from flask import Blueprint, request, jsonify, abort
from repository.cctv_repository import find_all, find_by_id, next_id
bp = Blueprint('cctv', __name__)
from entity.cctv_entity import CCTVEntity
@bp.route('/', methods=['GET'])
def get_all_cctv():
    print("안찍혀")
    return jsonify([data.__dict__ for data in find_all()])

@bp.route('/<id>', methods=['GET'])
def get_cctv(id):
    return jsonify(find_by_id(id).__dict__)

@bp.route('/<id>/stream_url', methods=['GET'])
def get_stream_url(id):
    cctv = find_by_id(id)
    if cctv is None: abort(404)
    return jsonify(cctv.get_connection_string())

@bp.route('/', methods=['POST'])
def add_cctv():
    json_data = request.json
    cctv = CCTVEntity(
        next_id(), 
        json_data['name'], 
        json_data['scheme'], 
        json_data['ip'], 
        json_data['port'], 
        json_data['username'], 
        json_data['password']
    )
    add_cctv(cctv)
    return "ok"

@bp.route('/<id>', methods=['PUT'])
def modify_cctv(id):
    json_data = request.json 
    cctv = CCTVEntity(
        id, 
        json_data['name'], 
        json_data['scheme'], 
        json_data['ip'], 
        json_data['port'], 
        json_data['username'], 
        json_data['password']
    )
    return jsonify(modify_cctv(id).__dict__)

@bp.route('/<id>', methods=['DELETE'])
def delete_cctv(id):
    return f"delete cctv {id}"