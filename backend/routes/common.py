from flask import Flask, Blueprint, request, url_for, redirect, session, jsonify, make_response
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired

comm = Blueprint('comm', __name__)

@comm.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()  # 解析JSON数据
    user_id = data.get('user_id')
    passwd = data.get('passwd')

    if not user_id or not passwd:
        return jsonify({'status': 'error', 'message': '用户ID或密码缺失'}), 400

    # 调用Common类中的login方法
    from backend.models.common import dbcommon
    login_status = dbcommon.login(user_id, passwd)
    if login_status == 0:
        return jsonify({'status': 'error', 'message': '用户不存在或学号、密码错误'}), 400
    elif login_status <= 9:
        user_info = {
            'user_id': user_id,
            'message': '欢迎管理员登录'
        }
        session["user_id"] = user_id
        resp = jsonify({'status': 'success', 'data': user_info})
        resp.set_cookie('user_id', user_id, max_age=3600)
        resp.status_code = 200
        return resp
    elif login_status >= 11:
        user_info = {
            'user_id': user_id,
            'message': '欢迎窗口工作者登录'
        }
        session["user_id"] = user_id
        resp = jsonify({'status': 'success', 'data': user_info})
        resp.set_cookie('user_id', user_id, max_age=3600)
        resp.status_code = 200
        return resp
    else:
        user_info = {
            'user_id': user_id,
            'message': '登录成功'
        }
        session["user_id"] = user_id
        rec = get_recom(user_id)
        resp = jsonify({'status': 'success', 'data': user_info, 'rec': rec})
        resp.set_cookie('user_id', user_id, max_age=3600)
        resp.status_code = 200
        return resp

@comm.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()  # 解析JSON数据
    user_id = data.get('user_id')
    name = data.get('name')
    passwd = data.get('passwd')
    print(user_id, name, passwd)
    if not user_id or not passwd:
        return jsonify({'status': 'error', 'message': '用户ID或密码缺失'}), 400
    from backend.models.common import dbcommon
    login_status = dbcommon.login(user_id, passwd)
    if login_status != 0:
        return jsonify({'status': 'error', 'message': '用户已存在'}), 400
    else:
        register_success = dbcommon.register(user_id, name, passwd)
        if register_success:
            return jsonify({'status': 'success', 'message': '注册成功'}), 200
        else:
            return jsonify({'status': 'error', 'message': '注册失败'}), 500



@comm.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()

@comm.route('/get_dish', methods=['GET', 'POST'])
def get_dish():
    data = request.get_json()
    dish_id = data.get('dish_id')
    from backend.models.common import dbcommon
    dish = dbcommon.get_dish(dish_id)
    return jsonify(dish.to_dict()), 200


def get_recom(user_id) -> list:
    from backend.recommender.recommender import rec
    lst = rec.recommend(user_id)
    return lst
