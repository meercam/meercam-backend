from flask import Blueprint
bp = Blueprint('bot', __name__)

@bp.route('/', methods=['GET'])
def get_all_bots():
    return "get all bot"


@bp.route('/<id>', methods=['GET'])
def get_bot(id):
    return f"get bot {id}"


@bp.route('/', methods=['POST'])
def add_bot():
    return "add bot"

@bp.route('/<id>', methods=['PUT'])
def modify_bot():
    return f"modify bot {id}"

@bp.route('/<id>', methods=['DELETE'])
def delete_bot():
    return f"delete bot {id}"
