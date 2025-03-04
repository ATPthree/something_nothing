from flask import Flask, Blueprint, jsonify, request


cus = Blueprint("cus", __name__)

@cus.route("/dish/get") # 根据食堂和楼层返回菜品
def get_dishes():
    data = request.get_json()
    window_id = data.get("window_id")
    from backend.models.common import dbcommon
    dish_order = dbcommon.get_dishes(window_id)
    dishes = [dish.to_dict() for dish in dish_order]
    return jsonify(dishes), 200

@cus.route('/account/get_history')
def get_history():
    data = request.get_json()
    user_id = data.get("id")
    from backend.models.customer import customer
    history_order = customer.get_history(user_id)
    history = [order.to_dict() for order in history_order]
    return jsonify(history), 200

@cus.route('/account/get_orders')
def get_orders():
    data = request.get_json()
    user_id = data.get("id")
    from backend.models.customer import customer
    order_order = customer.get_orders(user_id)
    orders = [order.to_dict() for order in order_order]
    return jsonify(orders), 200

@cus.route('/order/add', methods=['POST'])
def add_order():
    data = request.get_json()
    user_id = data.get("id")
    window_id = data.get("window_id")
    order_content = data.get("order_content")
    total_price = data.get("total_price")
    #print(user_id, window_id, order_content, total_price)
    from backend.models.customer import customer
    return str(customer.add_order(user_id, window_id, order_content, total_price))

@cus.route('/order/del', methods=['POST'])
def del_order():
    data = request.get_json()
    order_id = data.get("id")
    from backend.models.customer import customer
    res = customer.del_order(order_id)
    if res:
        return "success"
    return "fail"
