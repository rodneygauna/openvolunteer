"""Users > Views"""
# Imports
from datetime import datetime
from random import randint
from flask import (
    Blueprint, abort, render_template, request, flash,
    redirect, url_for, session)
from werkzeug.security import generate_password_hash
from flask_login import (
    login_user, login_required, logout_user,
    current_user)
from flask_mail import Message
from users.forms import (
    RegisterUserForm, EditProfileForm, LoginForm,
    ChangePasswordForm, ShortCodeForm, RequestPasswordResetForm
)
from app import db, mail
from .models import User


# Blueprint Configuration
users_bp = Blueprint('users', __name__)


# Helper Functions
def send_email(subject, recipient, body):
    """Sends an email to the recipient with the specified subject and body."""
    msg = Message(subject, recipients=[
                  recipient], sender="donotreply@openvolunteer.com")
    msg.body = body
    mail.send(msg)


def generate_short_code():
    """Generates a random 6-digit short code for 2FA or password reset."""
    return str(randint(100000, 999999))


# Register User
@users_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    """Registers a new user"""
    form = RegisterUserForm()
    check_if_first_user = User.query.first()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('This email is already registered.', 'warning')
            return redirect(url_for('users.register_user'))
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            password_hash=generate_password_hash(form.password.data),
        )
        if check_if_first_user is None:
            user.role = "admin"
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html',
                           title='OpenVolunteer - Register',
                           form=form)


# Route - Login and send Short Code (2FA)
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Logs in a user and sends a short code (2FA) to their email"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login failed. Please check your email and password.',
                  'warning')
            return redirect(url_for('users.login'))
        if user.status == 'INACTIVE':
            flash('Your account is inactive. Please contact an administrator.',
                  'warning')
            return redirect(url_for('users.login'))
        short_code = generate_short_code()
        send_email('OpenVolunteer - Short Code for Login',
                   user.email, f'Your short code is: {short_code}')
        session['short_code'] = short_code
        session['user_id'] = user.id
        return redirect(url_for('users.enter_code'))
    return render_template('users/login.html', title='OpenVolunteer - Login',
                           form=form)


# Route - Enter Short Code (2FA)
@users_bp.route('/short_code', methods=['GET', 'POST'])
def enter_code():
    """Validates the short code (2FA) and completes the login process"""
    form = ShortCodeForm()
    if form.validate_on_submit():
        entered_code = form.short_code.data
        stored_code = session.get('short_code')
        if not stored_code:
            flash('No short code found. Please log in again.', 'warning')
            return redirect(url_for('users.login'))
        if entered_code == stored_code:
            return redirect(url_for('users.complete_login'))
        else:
            flash('Short Code (2FA) is incorrect. '
                  'Please try again.', 'warning')
    return render_template('users/short_code.html',
                           title='OpenVolunteer - Short Code (2FA)',
                           form=form)


# Route - Complete Login
@users_bp.route('/complete_login')
def complete_login():
    """Completes the login process if the short code (2FA) is correct"""
    # Variables
    stored_user_id = session.get('user_id')
    user = User.query.get_or_404(stored_user_id)
    # Log the user in
    if user:
        login_user(user)
        session.pop('short_code', None)
        next_page = request.args.get('next')
        if next_page is None or not next_page.startswith('/'):
            next_page = url_for('core.index')
        flash('Login successful.', 'success')
        return redirect(next_page)
    # If the user is not found, redirect to the login page
    flash('Login failed.', 'warning')
    return redirect(url_for('users.login'))


# Logout user
@users_bp.route('/logout')
@login_required
def logout():
    """Logs out a user"""
    logout_user()
    return redirect(url_for('core.index'))


# Route - User Account
@users_bp.route('/account/@<string:first_name>-<string:last_name>',
                methods=['GET', 'POST'])
@login_required
def user_profile(first_name, last_name):
    """Routes to a user's profile page. This is public."""
    user = User.query.filter_by(
        first_name=first_name,
        last_name=last_name).first_or_404()
    return render_template('users/account.html',
                           title='OpenVolunteer - Account',
                           user=user)


# Route - Edit User Account
@users_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Routes the current user to their profile page"""
    user = User.query.get_or_404(current_user.id)
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        user.updated_by = current_user.id
        user.updated_date = datetime.utcnow()
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('users.user_profile',
                                first_name=user.first_name,
                                last_name=user.last_name))
    return render_template('users/edit_profile.html',
                           title='OpenVolunteer - Edit Profile',
                           form=form, user=user)


# Route - Change Password
@users_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Allows the user to change their password"""
    user = User.query.get_or_404(current_user.id)
    if user != current_user:
        abort(403)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your password has been updated.', 'success')
        return redirect(url_for('users.user_profile',
                                first_name=user.first_name,
                                last_name=user.last_name))
    return render_template('users/change_password.html',
                           title='OpenVolunteer - Change Password',
                           form=form)


# Route - Forgot Password
@users_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Starts the password reset process by sending a short code."""
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            short_code = generate_short_code()
            send_email('OpenVolunteer - Short Code for Password Reset',
                       user.email,
                       f"You're receiving this email because you requested a password reset for your OpenVolunteer account.\nUse this short code to reset your password: {short_code}")
            session['short_code'] = short_code
            session['user_id'] = user.id
            flash(
                'An email has been sent to you with instructions to reset your password.',
                'success')
            return redirect(url_for('users.enter_reset_code'))
    return render_template('users/forgot_password.html',
                           title='OpenVolunteer - Forgot Password', form=form)


@users_bp.route('/enter_reset_code', methods=['GET', 'POST'])
def enter_reset_code():
    """Allows the user to enter the short code sent to their email."""
    form = ShortCodeForm()
    if form.validate_on_submit():
        if form.short_code.data == session.get('short_code'):
            return redirect(url_for('users.forgot_change_password'))
        else:
            flash('The code you entered is incorrect. Please try again.',
                  'warning')
    return render_template('users/forgot_password_reset_code.html',
                           title='OpenVolunteer - Reset Password', form=form)


@users_bp.route('/enter_change_password', methods=['GET', 'POST'])
def forgot_change_password():
    """Allows the user to change their password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.get(session.get('user_id'))
        user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your password has been updated.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/change_password.html',
                           title='OpenVolunteer - Change Password', form=form)
