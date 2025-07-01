
"""
掌上宝企业管理系统 - 代码文档

本文件提供了对系统中各个模块和数据模型的详细说明，
帮助开发人员理解系统架构和各组件间的关系。
"""

# 模型文档
MODEL_DOCS = {
    'User': {
        '描述': '系统用户模型，用于身份认证和用户信息管理',
        '重要字段': {
            'username': '用户名，唯一标识，用于登录',
            'password_hash': '密码哈希，使用werkzeug的安全哈希函数加密存储',
            'name': '用户真实姓名',
            'department': '用户所属部门'
        },
        '关键方法': {
            'set_password': '设置密码（进行哈希加密）',
            'check_password': '验证密码是否正确'
        },
        '关联关系': {
            'sent_messages': '用户发送的消息（一对多）',
            'received_messages': '用户接收的消息（一对多）'
        }
    },
    'Customer': {
        '描述': '客户信息模型，存储客户相关数据',
        '重要字段': {
            'customer_code': '客户编码，系统内唯一',
            'name': '客户名称',
            'category': '客户分类（个人/企业）',
            'tax_id': '税号，用于发票等税务操作',
            'status': '状态（active/inactive）'
        },
        '关联关系': {
            'company': '关联的公司实体（多对一）'
        }
    },
    'Material': {
        '描述': '物料/产品信息模型',
        '重要字段': {
            'material_code': '物料编码，系统内唯一',
            'name': '物料名称',
            'specification': '规格型号',
            'purchase_price': '采购价',
            'sales_price': '销售价',
            'stock': '库存数量'
        }
    },
    'Message': {
        '描述': '消息模型，用于用户间即时通讯',
        '重要字段': {
            'sender_id': '发送者用户ID',
            'receiver_id': '接收者用户ID',
            'content': '消息内容',
            'status': '消息状态（已读/未读）',
            'file_path': '附件路径',
            'file_type': '附件类型'
        },
        '关联关系': {
            'sender': '消息发送者（多对一关系到User）',
            'receiver': '消息接收者（多对一关系到User）'
        }
    },
    'Company': {
        '描述': '公司模型，作为组织结构的顶层单位',
        '重要字段': {
            'code': '公司编码',
            'name': '公司名称'
        },
        '关联关系': {
            'departments': '公司下属部门（一对多）',
            'customers': '关联的客户（一对多）',
            'suppliers': '关联的供应商（一对多）'
        }
    },
    'Department': {
        '描述': '部门模型，企业组织结构单位',
        '重要字段': {
            'code': '部门编码',
            'name': '部门名称',
            'manager': '部门负责人',
            'company_id': '所属公司ID'
        },
        '关联关系': {
            'company': '所属公司（多对一）',
            'employees': '部门员工（一对多）'
        }
    },
    'Employee': {
        '描述': '员工模型，存储员工基本信息',
        '重要字段': {
            'employee_id': '员工工号',
            'name': '员工姓名',
            'department_id': '所属部门ID',
            'position': '职位',
            'hire_date': '入职日期',
            'status': '状态（active/inactive）'
        },
        '关联关系': {
            'department': '所属部门（多对一）'
        }
    },
    'Supplier': {
        '描述': '供应商模型，存储供应商信息',
        '重要字段': {
            'supplier_code': '供应商编码',
            'name': '供应商名称',
            'contact_person': '联系人',
            'tax_id': '税号',
            'status': '状态（active/inactive）'
        },
        '关联关系': {
            'company': '关联公司（多对一）'
        }
    }
}

# 路由模块说明
ROUTE_DOCS = {
    'app/routes.py': {
        '描述': '主路由模块，包含用户认证、联系人、消息、部门和员工等核心功能',
        '主要功能': [
            '用户登录/登出',
            '联系人管理CRUD操作',
            '即时消息功能',
            '部门管理',
            '员工管理',
            '公司管理'
        ]
    },
    'app/customer/routes.py': {
        '描述': '客户管理模块路由',
        '主要功能': [
            '客户列表展示',
            '添加新客户',
            '编辑客户信息',
            '删除客户'
        ]
    },
    'app/supplier/routes.py': {
        '描述': '供应商管理模块路由',
        '主要功能': [
            '供应商列表展示',
            '添加新供应商',
            '编辑供应商信息',
            '删除供应商'
        ]
    },
    'app/views/material_views.py': {
        '描述': '物料管理视图模块',
        '主要功能': [
            '物料列表展示',
            '添加新物料',
            '编辑物料信息',
            '删除物料'
        ]
    }
}

# 系统配置说明
SYSTEM_CONFIG = {
    '描述': '系统主要配置参数说明',
    '数据库': 'SQLite (app/__init__.py中配置)',
    '上传目录': 'app/static/uploads',
    '允许上传的文件类型': ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'],
    '最大上传文件大小': '16MB'
}

# 初始化数据说明
INIT_DATA = {
    '描述': '系统初始化数据',
    '初始用户': [
        {'username': 'admin', 'name': '管理员', 'department': '管理', 'password': '123456'},
        {'username': 'alice', 'name': '爱丽丝', 'department': '市场', 'password': '123456'},
        {'username': 'bob', 'name': '鲍勃', 'department': '技术', 'password': '123456'}
    ]
}

# 功能点用法示例
USAGE_EXAMPLES = {
    '文件上传': """
# 在routes.py的chat_with函数中处理文件上传:
file = request.files.get('file')
if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file_path = os.path.join('static', 'uploads', filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
""",
    '用户认证': """
# 用户登录验证示例:
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
"""
}

def get_model_documentation(model_name):
    """获取指定模型的文档信息

    Args:
        model_name: 模型名称，例如'User', 'Customer'等

    Returns:
        dict: 包含模型描述信息的字典
    """
    return MODEL_DOCS.get(model_name, {'描述': '未找到该模型的文档'})
