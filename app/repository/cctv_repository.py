
from flask import jsonify , abort
from entity.cctv_entity import CCTVEntity
from os import path

cur_dir = path.dirname(__file__)

repository = [
    CCTVEntity(101, '공원1', 'file', path.join(cur_dir, '..,', 'data', 'person.avi'), None, None, None),
    CCTVEntity(102, '공원2', 'file', path.join(cur_dir, '..', 'data', 'pose.avi'), None, None, None),
    CCTVEntity(103, '행사장1', 'file', path.join(cur_dir, '..', 'data', 'samplemp4'), None, None, None),
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

def modify_cctv(cctv):
    org = find_by_id(cctv.id)
    if org is None: abort(404)

    if cctv.name is not None:
        org.name = cctv.name    
    if cctv.scheme is not None:
        org.scheme = cctv.scheme
    if cctv.ip is not None:
        org.ip = cctv.ip
    if cctv.port is not None:
        org.port = cctv.port
    if cctv.username is not None:
        org.username = cctv.username
    if cctv.password is not None:
        org.password = cctv.password
    return org
