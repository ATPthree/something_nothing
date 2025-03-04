"""
该文件主要用于从数据库中加载数据集
每条记录需要获取：(user_id, order_content)
可以先转化为一个字典，key为user_id，value为order_cnt（list）,下标为商品id，值为点单次数
最终转化为一个矩阵，矩阵的行表示用户，列表示商品，矩阵中的值表示用户对商品的点单次数
"""
import numpy as np
from backend.models.orders import Order
from backend.models.dishes import Dish
from backend.models.base import Base

class Data_loader(Base):
    def __init__(self, app, db):
        super().__init__(app, db)
        self.data = None
        self.data_dir = None
        self.item_mean = None

    def load_data(self):
        with self.app.app_context():
            dish_num = self.db.session.query(Dish).count()
            users = self.db.session.query(Order.user_id).distinct().all()
        self.data_dir = {user[0]:[0.0]*dish_num for user in users}
        self.data = self.__load_data()
        self.data = np.array(self.data)
        return self.data, self.data_dir

    def __load_data(self):
        with self.app.app_context():
            orders = self.db.session.query(Order).all()
        for order in orders:
            user_id = order.user_id
            dish_ids = order.order_content.split()
            for dish_id in dish_ids:
                self.data_dir[user_id][int(dish_id)] += 1
        data = list(self.data_dir.values())
        return data

from backend.app import app
from backend.database import db
dl = Data_loader(app, db)