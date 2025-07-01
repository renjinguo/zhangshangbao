"""
客户管理模块 (Customer Management Module)

本模块提供客户信息的完整管理功能，包括客户的创建、查看、编辑和删除操作。
所有操作都通过Flask Blueprint实现，前缀为'/customer'。

包含的路由:
- / : 显示所有客户列表，按客户编码排序
- /create : 创建新客户，支持GET(显示表单)和POST(提交数据)请求
- /<id>/edit : 编辑现有客户信息，支持GET(显示表单)和POST(提交数据)请求
- /<id>/delete : 删除客户信息，仅支持POST请求

客户信息包括：客户编码、名称、类别、联系人、电话、邮箱、地址、税号、状态和所属公司等重要属性。
本模块确保客户编码的唯一性，并提供适当的用户反馈信息。
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Customer
from app import db
from datetime import datetime
bp = Blueprint('customer', __name__, url_prefix='/customer')

@bp.route('/')
def index():
    customers = Customer.query.order_by(Customer.customer_code).all()
    return render_template('customer/index.html', customers=customers)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        customer_code = request.form['customer_code']
        name = request.form['name']
        category = request.form.get('category')
        contact_person = request.form.get('contact_person')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        tax_id = request.form.get('tax_id')
        status = request.form.get('status', 'active')
        company_id = request.form.get('company_id')
        
        if Customer.query.filter_by(customer_code=customer_code).first():
            flash('客户编码已存在', 'danger')
            return redirect(url_for('customer.create'))
            
        customer = Customer(
            customer_code=customer_code,
            name=name,
            category=category,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address,
            tax_id=tax_id,
            status=status,
            company_id=company_id
        )
        
        db.session.add(customer)
        db.session.commit()
        flash('客户创建成功', 'success')
        return redirect(url_for('customer.index'))
    
    from app.models import Company
    companies = Company.query.all()
    return render_template('customer/create.html', companies=companies)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        customer.customer_code = request.form['customer_code']
        customer.name = request.form['name']
        customer.category = request.form.get('category')
        customer.contact_person = request.form.get('contact_person')
        customer.phone = request.form.get('phone')
        customer.email = request.form.get('email')
        customer.address = request.form.get('address')
        customer.tax_id = request.form.get('tax_id')
        customer.status = request.form.get('status', 'active')
        customer.company_id = request.form.get('company_id')
        
        db.session.commit()
        flash('客户信息更新成功', 'success')
        return redirect(url_for('customer.index'))
    
    from app.models import Company
    companies = Company.query.all()
    return render_template('customer/edit.html', customer=customer, companies=companies)

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('客户删除成功', 'success')
    return redirect(url_for('customer.index'))