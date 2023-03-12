from common.const import ReturnCode
from flask import jsonify


class BaseRsp(object):
    def __init__(self):
        pass

    @classmethod
    def success_rsp(cls, data=dict()):
        return jsonify({
            "code": ReturnCode.Success.value,
            "msg": ReturnCode.get_display_name(ReturnCode.Success.value),
            "data": data
        })

    @classmethod
    def err_rsp(cls, err_code, data=dict()):
        return jsonify({
            "code": err_code,
            "msg": ReturnCode.get_display_name(err_code),
            "data": data
        })

    @classmethod
    def rsp(cls, code, msg, data=dict()):
        return jsonify({
            "code": code,
            "msg": msg,
            "data": data
        })