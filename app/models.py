from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    department = db.Column(db.String(50))
    remark = db.Column(db.String(200))
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Customer(db.Model):
    __tablename__ = 'customer'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20))  # 客户分类：个人/企业
    contact_person = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    tax_id = db.Column(db.String(30))  # 税号
    status = db.Column(db.String(10), default='active')  # active/inactive
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))  # 新增：公司ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = db.relationship('Company', backref='customers')
    
    def __repr__(self):
        return f'<Customer {self.customer_code}>'

class Material(db.Model):
    __tablename__ = 'material'
    
    id = db.Column(db.Integer, primary_key=True)
    material_code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20))  # 物料分类
    specification = db.Column(db.String(200))  # 规格型号
    unit = db.Column(db.String(10))  # 单位
    purchase_price = db.Column(db.Numeric(10, 2))  # 采购价
    sales_price = db.Column(db.Numeric(10, 2))  # 销售价
    stock = db.Column(db.Integer, default=0)  # 库存数量
    status = db.Column(db.String(10), default='active')  # active/inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Material {self.material_code}>'

class Message(db.Model):
    __tablename__ = 'message'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(10), default='unread')  # unread/read
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(256))  # 文件路径
    file_type = db.Column(db.String(20))   # 文件类型
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
    
    @property
    def timestamp(self):
        return self.created_at
    
    def __repr__(self):
        return f'<Message {self.id}>'

class Company(db.Model):
    __tablename__ = 'company'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    departments = db.relationship('Department', backref='company', lazy=True)
    
    def __repr__(self):
        return f'<Company {self.code}>'

class Department(db.Model):
    __tablename__ = 'department'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # 部门编码
    name = db.Column(db.String(50), nullable=False)  # 部门名称
    manager = db.Column(db.String(50))  # 负责人
    phone = db.Column(db.String(20))  # 联系电话
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))  # 新增：公司ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    employees = db.relationship('Employee', backref='department', lazy=True)
    
    def __repr__(self):
        return f'<Department {self.code}>'

class Employee(db.Model):
    __tablename__ = 'employee'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)  # 员工ID
    name = db.Column(db.String(50), nullable=False)  # 姓名
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))  # 部门ID
    position = db.Column(db.String(50))  # 职位
    hire_date = db.Column(db.Date)  # 入职日期
    phone = db.Column(db.String(20))  # 电话
    email = db.Column(db.String(100))  # 邮箱
    status = db.Column(db.String(10), default='active')  # 状态: active/inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Employee {self.employee_id}>'

class Supplier(db.Model):
    __tablename__ = 'supplier'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    tax_id = db.Column(db.String(30))
    status = db.Column(db.String(10), default='active')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))  # 新增：公司ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    company = db.relationship('Company', backref='suppliers')

    def __repr__(self):
        return f'<Supplier {self.supplier_code}>'