from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user
from app.models import PasswordEntry
from app.utils.encryption import encrypt, decrypt
from app import db
from app.routes import vault

@vault.route('/dashboard')
@login_required
def dashboard():
    entries = PasswordEntry.query.filter_by(user=current_user).all()
    for entry in entries:
        entry.password_encrypted = decrypt(entry.password_encrypted)
    return render_template('dashboard.html', entries=entries)

@vault.route('/add', methods=['GET', 'POST'])
@login_required
def add_entry():
    if request.method == 'POST':
        brand = request.form.get('brand')
        app = request.form.get('app')
        username = request.form.get('username')
        email = request.form.get('email')
        login_link = request.form.get('login_link')
        raw_password = request.form.get('password')
        encrypted_password = encrypt(raw_password)
        twofa_enabled = request.form.get('twofa') == 'on'

        entry = PasswordEntry(
            brand=brand,
            app=app,
            username=username,
            email=email,
            login_link=login_link,
            password_encrypted=encrypted_password,
            twofa_enabled=twofa_enabled,
            user=current_user
        )
        db.session.add(entry)
        db.session.commit()
        flash('Entry added successfully.', 'success')
        return redirect(url_for('vault.dashboard'))

    return render_template('add-new.html')

@vault.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    entry = PasswordEntry.query.get_or_404(id)
    if entry.user != current_user:
        flash('Access denied.', 'danger')
        return redirect(url_for('vault.dashboard'))

    if request.method == 'POST':
        entry.brand = request.form.get('brand')
        entry.app = request.form.get('app')
        entry.username = request.form.get('username')
        entry.email = request.form.get('email')
        entry.login_link = request.form.get('login_link')
        raw_password = request.form.get('password')
        entry.password_encrypted = encrypt(raw_password)
        entry.twofa_enabled = request.form.get('twofa') == 'on'
        db.session.commit()
        flash('Entry updated successfully.', 'success')
        return redirect(url_for('vault.dashboard'))

    entry.password_encrypted = decrypt(entry.password_encrypted)
    return render_template('update.html', entry=entry)

@vault.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_entry(id):
    entry = PasswordEntry.query.get_or_404(id)
    if entry.user != current_user:
        flash('Access denied.', 'danger')
        return redirect(url_for('vault.dashboard'))

    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted successfully.', 'info')
    return redirect(url_for('vault.dashboard'))

@vault.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
