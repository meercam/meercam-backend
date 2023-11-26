
from flask import jsonify , abort
from entity.cctv_entity import CCTVEntity
from os import path

cur_dir = path.dirname(__file__)

repository = [
    CCTVEntity(101, '공원1', 'file','/person.avi', None, None, None),
    CCTVEntity(102, '공원2', 'file', '/pose.avi', None, None, None),
]
next_id = 0

def next_id():
    global next_id
    next_id += 1
    return next_id

def find_all():
    return repository

def find_by_id(id):
    print("asdf")
    cctv = list(filter(lambda cctv: str(cctv.id) == id, repository))

    if len(cctv) == 0:
        abort(400)

    cctv = cctv[0]
    return cctv

def add_cctv(cctv):
    repository.append(cctv)
    return cctv