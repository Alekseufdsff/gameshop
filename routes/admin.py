from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db, News, Product, Purchase, User
from config import Config
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('❌ Доступ запрещен. Требуются права администратора.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'total_users': User.query.count(),
        'total_products': Product.query.count(),
        'total_orders': Purchase.query.count(),
        'pending_orders': Purchase.query.filter_by(status='pending').count()
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/news/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_news():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('❌ Все поля обязательны для заполнения', 'error')
            return render_template('admin/add_news.html')
        
        news = News(
            title=title,
            content=content,
            author=current_user.username,
            is_published=True
        )
        
        db.session.add(news)
        db.session.commit()
        
        flash('✅ Новость успешно добавлена!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('admin/add_news.html')

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category = request.form.get('category')
        
        if not all([name, description, price, category]):
            flash('❌ Все поля обязательны для заполнения', 'error')
            return render_template('admin/add_product.html')
        
        try:
            price = float(price)
        except ValueError:
            flash('❌ Неверный формат цены', 'error')
            return render_template('admin/add_product.html')
        
        product = Product(
            name=name,
            description=description,
            price=price,
            category=category
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('✅ Товар успешно добавлен!', 'success')
        return redirect(url_for('shop.shop'))
    
    return render_template('admin/add_product.html')

@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    orders_list = Purchase.query.order_by(Purchase.purchase_date.desc()).all()
    return render_template('admin/orders.html', orders=orders_list)

@admin_bp.route('/order/<int:order_id>/update_status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Purchase.query.get_or_404(order_id)
    status = request.form.get('status')
    comment = request.form.get('comment', '')
    
    if status not in ['paid', 'cancelled']:
        flash('❌ Неверный статус', 'error')
        return redirect(url_for('admin.orders'))
    
    order.status = status
    order.admin_comment = comment
    
    db.session.commit()
    
    flash(f'✅ Статус заказа #{order.id} обновлен на "{status}"', 'success')
    return redirect(url_for('admin.orders'))

@admin_bp.route('/news/delete/<int:news_id>')
@login_required
@admin_required
def delete_news(news_id):
    news = News.query.get_or_404(news_id)
    db.session.delete(news)
    db.session.commit()
    flash('✅ Новость удалена', 'success')
    return redirect(url_for('main.index'))