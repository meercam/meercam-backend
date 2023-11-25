
from flask import jsonify , abort
from entity.cctv_entity import CCTVEntity
import os 
repository = [
    CCTVEntity(101, '공원1', 'file', 0, None, None, None),
    CCTVEntity(102, '공원2', 'file', "C:\\Users\\0____\\projects\\cv-ex\\app\\data\\sample.mp4", 554, None, None),
    CCTVEntity(103, '행사장1', 'file', 'C:\\Users\\0____\\projects\\cv-ex\\app\\data\\datasets\\1.jpg', 554, None, None),
]
next_id = 0

def next_id():
    global next_id
    next_id += 1
    return next_id

def find_all():
    return repository

def find_by_id(id):
    print(type(id))
    print('hi')
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
