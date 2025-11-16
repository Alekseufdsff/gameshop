from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from config import Config
import re

auth_bp = Blueprint('auth', __name__)

def is_strong_password(password):
    """Проверка сложности пароля"""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Валидация
        if not all([username, email, password]):
            flash('❌ Все поля обязательны для заполнения', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('❌ Пароли не совпадают', 'error')
            return render_template('auth/register.html')
        
        if not is_strong_password(password):
            flash('❌ Пароль должен быть не менее 8 символов, содержать заглавные и строчные буквы, цифры и специальные символы', 'error')
            return render_template('auth/register.html')
        
        # Проверка существующего пользователя
        if User.query.filter_by(username=username).first():
            flash('❌ Пользователь с таким именем уже существует', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('❌ Пользователь с таким email уже существует', 'error')
            return render_template('auth/register.html')
        
        # Создание пользователя
        hashed_password = generate_password_hash(password)
        is_admin = (username == Config.ADMIN_USERNAME)
        
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            is_admin=is_admin
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('✅ Регистрация успешна! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('❌ Неверное имя пользователя или пароль', 'error')
            return render_template('auth/login.html')
        
        login_user(user, remember=remember)
        
        flash(f'✅ Добро пожаловать, {username}!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('✅ Вы успешно вышли из системы', 'success')
    return redirect(url_for('main.index'))