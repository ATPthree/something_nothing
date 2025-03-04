from sqlalchemy.exc import SQLAlchemyError

from backend.models.base import Base
from backend.models.orders import Order
from backend.models.order_queue import OrderQueue
from backend.app import app
from backend.database import db

class Customer(Base):
    def __init__(self, app, db):
        super().__init__(app, db)

    def get_history(self, user_id):
        #查询用户的历史订单
        with self.app.app_context():
            return self.db.session.query(Order).filter(Order.user_id==user_id).all()

    def get_orders(self, user_id):
        #查询用户的点单队列
        with self.app.app_context():
            return self.db.session.query(OrderQueue).filter(OrderQueue.user_id==user_id).all()

    def add_order(self, user_id, window_id, order_content, total_price):
        #插入点单队列，成功返回id，失败返回None
        with self.app.app_context():
            order=OrderQueue(user_id,window_id,order_content, total_price)
            self.db.session.add(order)
            if self.session_commit("add_order"):
                self.db.session.refresh(order)
                return order.id
            else:
                return None
            # try:
            #     self.db.session.commit()
            #     self.db.session.refresh(order)
            #     return order.id
            # except SQLAlchemyError as e:
            #     self.db.session.rollback()
            #     return None

    def del_order(self, order_id):
        #查询订单状态，如果为0则删除并返回True，否则返回False，如果没找到订单表示制作完成，返回False
        with self.app.app_context():
            order = self.db.session.query(OrderQueue).filter(OrderQueue.id==order_id).first()
            if order is None:
                return False
            if order.status==0:
                Order.query.add(Order(order.user_id, order.order_content, order.order_time, order.window_id, 1, order.total_price))
                self.db.session.delete(order)
                return self.session_commit('del_order', order_id)
            else:
                return False


customer = Customer(app, db)