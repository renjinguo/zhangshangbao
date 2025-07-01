"""
供应商管理模块 (Supplier Management Module)

该模块提供了对供应商信息的全面管理功能，包括创建、查看、编辑和删除供应商记录。

包含的路由:
- / : 显示所有供应商列表
- /create : 创建新供应商（GET显示表单，POST处理提交）
- /<id>/edit : 编辑现有供应商信息（GET显示表单，POST处理更新）
- /<id>/delete : 删除供应商记录（仅POST方法）

供应商信息包括：供应商编码、名称、联系人、电话、电子邮件、地址、
税号、状态以及关联的公司ID等基本信息。
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Supplier
from app import db

bp = Blueprint('supplier', __name__, url_prefix='/supplier')

@bp.route('/')
def index():
    suppliers = Supplier.query.order_by(Supplier.supplier_code).all()
    return render_template('supplier/index.html', suppliers=suppliers)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        supplier_code = request.form['supplier_code']
        name = request.form['name']
        contact_person = request.form.get('contact_person')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        tax_id = request.form.get('tax_id')
        status = request.form.get('status', 'active')
        company_id = request.form.get('company_id')
        if Supplier.query.filter_by(supplier_code=supplier_code).first():
            flash('供应商编码已存在', 'danger')
            return redirect(url_for('supplier.create'))
        supplier = Supplier(
            supplier_code=supplier_code,
            name=name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address,
            tax_id=tax_id,
            status=status,
            company_id=company_id
        )
        db.session.add(supplier)
        db.session.commit()
        flash('供应商创建成功', 'success')
        return redirect(url_for('supplier.index'))
    from app.models import Company
    companies = Company.query.all()
    return render_template('supplier/create.html', companies=companies)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    supplier = Supplier.query.get_or_404(id)
    if request.method == 'POST':
        supplier.supplier_code = request.form['supplier_code']
        supplier.name = request.form['name']
        supplier.contact_person = request.form.get('contact_person')
        supplier.phone = request.form.get('phone')
        supplier.email = request.form.get('email')
        supplier.address = request.form.get('address')
        supplier.tax_id = request.form.get('tax_id')
        supplier.status = request.form.get('status', 'active')
        supplier.company_id = request.form.get('company_id')
        db.session.commit()
        flash('供应商信息更新成功', 'success')
        return redirect(url_for('supplier.index'))
    from app.models import Company
    companies = Company.query.all()
    return render_template('supplier/edit.html', supplier=supplier, companies=companies)

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    flash('供应商删除成功', 'success')
    return redirect(url_for('supplier.index'))