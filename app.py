from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from models import db, User, Message
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}

db.init_app(app)

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        count = Message.query.filter_by(sender_id=c.id, receiver_id=current_id, is_read=False).count()
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
    ).order_by(Message.timestamp).all()
    # 只将当前聊天对象发给当前用户的未读消息标记为已读
    unread_msgs = Message.query.filter_by(sender_id=contact_id, receiver_id=current_id, is_read=False).all()
    for m in unread_msgs:
        m.is_read = True
    db.session.commit()
    # 统计每个联系人发给当前用户的未读消息数（用于侧边栏角标）
    unread_counts = {}
    for c in contacts:
        count = Message.query.filter_by(sender_id=c.id, receiver_id=current_id, is_read=False).count()
        unread_counts[c.id] = count
    return render_template('chat_with.html', contacts=contacts, target=target, messages=messages, sender_id=current_id, unread_counts=unread_counts)

@app.route('/chat/recall/<int:msg_id>', methods=['POST'])
def recall_message(msg_id):
    msg = Message.query.get_or_404(msg_id)
    msg.is_recalled = True
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)