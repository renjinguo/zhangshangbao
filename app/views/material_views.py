"""
物料管理模块视图 (Material Management Views)

该模块提供物料管理的所有视图函数，处理物料的创建、查询、更新和删除操作(CRUD)。

路由包括:
- GET  /material/          : 列出所有物料
- GET  /material/create    : 显示物料创建表单
- POST /material/create    : 处理物料创建请求
- GET  /material/edit/<id> : 显示物料编辑表单
- POST /material/edit/<id> : 处理物料更新请求
- POST /material/delete/<id>: 处理物料删除请求

与其他模块关系:
- 依赖于models模块中的Material模型
- 使用主应用中的db对象进行数据库操作
- 通过Blueprint集成到主应用程序中
"""
from flask import render_template, request, redirect, url_for, flash, Blueprint
from .. import db
from ..models import Material

material_bp = Blueprint('material', __name__, url_prefix='/material')

@material_bp.route('/')
def list_materials():
    materials = Material.query.all()
    return render_template('material/list.html', materials=materials)

@material_bp.route('/create', methods=['GET', 'POST'])
def create_material():
    if request.method == 'POST':
        material_code = request.form['code']
        name = request.form['name']
        specification = request.form['spec']
        unit = request.form['unit']
        category = request.form.get('category', '')
        purchase_price = float(request.form.get('purchase_price', 0))
        sales_price = float(request.form.get('sales_price', 0))
        stock = int(request.form.get('stock', 0))
        
        material = Material(
            material_code=material_code,
            name=name,
            specification=specification,
            unit=unit,
            category=category,
            purchase_price=purchase_price,
            sales_price=sales_price,
            stock=stock
        )
        db.session.add(material)
        db.session.commit()
        flash('物料创建成功', 'success')
        return redirect(url_for('material.list_materials'))
    
    return render_template('material/create.html')

@material_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_material(id):
    material = Material.query.get_or_404(id)
    if request.method == 'POST':
        material.material_code = request.form['code']
        material.name = request.form['name']
        material.specification = request.form['spec']
        material.unit = request.form['unit']
        material.category = request.form.get('category', '')
        material.purchase_price = float(request.form.get('purchase_price', 0))
        material.sales_price = float(request.form.get('sales_price', 0))
        material.stock = int(request.form.get('stock', 0))
        
        db.session.commit()
        flash('物料更新成功', 'success')
        return redirect(url_for('material.list_materials'))
    
    return render_template('material/edit.html', material=material)

@material_bp.route('/delete/<int:id>', methods=['POST'])
def delete_material(id):
    material = Material.query.get_or_404(id)
    db.session.delete(material)
    db.session.commit()
    flash('物料删除成功', 'success')
    return redirect(url_for('material.list_materials'))