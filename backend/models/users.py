from backend.database import db

class User(db.Model):
    __tablename__ = 'user'
    __engine__ = 'InnoDB'
    __charset__ = 'utf8mb4'
    id = db.Column(db.String(18), unique=True, primary_key=True)
    username = db.Column(db.String(18), nullable=False)
    password = db.Column(db.String(18), nullable=False)
    goal = db.Column(db.Integer, default=100) # credit
    #0 for superadmin, 1-9 of canteen,10 for user, >=11 for window_id
    group = db.Column(db.Integer, default=10)

    def __init__(self, id, name, pw, group) -> None:
        super().__init__()
        self.id = id
        self.username = name
        self.password = pw
        self.group = group