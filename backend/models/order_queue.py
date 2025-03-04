from backend.database import db
from datetime import datetime

class OrderQueue(db.Model):
    #点单队列
    __tablename__ = 'order_queue'
    __engine__ = 'InnoDB'
    __charset__ = 'utf8mb4'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(18), nullable=False)
    window_id = db.Column(db.Integer, nullable=False)
    order_time = db.Column(db.DateTime, default=datetime.now)
    order_content = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Integer, default=0) # 0 for waiting, 1 for processing, 2 for finished, delete if accomplished
    total_price = db.Column(db.Integer, default=0)


    def __init__(self, user_id, window_id, order_content, status=0, total_price=0) -> None:
        super().__init__()
        self.user_id = user_id
        self.window_id = window_id
        self.order_content = order_content
        self.status = status
        self.total_price = total_price
        #self.order_time = datetime.now()

    def to_dict(self):
        # 将OrderQueue实例转换为字典
        return {
            "id": self.id,
            "user_id": self.user_id,
            "order_content": self.order_content,
            "status": self.status,
            "order_time": self.order_time.strftime('%Y-%m-%dT%H:%M:%SZ'),  # 假设ordertime是datetime对象
            "total_price": self.total_price
        }