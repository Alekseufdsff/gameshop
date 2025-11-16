from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db, Product, Purchase
import secrets

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/shop')
def shop():
    products = Product.query.filter_by(is_active=True).all()
    return render_template('shop/shop.html', products=products)

@shop_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('shop/product_detail.html', product=product)

@shop_bp.route('/purchase/<int:product_id>', methods=['GET', 'POST'])
@login_required
def purchase_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        tg_username = request.form.get('tg_username')
        customer_email = request.form.get('customer_email')
        customer_name = request.form.get('customer_name')
        
        if not all([tg_username, customer_email, customer_name]):
            flash('❌ Все поля обязательны для заполнения', 'error')
            return render_template('shop/purchase_confirm.html', product=product)
        
        # Создание заказа
        purchase = Purchase(
            user_id=current_user.id,
            product_id=product.id,
            tg_username=tg_username,
            customer_email=customer_email,
            customer_name=customer_name,
            status='pending'
        )
        
        db.session.add(purchase)
        db.session.commit()
        
        flash('✅ Заказ успешно создан! Ожидайте подтверждения от администратора.', 'success')
        return redirect(url_for('shop.my_purchases'))
    
    return render_template('shop/purchase_confirm.html', product=product)

@shop_bp.route('/cancel_purchase/<string:order_token>')
@login_required
def cancel_purchase(order_token):
    purchase = Purchase.query.filter_by(order_token=order_token, user_id=current_user.id).first_or_404()
    
    if purchase.status == 'pending':
        purchase.status = 'cancelled'
        db.session.commit()
        flash('✅ Заказ отменен', 'success')
    else:
        flash('❌ Невозможно отменить этот заказ', 'error')
    
    return redirect(url_for('main.my_purchases'))