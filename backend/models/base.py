from backend.models.users import User
from backend.models.dishes import Dish
from backend.models.windows import Window
from datetime import datetime

class Base:
    db=None
    app=None
    def __init__(self, app, db):
        self.db = db
        self.app = app

    def session_commit(self, func_name, *args):
        try:
            self.db.session.commit()
            return True
        except Exception as e:
            self.db.session.rollback()
            self.__log_err(e, func_name, args)
            return False
        
    def __log_err(self, e, func_name, args):
        content = '{} : Error in function {} with args {}:\n'.format(datetime.now(), func_name, args)
        with open('err.log', 'a') as f:
            f.write(content)
            f.write(str(e))
            f.write('\n')

    def get_canteens(self):
        with self.app.app_context():
            return self.db.session.query(self.db.distinct(Window.canteen_id)).all()
    
    def get_windows(self, canteen_id):
        with self.app.app_context():
            return self.db.session.query(Window).fliter(Window.canteen_id==canteen_id).all()
    
    def get_dishes(self, window_id):
        with self.app.app_context():
            return self.db.session.query(Dish).fliter(Dish.window_id==window_id).all()

    def get_dish(self, dish_id):
        with self.app.app_context():
            return Dish.query.filter_by(id=dish_id).first()