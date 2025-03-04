from backend.models.base import Base
from backend.models.users import User
from backend.models.dishes import Dish
from backend.models.windows import Window
from backend.models.orders import Order
from backend.models.order_queue import OrderQueue
from backend.app import app
from backend.database import db


class Manager(Base):
    def __init__(self, app, db):
        super().__init__(app, db)

    def add_user(self, id, name, password, group=0):
        with self.app.app_context():
            user = User(id, name, password, group)
            self.db.session.add(user)
            return self.session_commit('add_user', id, name, password, group)

    def add_dish(self, name, price, window_id):
        with self.app.app_context():
            self.db.session.add(Dish(name, price, window_id))
            return self.session_commit('add_dish', name, price, window_id)

    def add_window(self, name, canteen_id, floor):
        with self.app.app_context():
            self.db.session.add(Window(name, canteen_id, floor))
            return self.session_commit('add_window', name, canteen_id, floor)

    def del_user(self, id):
        with self.app.app_context():
            user = self.db.session.query(User).filter_by(id=id).first()
            self.db.session.delete(user)
            return self.session_commit('del_user', id)

    def del_dish(self, id):
        with self.app.app_context():
            dish = self.db.session.query(Dish).filter_by(id=id).first()
            self.db.session.delete(dish)
            return self.session_commit('del_dish', id)

    def del_window(self, id):
        with self.app.app_context():
            window = self.db.session.query(Window).filter_by(id=id).first()
            self.db.session.delete(window)
            return self.session_commit('del_window', id)

    def update_dish(self, id, dish_name, price, window_id):
        with self.app.app_context():
            dish = self.db.session.query(Dish).filter_by(id=id).first()
            dish.dish_name = dish_name
            dish.price = price
            dish.window_id = window_id
            return self.session_commit('update_dish', id, dish_name, price, window_id)

    def get_order_queue(self, window_id):
        #获取窗口的订单队列
        with self.app.app_context():
            return OrderQueue.query.filter_by(window_id=window_id).all()

    def start_make_order(self, order_id):
        # 开始制作订单
        with self.app.app_context():
            order = self.db.session.query(OrderQueue).filter_by(id=order_id).first()
            order.status = 1
            return self.session_commit('start_make_order', order_id)

    def start_order(self, order_id):
        with self.app.app_context():
            order = self.db.session.query(Order).filter_by(id=order_id).first()
            order.status = 1
            return self.session_commit('start_order', order_id)

    def complete_order(self, order_id):
        # 订单制作完成
        with self.app.app_context():
            order = self.db.session.query(OrderQueue).filter_by(id=order_id).first()
            order.status = 2
            return self.session_commit('complete_order', order_id)

    def accomplish_order(self, order_id):
        # 订单完成
        with self.app.app_context():
            order = self.db.session.query(OrderQueue).filter_by(id=order_id).first()
            history_order = Order(order.user_id, order.order_content, order.order_time, order.window_id, 0, order.total_price)
            self.db.session.add(history_order)
            self.db.session.delete(order)
            return self.session_commit('accomplish_order', order_id)



manager = Manager(app, db)