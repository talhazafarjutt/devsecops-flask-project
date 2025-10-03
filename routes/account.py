import json
from base64 import b64encode, b64decode
from uuid import uuid4

from bcrypt import gensalt, hashpw
from flask_login import login_required, current_user
from flask import redirect, flash, render_template, request, Response, g, make_response

from app import app
from models import Session, Note
from forms.image_form import ImageForm
from forms.account_form import AccountForm
from utils.profile_image import get_base64_image_blob
from utils.input_sanitizer import sanitize_text_field


@app.route('/account')
@login_required
def account():
    return render_template('account.html', uuid=str(uuid4()))


@app.route('/search')
@login_required
def search():
    search_param = request.args.get('search', '')
    search_param = sanitize_text_field(search_param, 100)  # Limit to 100 chars

    with Session() as session:
        session.query(Note)

        personal_notes = session.query(Note).filter(
            Note.user_id == current_user.id,
            Note.text.like(f"%{search_param}%")).all()
        return render_template(
            'search.html',
            search=search_param,
            personal_notes=personal_notes,
        )


@app.route('/accounts/<int:user_id>/notes')
@login_required
def get_personal_notes(user_id: int):
    with Session() as session:
        personal_notes = session.query(Note).filter(
            Note.user_id == user_id).all()
        return render_template('personal_notes.html',
                               personal_notes=personal_notes)


@app.route('/account/image', methods=['POST'])
@login_required
def add_image():
    form = ImageForm(request.form)

    if not form.validate():
        flash(json.dumps(form.errors), 'error')
    else:
        try:
            with Session() as session:
                current_user.profile_image = get_base64_image_blob(
                    form.url.data).encode()
                session.merge(current_user)
                session.commit()
                flash('Profile image updated', 'success')
        except Exception as e:
            flash(f'Error updating profile image: {str(e)}', 'error')

    return redirect('/account')


@app.route('/account', methods=['POST'])
def update_account():
    form = AccountForm(request.form)

    if not form.validate():
        flash(json.dumps(form.errors), 'error')
    else:
        with Session() as session:
            if form.email.data:
                try:
                    form.email.data = sanitize_text_field(form.email.data, 255)
                except ValueError:
                    flash('Invalid email format', 'error')
                    return redirect('/account')

            filtered_values = {
                key: value
                for key, value in form.data.items()
                if value is not None and key != 'password'
            }
            current_user.__dict__.update(filtered_values)

            new_password = form.password.data
            was_password_changed = new_password is not None and new_password != filtered_values.get(
                'password_control')

            if was_password_changed:
                # Sanitize password (basic check)
                if len(new_password) < 8:
                    flash('Password must be at least 8 characters long', 'error')
                    return redirect('/account')
                current_user.password = hashpw(new_password.encode(),
                                               gensalt()).decode()

            session.merge(current_user)
            session.commit()
            flash('Account updated', 'success')

    return redirect('/account')


@app.route('/darkmode', methods=['POST'])
def toggle_darkmode():
    response = make_response(redirect('/account'))

    preferences = g.preferences
    preferences['mode'] = 'light' if preferences['mode'] == 'dark' else 'dark'

    try:
        preferences_json = json.dumps(preferences)
        encoded_preferences = b64encode(preferences_json.encode('utf-8')).decode()
        response.set_cookie('preferences', encoded_preferences, secure=True, samesite='Strict', httponly=True)
    except (TypeError, json.JSONEncodeError):
        response.set_cookie('preferences', 'light', secure=True, samesite='Strict', httponly=True)
    return response


default_preferences = {'mode': 'light'}


@app.before_request
def before_request():
    preferences_cookie = request.cookies.get('preferences')
    
    if preferences_cookie is None:
        preferences = default_preferences
    else:
        try:
            decoded_data = b64decode(preferences_cookie).decode('utf-8')
            parsed_prefs = json.loads(decoded_data)
            preferences = parsed_prefs if (isinstance(parsed_prefs, dict) and parsed_prefs.get('mode') in ('light', 'dark')) else default_preferences
        except ValueError:
            preferences = default_preferences

    g.preferences = preferences


@app.after_request
def after_request(response: Response) -> Response:
    if request.cookies.get('preferences') is None:
        response.set_cookie('preferences', 'light', secure=True, samesite='Strict', httponly=True)
    return response
