import os
from flask import Flask, redirect, url_for, request, abort
from flask_login import current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget
from wtforms import SelectMultipleField, SelectField

##################################################################################################################################################

# 初始化 Flask 应用
app = Flask(__name__)

# 初始化 Flask 应用配置
app.config['STATIC_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')    # 静态文件位置
# 必须设置默认数据库 URI（即使不使用）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///default.db'
# 数据库保存位置：./instance/<name>.db
app.config['SQLALCHEMY_BINDS'] = {
    'navigation': 'sqlite:///navigation.db',
    'service': 'sqlite:///service.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                           # 关闭追踪修改，避免警告
app.config['SECRET_KEY'] = 'R7D5MH8YJHCU2CD9'                                  # 会话安全密钥，必须设置

##################################################################################################################################################

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        """设置密码，自动哈希"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

class Navigation(db.Model):
    # 指定绑定到 'navigation' 数据库
    __bind_key__ = 'navigation'
    __tablename__ = 'navigation'

    # nullable=False - 该字段不允许为空
    # unique=True - 该字段的值在整个表中必须唯一，不能重复
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False, unique=True)
    group = db.Column(db.String(80), nullable=False)
    tags = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f'<Navigation {self.name}>'

class Service(db.Model):
    # 指定绑定到 'service' 数据库
    __bind_key__ = 'service'
    __tablename__ = 'service'

    # nullable=False - 该字段不允许为空
    # unique=True - 该字段的值在整个表中必须唯一，不能重复
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False, unique=True)
    group = db.Column(db.String(80), nullable=False)
    tags = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f'<Service {self.name}>'

with app.app_context():
    db.create_all()

##################################################################################################################################################

class NavigationView(ModelView):

    form_overrides = {
        'tags': SelectMultipleField,     # 将 tags 字段改为多选下拉框
        'group': SelectField,            # 将 group 字段改为单选下拉框
    }

    form_args = {
        'tags': {
            'choices': [              # 定义可选项 (value, label)
                ('ADMINISTRATION', '行政部门'),
                ('ANIMATION', '动画部门'),
                ('BOARD', '董事部门'),
                ('BUSINESS', '商务部门'),
                ('DESIGN', '设计部门'),
                ('DEVELOPMENT', '开发部门'),
                ('EFFECTS', '特效部门'),
                ('FINANCE', '财务部门'),
                ('MODELING', '建模部门'),
                ('OPERATION', '运维部门'),
                ('PHOTOGRAPHY', '摄影部门'),
                ('VIDEO', '视频部门'),
            ],
            'widget': Select2Widget(multiple=True)  # 使用更美观的下拉框，明确指定多选
        },
        'group': {
            'choices': [                 # 定义可选项 (value, label)
                ('素材资源', '素材资源'),
                ('效率工具', '效率工具'),
                ('综合平台', '综合平台'),
                ('在线文档', '在线文档'),
            ],
            'widget': Select2Widget(),    # 使用更美观的下拉框
            'default': '素材资源'         # 设置默认值
        }
    }

    # 处理数据转换：SelectMultipleField 返回的是值列表，直接赋值给 model.tags
    def on_model_change(self, form, model, is_created):
        # form.tags.data 已经是用户选择的列表，直接赋给 model.tags
        model.tags = form.tags.data
        super().on_model_change(form, model, is_created)

    # 可选：在列表页面美化 tags 显示
    column_formatters = {
        'tags': lambda v, c, m, p: ', '.join(m.tags) if m.tags else ''
    }

class ServiceView(ModelView):

    form_overrides = {
        'tags': SelectMultipleField,     # 将 tags 字段改为多选下拉框
        'group': SelectField,            # 将 group 字段改为单选下拉框
    }

    form_args = {
        'tags': {
            'choices': [              # 定义可选项 (value, label)
                ('ADMINISTRATION', '行政部门'),
                ('ANIMATION', '动画部门'),
                ('BOARD', '董事部门'),
                ('BUSINESS', '商务部门'),
                ('DESIGN', '设计部门'),
                ('DEVELOPMENT', '开发部门'),
                ('EFFECTS', '特效部门'),
                ('FINANCE', '财务部门'),
                ('MODELING', '建模部门'),
                ('OPERATION', '运维部门'),
                ('PHOTOGRAPHY', '摄影部门'),
                ('VIDEO', '视频部门'),
            ],
            'widget': Select2Widget(multiple=True)  # 使用更美观的下拉框，明确指定多选
        },
        'group': {
            'choices': [                 # 定义可选项 (value, label)
                ('DATAGC00', 'DATAGC00'),
                ('DATAGC01', 'DATAGC01'),
                ('DATABC00', 'DATABC00'),
                ('DATABC00-BACKUP', 'DATABC00-BACKUP'),
                ('DATASC00', 'DATASC00'),
                ('DATASC00-BACKUP', 'DATASC00-BACKUP'),
                ('DATASC01', 'DATASC01'),
                ('DATASC01-BACKUP', 'DATASC01-BACKUP'),
                ('DATAHC00', 'DATAHC00'),
                ('DATAHC01', 'DATAHC01'),
                ('NETWORK', 'NETWORK'),
            ],
            'widget': Select2Widget(),   # 使用更美观的下拉框
            'default': 'DATAGC00'        # 设置默认值
        }
    }

    # 处理数据转换：SelectMultipleField 返回的是值列表，直接赋值给 model.tags
    def on_model_change(self, form, model, is_created):
        # form.tags.data 已经是用户选择的列表，直接赋给 model.tags
        model.tags = form.tags.data
        super().on_model_change(form, model, is_created)

    # 可选：在列表页面美化 tags 显示
    column_formatters = {
        'tags': lambda v, c, m, p: ', '.join(m.tags) if m.tags else ''
    }

# 自定义管理后台首页视图
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        # 只有已登录用户可以访问
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # 如果用户未登录，重定向到登录页面
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.url))
        # 其他情况（这里暂不处理，但你可以根据业务逻辑返回 403）
        return abort(403)

# 自定义模型管理视图
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.url))
        return abort(403)

admin = Admin(app, name='管理后台', index_view=MyAdminIndexView())
admin.add_view(NavigationView(Navigation, db.session))
admin.add_view(ServiceView(Service, db.session))
admin.add_view(MyModelView(User, db.session))

##################################################################################################################################################

from flask import render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_required, logout_user, login_user

# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# 设置登录页面的端点，当未登录用户访问被保护的页面时会跳转到此
login_manager.login_view = 'login' # 'login' 是后面登录路由的函数名

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        # 验证用户名和密码
        if user and user.check_password(password):
            login_user(user)  # 登录用户
            # 获取 'next' 参数，登录后跳转到之前尝试访问的页面
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.index'))
        else:
            flash('用户名或密码无效', 'error')

    # GET 请求则显示登录表单
    return render_template('login.html') # 需要创建该 HTML 模板

# 实现 user_loader 回调，告诉 Flask-Login 如何根据存储在 session 中的 ID 加载用户对象
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# 定义视图函数中映射字典
tag_dict = {
    'ADMINISTRATION': '行政部门',
    'ANIMATION': '动画部门',
    'BOARD': '董事部门',
    'BUSINESS': '商务部门',
    'DESIGN': '设计部门',
    'DEVELOPMENT': '开发部门',
    'EFFECTS': '特效部门',
    'FINANCE': '财务部门',
    'MODELING': '建模部门',
    'OPERATION': '运维部门',
    'PHOTOGRAPHY': '摄影部门',
    'VIDEO': '视频部门',
}

# 路由 - 搜索引擎
@app.route('/')
def index():
    # 获取 cookie 值
    cookie_tag = request.cookies.get('tag', '')
    sidebar_option = "index"
    cookie_engine = request.cookies.get('engine', '')

    return render_template('index.html', cookie_tag=cookie_tag, tag_dict=tag_dict, sidebar_option=sidebar_option, cookie_engine=cookie_engine)

# 路由 - 外网导航
@app.route('/navigation')
def navigation():
    # 获取 cookie 值
    cookie_tag = request.cookies.get('tag', '')
    sidebar_option = "navigation"

    # 获取所有数据
    navigationData = Navigation.query.all()
    return render_template('navigation.html', navigationData=navigationData, cookie_tag=cookie_tag, tag_dict=tag_dict, sidebar_option=sidebar_option)

# 路由 - 内网服务
@app.route('/service')
def service():
    # 获取 cookie 值
    cookie_tag = request.cookies.get('tag', '')
    sidebar_option = "service"

    # 获取所有数据
    serviceData = Service.query.all()
    return render_template('service.html', serviceData=serviceData, cookie_tag=cookie_tag, tag_dict=tag_dict, sidebar_option=sidebar_option)

##################################################################################################################################################

from waitress import serve

if __name__ == '__main__':
    # 创建管理员
    with app.app_context():
        # 检查是否已存在 admin 用户
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('u6b74hfy')
            db.session.add(admin)
            db.session.commit()
            print('Admin user created.')
        else:
            print('Admin user already exists.')
    # 启动服务
    app.run(host="0.0.0.0", port=5000, debug=True)
    # serve(app, host="0.0.0.0", port=5000)
