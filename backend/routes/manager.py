from flask import Flask, Blueprint, jsonify, request



mgr = Blueprint("mgr", __name__)

@mgr.route('/home/<int:w_id>')    # mgr首页
def mgr_home(w_id):
    return f"{w_id} success"

@mgr.route('/dishes/add', methods=['GET', 'POST'])  # 跳转页面前端自行完成，此处仅添加菜品
def mgr_add_dish():
    name = request.form.get("dish_name")
    price = request.form.get("price")
    w_id = request.form.get("window_id")
    from backend.models.manager import manager
    manager.add_dish(name, price, w_id)
    return "success"


@mgr.route('/dishes/delete', methods=['GET', 'POST']) #根据dish_id删除菜品
def mgr_delete_dish():
    dish_id = request.form.get("id")
    from backend.models.manager import manager
    manager.del_dish(dish_id)
    return "success"

@mgr.route('/list_all_dishes/<int:window_id>') #展示所有菜品
def mgr_list_all_dishes(window_id):
    from backend.models.common import dbcommon
    dish_order = dbcommon.get_dishes(window_id)
    dishes = [dish.to_dict() for dish in dish_order]
    return jsonify(dishes), 200

@mgr.route('/dishes/update', methods = ['GET', 'POST'])  #对应图中修改菜单页面
def mgr_update_dish():
    dish_id = request.form.get("id")
    dish_name = request.form.get("dish_name")
    price = request.form.get("price")
    window_id = request.form.get("window_id")
    from backend.models.manager import manager
    manager.update_dish(dish_id, dish_name, price, window_id)
    return "success"


@mgr.route('/orders/<int:w_id>',methods=['GET']) #点餐队列
def mgr_orders(w_id):
    from backend.models.manager import manager
    order_queue = manager.get_order_queue(w_id)
    orders=[order.to_dict() for order in order_queue]
    return jsonify(orders),200

@mgr.route('/window/add', methods = ['GET', 'POST'])
def mgr_add_window():
    data = request.get_json()
    name = data.get("name")
    canteen_id = data.get("canteen_id")
    floor = data.get("floor")
    from backend.models.manager import manager
    return str(manager.add_window(name, canteen_id, floor))



@mgr.route('/window/delete', methods = ['GET', 'POST'])
def mgr_del_window():
    id = request.get_json().get("id")
    from backend.models.manager import manager
    return str(manager.del_window(id))

@mgr.route('user/add', methods = ['GET', 'POST'])
def mgr_add_mgr():
    data = request.get_json()
    id = data.get("id")
    name = data.get("name")
    pw = data.get("pw")
    group = data.get("group")
    from backend.models.manager import manager
    return str(manager.add_user(id, name, pw, group))


@mgr.route('user/delete', methods = ['GET', 'POST'])
def mgr_delete_mgr():
    id = request.get_json().get("id")
    from backend.models.manager import manager
    return str(manager.del_user(id))

@mgr.route('order_queue/start', methods = ['GET', 'POST'])
def mgr_start_order():
    order_id = request.get_json().get("order_id")
    from backend.models.manager import manager
    return str(manager.start_order(order_id))


@mgr.route('order_queue/complete', methods = ['GET', 'POST'])
def mgr_finished_order():
    order_id = request.get_json().get("order_id")
    from backend.models.manager import manager
    return str(manager.complete_order(order_id))

@mgr.route('order_queue/finish', methods = ['GET', 'POST'])
def mgr_finish_order():
    order_id = request.get_json().get("order_id")
    from backend.models.manager import manager
    return str(manager.accomplish_order(order_id))