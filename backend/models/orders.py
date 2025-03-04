from backend.database import db
from datetime import datetime

class Order(db.Model): # 相比order_queue多了一个accomplished_time 完成时间
    #用户历史订单
    __tablename__ = 'order'
    __engine__ = 'InnoDB'
    __charset__ = 'utf8mb4'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(18), nullable=False)
    order_content=db.Column(db.String(128), nullable=False)
    order_time = db.Column(db.DateTime, nullable=False)
    accomplished_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Boolean, default=0)#0 for accomplished, 1 for deleted
    window_id = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, default=0)

    def __init__(self, user_id, order_content, order_time, window_id, status=0, total_price=0) -> None:
        super().__init__()
        self.user_id = user_id
        self.order_content = order_content
        self.order_time = order_time
        self.window_id = window_id
        self.status = status
        self.total_price = total_price

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'order_content': self.order_content,
            'order_time': self.order_time,
            'accomplished_time': self.accomplished_time,
            'status': self.status,
            'window_id': self.window_id,
            'total_price': self.total_price
        }