"""Users > Views"""

# Imports
from random import randint
from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session,
)
from werkzeug.security import generate_password_hash
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_mail import Message
from users.forms import (
    RegisterUserForm,
    LoginForm,
    ChangePasswordForm,
    ShortCodeForm,
)
from app import db, mail
from .models import User


# Blueprint Configuration
users_bp = Blueprint('users', __name__)


# Register User
@users_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    """Registers a new user"""

    form = RegisterUserForm()

    check_if_first_user = User.query.first()

    if form.validate_on_submit():
        # Check if email is already registered
        if User.query.filter_by(email=form.email.data).first():
            flash('This email is already registered.', 'warning')
            return redirect(url_for('users.register_user'))

        # Commit the new user to the database
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

        if user is None:
            flash('Login failed. Please check your email and password.',
                  'warning')
            return redirect(url_for('users.login'))

        elif user.check_password(form.password.data) and user is not None:
            # Check user's status
            if user.status == 'INACTIVE':
                flash(
                    """Your account is inactive.
                    Please contact an administrator.""",
                    'warning')
                return redirect(url_for('users.login'))

            # Generate a short code to complete the login process
            short_code = str(randint(100000, 999999))

            # Send the short code to the user's email
            msg = Message(
                'OpenVolunteer - Short Code for Login',
                recipients=[user.email],
                sender="noreply-2FA@openvolunteer.com")
            msg.body = f'Your short code is: {short_code}'
            mail.send(msg)

            # Store the short code in the session
            session['short_code'] = short_code
            # After generating the short code and sending the email
            session['user_id'] = user.id

            # Redirect the user to the short code page
            return redirect(url_for('users.enter_code'))

    return render_template('users/login.html',
                           title='OpenVolunteer - Login',
                           form=form)


# Route - Enter Short Code (2FA)
@users_bp.route('/short_code', methods=['GET', 'POST'])
def enter_code():
    """Validates the short code (2FA) and completes the login process"""

    form = ShortCodeForm()

    if form.validate_on_submit():
        # Variables
        entered_code = form.short_code.data
        stored_code = session.get('short_code')

        # Check if the entered code matches the stored code
        if entered_code == stored_code:
            flash('Short Code (2FA) is correct. Completing login.', 'success')
            return redirect(url_for('users.complete_login'))
        else:
            flash('Short Code (2FA) is incorrect. Please try again.',
                  'warning')

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
    '''Logs out a user'''

    logout_user()
    return redirect(url_for('core.index'))


# Route - User Account
@users_bp.route('/account/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_profile(user_id):
    """Routes the current user to their profile page"""

    user = User.query.get_or_404(user_id)

    if user != current_user:
        abort(403)

    return render_template('users/account.html',
                           title='OpenVolunteer - Account',
                           user=user)


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
        return redirect(url_for('users.user_profile', user_id=user.id))

    return render_template('users/change_password.html',
                           title='OpenVolunteer - Change Password',
                           form=form)
