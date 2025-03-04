from backend.database import db


class Window(db.Model):
    __tablename__ = 'windows'
    __engine__ = 'InnoDB'
    __charset__ = 'utf8mb4'
    __table_args__ = {'mysql_auto_increment': '11'}  #设置自增初始值
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    window_name = db.Column(db.String(18), nullable=False)
    canteen_id=db.Column(db.Integer, nullable=False)
    floor=db.Column(db.Integer, nullable=False)

    def __init__(self, window_name, canteen_id, floor) -> None:
        super().__init__()
        self.window_name = window_name
        self.canteen_id = canteen_id
        self.floor = floor

