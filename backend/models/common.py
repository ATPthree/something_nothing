from backend.models.base import Base
from backend.models.users import User
from backend.app import app
from backend.database import db


class Common(Base):
    def __init__(self, app, db):
        super().__init__(app, db)

    def is_exist(self, id):
        with self.app.app_context():
            user = self.db.session.query(User).filter(User.id == id).first()
            if user:
                return True
            return False

    def login(self, id, pw): #检测用户是否存在，以及其类型
        with self.app.app_context():
            user = self.db.session.query(User).filter(User.id == id).first()
        if user and user.password == pw:
            return user.group
        return 0


    def register2(self, id, name, pw ,group=1):
        try:
            user = User(id, name, pw, group)
            with self.app.app_context():
                 self.db.session.add(user)
                 self.db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()  #回滚操作
            print(f"注册失败: {e}")
            return False

    def register(self, id, name, pw, group=1):
        try:
            # 如果用户不存在，则创建新用户
            user = User(id, name, pw, group)

            with self.app.app_context():
                self.db.session.add(user)
                self.db.session.commit()  # 提交事务，插入新用户

            print(f"用户 {id} 注册成功")
            return True
        except Exception as e:
            self.db.session.rollback()  # 出现异常时回滚
            print(f"注册失败: {e}")
            return False


dbcommon = Common(app, db)
