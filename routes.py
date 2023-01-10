from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    request,
    jsonify
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError


from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app,db,login_manager,bcrypt
from models import User, Leaderboard, Userdata
from forms import login_form,register_form, vote_form, profile_form

def query_db():
    ulist = []
    users = User.query.all()
    for all in users:
        ulist.append((all.username, all.username.upper()))
    return ulist
def jsonify_votes():
    ulist = []
    users = Leaderboard.query.all()
    for all in users:
        ulist.append({
            "Username": all.username,
            "Votes": all.votes,
            "status": all.status
        })
    return ulist
def jsonify_userdata(username):
    userdata = {}
    users = Userdata.query.filter_by(username = username).first()
    userdata["firstname"] = users.firstname
    userdata["lastname"] = users.lastname
    userdata["address"] = users.address
    userdata["address2"] = users.address2
    userdata["city"] = users.city
    userdata["state"] = users.state
    userdata["zip"] = users.zip
    return userdata

def jsonify_alldata():
    ulist = []
    users = Leaderboard.query.all()
    for all in users:
        userdata = User.query.filter_by(username=all.username).first()
        ulist.append({
            "Username": all.username,
            "Votes": all.votes,
            "Status": all.status,
            "Token": userdata.token,
            "Bio": "bio"
        })
    return ulist

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def index():
    logged_in_user = session['username']
    user = User.query.filter_by(username=logged_in_user).first()
    # user = db.session.execut(db.select(User).filter_by(email="1@gmail.com")).first()
    return render_template("index.html",title="Home", username=logged_in_user, user_email=user.email)


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                session['username'] = user.username
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("page-login.html",
        form=form,
        text="Login",
        title="Login",
        btn_action="Login"
        )
        
# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data
            token = form.token.data
            
            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd).decode('utf-8'),
                token=token
            )
            newuserdata = Userdata(
                username = username
            )
            new_voter = Leaderboard(
            username = username,
            votes = 0,
            status = False
            )
            db.session.add(new_voter)
            db.session.add(newuser)
            db.session.add(newuserdata)
            db.session.commit()
            flash(f"Account Succesfully created", "success")

            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User credentials already used!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template("page-register.html",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Register account"
        )

@app.route("/profile", methods=("GET", "POST"), strict_slashes=False)
@login_required
def profile():
    active_user = session['username']
    userdata = jsonify_userdata(username=active_user)

    form = profile_form()
    if form.validate_on_submit():
        updated = Userdata(
            username = session['username'],
            firstname = form.firstname.data,
            lastname = form.lastname.data,
            address = form.address.data,
            address2 = form.address2.data,
            city = form.city.data,
            state = form.state.data,
            zip = form.zip.data
        )
        db.session.add(updated)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('app-profile.html', form=form, userdata=userdata)





@app.route("/vote", methods=("GET", "POST"), strict_slashes=False)
@login_required
def vote(voted=False):
    form = vote_form()
    form.voted.choices = query_db()
    if request.method == 'POST':
        return redirect(url_for('castvote', user=form.voted.data))

    return render_template('vote_area.html',
    form = form,
    users= query_db(),
    error= voted )


@app.route("/castedvotes/<user>", methods=("GET","POST"), strict_slashes=False)
@login_required
def castvote(user):
    voter = session['username']
    vote_validity = Leaderboard.query.filter_by(username = voter).first()
    if vote_validity.status == True:
        return redirect(url_for('vote', error=True))

    votes_count = Leaderboard.query.filter_by(username = user).first()
    if votes_count.username == user:
        #increment vote count
        votes_count.votes += 1
        #update record of voting status
        vote_validity.status = True
        db.session.commit()
        return redirect(url_for('results'))
    return redirect(url_for('index'))


@app.route("/results")
def results():
    data = jsonify_votes()
    return render_template(
        'test.html',
        data=data
    )

@app.route("/admin")
@login_required
def admin():
    test = jsonify_alldata()
    return render_template(
        'adminCandidateDetails.html',
        data=test
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




@app.errorhandler(400)
def page_not_found(error):
    return render_template('page-error-400.html'), 400
@app.errorhandler(403)
def page_not_found(error):
    return render_template('page-error-403.html'), 403
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page-error-404.html'), 404
@app.errorhandler(500)
def page_not_found(error):
    return render_template('page-error-500.html'), 500
@app.errorhandler(503)
def page_not_found(error):
    return render_template('page-error-503.html'), 503


if __name__ == "__main__":
    app.run(debug=True)
