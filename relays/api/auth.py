# api/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import SessionLocal, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username', '')
        p = request.form.get('password', '')
        db = SessionLocal()
        user = db.query(User).filter_by(username=u).first()
        db.close()
        if user and user.password == p:
            login_user(user)
            # redirige por rol:
            if user.role == 'admin':
                return redirect(url_for('admin.panel'))
            else:
                return redirect(url_for('remote.remote_panel'))
        flash('Credenciales inválidas', 'danger')
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
