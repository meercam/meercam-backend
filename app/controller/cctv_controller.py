from flask import Blueprint
bp = Blueprint('cctv', __name__)

@bp.route('/', methods=['GET'])
def get_all_cctv():
    return "get all cctv"

@bp.route('/<id>', methods=['GET'])
def get_cctv(id):
    return f"get cctv {id}"

@bp.route('/', methods=['POST'])
def add_cctv():
    return f"post cctv"

@bp.route('/<id>', methods=['PUT'])
def modify_cctv(id):
    return f"put cctv {id}"

@bp.route('/<id>', methods=['DELETE'])
def delete_cctv(id):
    return f"delete cctv {id}"