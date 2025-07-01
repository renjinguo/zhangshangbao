"""
路由模块 - 企业管理系统的Web路由实现

本模块包含整个企业管理系统的所有Flask路由和功能，主要包括:

1. 用户认证与会话管理
   - 登录(/login): 用户登录系统
   - 登出(/logout): 用户注销

2. 联系人管理
   - 联系人列表(/contacts): 显示所有联系人
   - 添加联系人(/contacts/add): 创建新联系人
   - 编辑联系人(/contacts/edit/<id>): 更新联系人信息
   - 删除联系人(/contacts/delete/<id>): 删除指定联系人

3. 聊天和消息系统
   - 聊天界面(/chat): 显示聊天主页面和联系人列表
   - 与联系人聊天(/chat/<id>): 与特定联系人的聊天界面
   - 撤回消息(/chat/recall/<id>): 撤回已发送的消息

4. 部门管理
   - 部门列表(/departments): 显示所有部门
   - 创建部门(/departments/create): 添加新部门
   - 编辑部门(/departments/<id>/edit): 更新部门信息
   - 删除部门(/departments/<id>/delete): 删除指定部门

5. 员工管理
   - 员工列表(/employees): 显示所有员工
   - 添加员工(/employees/create): 创建新员工
   - 编辑员工(/employees/<id>/edit): 更新员工信息
   - 删除员工(/employees/<id>/delete): 删除指定员工

6. 公司主数据管理
   - 公司列表(/companies): 显示所有公司
   - 添加公司(/companies/create): 创建新公司
   - 编辑公司(/companies/<id>/edit): 更新公司信息
   - 删除公司(/companies/<id>/delete): 删除指定公司

7. 系统初始化
   - init_app函数用于初始化数据库和创建默认用户

该模块还包括文件上传处理、全局上下文处理以及各种辅助功能。
"""

from flask import render_template, request, redirect, url_for, flash, jsonify, session, current_app
from .models import db, User, Message, Department, Material, Employee, Company
import os
from werkzeug.utils import secure_filename
import re

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_app(app):
    with app.app_context():
        db.create_all()
        # 初始化3个用户
        if User.query.count() == 0:
            users = [
                dict(username='admin', name='管理员', phone='13800000001', email='admin@test.com', department='管理', remark='系统管理员'),
                dict(username='alice', name='爱丽丝', phone='13800000002', email='alice@test.com', department='市场', remark='市场部'),
                dict(username='bob', name='鲍勃', phone='13800000003', email='bob@test.com', department='技术', remark='技术部')
            ]
            for u in users:
                user = User(**u)
                user.set_password('123456')
                db.session.add(user)
            db.session.commit()

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                flash('登录成功', 'success')
                return redirect(url_for('home'))
            flash('用户名或密码错误', 'danger')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('login'))

    # 全局上下文处理器，所有模板都能用current_user
    @app.context_processor
    def inject_current_user():
        user = None
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
        return dict(current_user=user)

    @app.route('/')
    def index():
        return redirect(url_for('login'))

    @app.route('/home')
    def home():
        return render_template('home.html')

    @app.route('/contacts')
    def contacts():
        user_list = User.query.all()
        return render_template('contacts.html', contacts=user_list)

    @app.route('/contacts/add', methods=['GET', 'POST'])
    def add_contact():
        if request.method == 'POST':
            username = request.form['username']
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            department = request.form['department']
            remark = request.form['remark']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                flash('用户名已存在', 'danger')
                return redirect(url_for('add_contact'))
            new_user = User(username=username, name=name, phone=phone, email=email, department=department, remark=remark)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('联系人添加成功', 'success')
            return redirect(url_for('contacts'))
        return render_template('contact_form.html', action='add', contact=None)

    @app.route('/contacts/edit/<int:contact_id>', methods=['GET', 'POST'])
    def edit_contact(contact_id):
        contact = User.query.get_or_404(contact_id)
        if request.method == 'POST':
            contact.username = request.form['username']
            contact.name = request.form['name']
            contact.phone = request.form['phone']
            contact.email = request.form['email']
            contact.department = request.form['department']
            contact.remark = request.form['remark']
            password = request.form.get('password')
            if password:
                contact.set_password(password)
            db.session.commit()
            flash('联系人信息已更新', 'success')
            return redirect(url_for('contacts'))
        return render_template('contact_form.html', action='edit', contact=contact)

    @app.route('/contacts/delete/<int:contact_id>', methods=['POST'])
    def delete_contact(contact_id):
        contact = User.query.get_or_404(contact_id)
        db.session.delete(contact)
        db.session.commit()
        flash('联系人已删除', 'success')
        return redirect(url_for('contacts'))

    @app.route('/chat', methods=['GET'])
    def chat():
        if not session.get('user_id'):
            return redirect(url_for('login'))
        current_id = session['user_id']
        contacts = User.query.filter(User.id != current_id).all()
        # 统计每个联系人发给当前用户的未读消息数（只统计未读，chat_with已读后刷新chat才会消失）
        unread_counts = {}
        for c in contacts:
            count = Message.query.filter_by(sender_id=c.id, receiver_id=current_id, status='unread').count()
            unread_counts[c.id] = count
        return render_template('chat.html', contacts=contacts, current_user_id=current_id, unread_counts=unread_counts)

    @app.route('/chat/<int:contact_id>', methods=['GET', 'POST'])
    def chat_with(contact_id):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        current_id = session['user_id']
        contacts = User.query.filter(User.id != current_id).all()
        target = User.query.get_or_404(contact_id)
        sender_id = current_id
        if request.method == 'POST':
            content = request.form.get('content', '')
            file = request.files.get('file')
            file_path = None
            file_type = 'none'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                ext = filename.rsplit('.', 1)[1].lower()
                file_path = os.path.join('static', 'uploads', filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if ext in ['png', 'jpg', 'jpeg', 'gif']:
                    file_type = 'image'
                else:
                    file_type = 'file'
            emoji_map = {':smile:': '😄', ':sad:': '😢', ':thumbsup:': '👍', ':heart:': '❤️', ':laugh:': '😂'}
            for k, v in emoji_map.items():
                content = content.replace(k, v)
            msg = Message(sender_id=sender_id, receiver_id=contact_id, content=content, file_path=file_path, file_type=file_type)
            db.session.add(msg)
            db.session.commit()
            flash('消息已发送', 'success')
            return redirect(url_for('chat_with', contact_id=contact_id))
        # 查询当前用户与目标用户的所有消息
        messages = Message.query.filter(
            ((Message.sender_id==current_id) & (Message.receiver_id==contact_id)) |
            ((Message.sender_id==contact_id) & (Message.receiver_id==current_id))
        ).order_by(Message.created_at).all()
        # 只将当前聊天对象发给当前用户的未读消息标记为已读
        unread_msgs = Message.query.filter_by(sender_id=contact_id, receiver_id=current_id, status='unread').all()
        for m in unread_msgs:
            m.status = 'read'
        db.session.commit()
        # 统计每个联系人发给当前用户的未读消息数（用于侧边栏角标）
        unread_counts = {}
        for c in contacts:
            count = Message.query.filter_by(sender_id=c.id, receiver_id=current_id, status='unread').count()
            unread_counts[c.id] = count
        return render_template('chat_with.html', contacts=contacts, target=target, messages=messages, sender_id=current_id, unread_counts=unread_counts)

    @app.route('/chat/recall/<int:msg_id>', methods=['POST'])
    def recall_message(msg_id):
        msg = Message.query.get_or_404(msg_id)
        msg.is_recalled = True
        db.session.commit()
        return jsonify({'success': True})

    # 部门管理路由
    @app.route('/departments')
    def list_departments():
        departments = Department.query.order_by(Department.code).all()
        return render_template('department/list.html', departments=departments)

    @app.route('/departments/create', methods=['GET', 'POST'])
    def create_department():
        from .models import Company
        companies = Company.query.order_by(Company.name).all()
        if request.method == 'POST':
            code = request.form['code']
            name = request.form['name']
            manager = request.form.get('manager', '')
            phone = request.form.get('phone', '')
            company_id = request.form.get('company_id')
            if Department.query.filter_by(code=code).first():
                flash('部门编码已存在', 'danger')
                return redirect(url_for('create_department'))
            department = Department(code=code, name=name, manager=manager, phone=phone, company_id=company_id)
            db.session.add(department)
            db.session.commit()
            flash('部门创建成功', 'success')
            return redirect(url_for('list_departments'))
        return render_template('department/create.html', companies=companies)

    @app.route('/departments/<int:id>/edit', methods=['GET', 'POST'])
    def edit_department(id):
        from .models import Company
        department = Department.query.get_or_404(id)
        companies = Company.query.order_by(Company.name).all()
        if request.method == 'POST':
            department.code = request.form['code']
            department.name = request.form['name']
            department.manager = request.form.get('manager', '')
            department.phone = request.form.get('phone', '')
            department.company_id = request.form.get('company_id')
            db.session.commit()
            flash('部门信息已更新', 'success')
            return redirect(url_for('list_departments'))
        return render_template('department/edit.html', department=department, companies=companies)

    @app.route('/departments/<int:id>/delete', methods=['POST'])
    def delete_department(id):
        department = Department.query.get_or_404(id)
        db.session.delete(department)
        db.session.commit()
        flash('部门已删除', 'success')
        return redirect(url_for('list_departments'))

    # 员工管理路由
    @app.route('/employees')
    def list_employees():
        employees = Employee.query.order_by(Employee.name).all()
        departments = {d.id: d.name for d in Department.query.all()}
        return render_template('employee/list.html', employees=employees, departments=departments)

    @app.route('/employees/create', methods=['GET', 'POST'])
    def create_employee():
        from .models import Company
        if request.method == 'POST':
            employee_id = request.form['employee_id']
            name = request.form['name']
            department_id = request.form['department_id']
            position = request.form.get('position', '')
            from datetime import datetime
            hire_date_str = request.form.get('hire_date')
            phone = request.form.get('phone', '')
            email = request.form.get('email', '')
            status = request.form.get('status', 'active')
            if Employee.query.filter_by(employee_id=employee_id).first():
                flash('员工ID已存在', 'danger')
                return redirect(url_for('create_employee'))
            hire_date = datetime.strptime(hire_date_str, '%Y-%m-%d').date() if hire_date_str else None
            employee = Employee(
                employee_id=employee_id,
                name=name,
                department_id=department_id,
                position=position,
                hire_date=hire_date,
                phone=phone,
                email=email,
                status=status
            )
            db.session.add(employee)
            db.session.commit()
            flash('员工创建成功', 'success')
            return redirect(url_for('list_employees'))
        departments = Department.query.order_by(Department.name).all()
        companies = Company.query.order_by(Company.name).all()
        return render_template('employee/create.html', departments=departments, companies=companies)

    @app.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
    def edit_employee(id):
        employee = Employee.query.get_or_404(id)
        if request.method == 'POST':
            employee.employee_id = request.form['employee_id']
            employee.name = request.form['name']
            employee.department_id = request.form['department_id']
            employee.position = request.form.get('position', '')
            from datetime import datetime
            hire_date_str = request.form.get('hire_date')
            # 转换日期字符串为date对象
            employee.hire_date = datetime.strptime(hire_date_str, '%Y-%m-%d').date() if hire_date_str else None
            employee.phone = request.form.get('phone', '')
            employee.email = request.form.get('email', '')
            employee.status = request.form.get('status', 'active')
            db.session.commit()
            flash('员工信息已更新', 'success')
            return redirect(url_for('list_employees'))
        departments = Department.query.order_by(Department.name).all()
        return render_template('employee/edit.html', employee=employee, departments=departments)

    @app.route('/employees/<int:id>/delete', methods=['POST'])
    def delete_employee(id):
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        flash('员工已删除', 'success')
        return redirect(url_for('list_employees'))

    # 公司主数据CRUD
    @app.route('/companies')
    def list_companies():
        companies = Company.query.order_by(Company.code).all()
        return render_template('company/list.html', companies=companies)

    @app.route('/companies/create', methods=['GET', 'POST'])
    def create_company():
        if request.method == 'POST':
            code = request.form['code']
            name = request.form['name']
            address = request.form.get('address', '')
            phone = request.form.get('phone', '')
            if Company.query.filter_by(code=code).first():
                flash('公司编码已存在', 'danger')
                return redirect(url_for('create_company'))
            company = Company(code=code, name=name, address=address, phone=phone)
            db.session.add(company)
            db.session.commit()
            flash('公司创建成功', 'success')
            return redirect(url_for('list_companies'))
        return render_template('company/create.html')

    @app.route('/companies/<int:id>/edit', methods=['GET', 'POST'])
    def edit_company(id):
        company = Company.query.get(id)
        if request.method == 'POST':
            company.code = request.form['code']
            company.name = request.form['name']
            company.address = request.form.get('address', '')
            company.phone = request.form.get('phone', '')
            db.session.commit()
            flash('公司信息已更新', 'success')
            return redirect(url_for('list_companies'))
        return render_template('company/edit.html', company=company)

    @app.route('/companies/<int:id>/delete', methods=['POST'])
    def delete_company(id):
        company = Company.query.get(id)
        db.session.delete(company)
        db.session.commit()
        flash('公司已删除', 'success')
        return redirect(url_for('list_companies'))

    @app.route('/test/employee')
    def test_employee():
        try:
            # 检查Employee表是否存在
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'employee' not in tables:
                return jsonify({
                    'status': 'error',
                    'message': 'Employee表不存在',
                    'tables': tables
                })
            
            # 测试创建员工
            test_emp = Employee(
                employee_id='TEST001',
                name='测试员工',
                department_id=1,
                position='测试职位'
            )
            db.session.add(test_emp)
            db.session.commit()
            
            # 测试查询
            emp = Employee.query.filter_by(employee_id='TEST001').first()
            if emp:
                return jsonify({
                    'status': 'success',
                    'message': 'Employee模型测试通过',
                    'data': {
                        'id': emp.id,
                        'name': emp.name,
                        'position': emp.position
                    }
                })
            return jsonify({'status': 'error', 'message': 'Employee查询失败'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})