from backend.database import db


class Dish(db.Model):
    __tablename__ = 'dishes'
    __engine__ = 'InnoDB'
    __charset__ = 'utf8mb4'
    __table_args__ = {'mysql_auto_increment': '0'}  # 设置自增初始值
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    dish_name = db.Column(db.String(18), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    window_id = db.Column(db.Integer, nullable=False)

    def __init__(self, dish_name, price, window_id) -> None:
        super().__init__()
        self.dish_name = dish_name
        self.price = price
        self.window_id = window_id

    def to_dict(self):
        # 将OrderQueue实例转换为字典
        return {
            'id': self.id,
            'dish_name': self.dish_name,
            'price': self.price,
            'window_id': self.window_id
        }