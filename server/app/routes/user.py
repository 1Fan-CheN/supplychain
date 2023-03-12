from common.basersp import BaseRsp
from common.const import ReturnCode
from flask import Blueprint, request

users = Blueprint('user', __name__)

@users.route('/user/test', methods=['GET'])
def test():
    return BaseRsp.success_rsp('test success')

@users.route('/user/create', methods=['POST'])
def create():
    pass
    

@users.route('/user/login', methods=['POST'])
def login():
    return BaseRsp(ReturnCode.Success, 'login success').to_json()