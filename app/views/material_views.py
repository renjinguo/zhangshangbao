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