from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from backend.database import db
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()

app = Flask(__name__)

# MySQL所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名，读者用自己设置的
USERNAME = "root"
# 连接MySQL的密码，读者用自己的
PASSWORD = "123456"
# MySQL上创建的数据库名称
DATABASE = "mydb"

class Config:
    SECRET_KEY = 'secret key'
    Debug = True
    host = HOSTNAME
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

app.config.from_object(Config)

# # 在app.config中设置好连接数据库的信息，
# # 然后使用SQLAlchemy(app)创建一个db对象
# # SQLAlchemy会自动读取app.config中连接数据库的信息

db.init_app(app)

#测试连接数据库
# with app.app_context():
#     with db.engine.connect() as conn:
#         result = conn.execute(text("select 1"))
#         print(result.fetchone())


from backend.routes.manager import mgr
from backend.routes.common import comm
from backend.routes.customers import cus
app.register_blueprint(mgr, url_prefix="/mgr")
app.register_blueprint(comm, url_prefix="/comm")
app.register_blueprint(cus, url_prefix="/cus")




if __name__ == "__main__":
    scheduler.start()
    app.run(debug=True, host='127.0.0.1')