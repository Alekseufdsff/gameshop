from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from models import News, Purchase

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    news_list = News.query.filter_by(is_published=True).order_by(News.date_posted.desc()).all()
    return render_template('index.html', news_list=news_list)

@main_bp.route('/profile')
@login_required
def profile():
    user_purchases = Purchase.query.filter_by(user_id=current_user.id).order_by(Purchase.purchase_date.desc()).all()
    return render_template('profile.html', purchases=user_purchases)

@main_bp.route('/my_purchases')
@login_required
def my_purchases():
    purchases = Purchase.query.filter_by(user_id=current_user.id).order_by(Purchase.purchase_date.desc()).all()
    return render_template('shop/my_purchases.html', purchases=purchases)

@main_bp.route('/support')
def support():
    return render_template('support.html')