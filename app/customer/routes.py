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