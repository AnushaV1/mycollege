import os,json

from flask import Flask, render_template, request, flash, redirect, session, g, url_for,jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import ImmutableMultiDict
from forms import UserAddForm, LoginForm, EditForm, DeleteForm,EditNotesForm
from models import db, connect_db, User, Tag, UserFavorite, UserCollegeTag
from login_decorator import login_required
from api_response import sendRequest,sendSingleCollegeRequest

CURR_USER_KEY = "curr_user"

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///college_search'))

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "search_my_college")
toolbar = DebugToolbarExtension(app)

connect_db(app)


db.create_all()


##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        
    else:
        g.user = None

    
    g.tags = Tag.query.all()
    
def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """ Handle user signup. """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username= form.username.data,
                password= form.password.data,
                email= form.email.data,
                )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('user/signup.html', form=form)
        
        flash("Welcome to My College App!",'success')
        return redirect("/login")

    else:
        return render_template('user/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials. Please try again", "danger")

    return render_template('user/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout() 
    
    flash("You are successfully logged out", "info")
    return redirect(url_for("login"))


##############################################################################
@app.route('/user/profile', methods=["GET", "POST"])
@login_required
def profile():
    """Update profile for current user."""

    profile = g.user
    form = EditForm(obj=profile)
    
    if form.validate_on_submit():
        if User.authenticate(profile.username, form.password.data):
            profile.username = form.username.data
            profile.email = form.email.data
            profile.first_name = form.first_name.data
            profile.last_name = form.last_name.data
            db.session.commit()
            flash("Profile updated successfully", "success")
            return redirect(url_for("homepage"))
            
        flash("Wrong password try again", "danger")
    return render_template("/user/edit_profile.html", form=form, user_id = profile.id)



@app.route('/user/search')
@login_required
def user_search_form():
    """ Render college search form for user """
    return render_template("/user/college_search_form.html")

@app.route("/api/get-college")
@login_required
def get_college():
    """ Render college search results """
    search_data = request.args
    response = sendRequest(search_data)
    return jsonify(response)
    
############## Get single college info from API ########
@app.route("/api/show-college")
@login_required
def show_college_details():
    """ Show college details for selected college id """
    collegeID = request.args.to_dict()
    single_college_response = sendSingleCollegeRequest(collegeID)
    return single_college_response
    

@app.route("/api/add-notes", methods=["POST"])
@login_required
def add_notes():
    """ Add notes for user's college  """
    get_notes_id = request.json
    id = get_notes_id['id']
    fav = UserFavorite.query.get_or_404(id)
    fav.notes = get_notes_id['notes']
    db.session.commit()
    return jsonify(fav.notes) 

    
@app.route("/api/edit-notes", methods=["POST"])
@login_required
def edit_notes():
    """edit notes for user's college  """
    edit_notes_id = request.json
    id = edit_notes_id['id']
    favorites = UserFavorite.query.filter_by(id=id).one()
    form = EditForm(obj=favorites)
    favorites.notes = edit_notes_id['notes']
    db.session.commit()
    return jsonify(favorites.notes)     

@app.route("/api/add-tags", methods=["POST"])
@login_required
def add_tags():
    """ Add tags for user's college id """
    get_tags_id = request.json
    user_fav_id = get_tags_id['user_fav_id']
    tag_id = get_tags_id['tag_id']
    college_tags = UserCollegeTag.query.filter_by(user_favorite_id=user_fav_id,tag_id = tag_id).first()
    if college_tags is None:
        user_college_tags = UserCollegeTag(user_favorite_id=user_fav_id,tag_id = tag_id)
        db.session.add(user_college_tags)
        db.session.commit()
        tag = Tag.query.get_or_404(tag_id)
        return jsonify(tag.tag_name)
        
    else:    
        return jsonify("Already exists")


#######################User Shortlist ##################
@app.route('/user/shortlist')
@login_required
def shortlist():
    """ Add college id to user's favorite """
    college_values = request.args.to_dict()
    
    college_name = college_values["college_name"]
    college_id = college_values["college_id"]
    id = int(college_id)
    
    college_id = UserFavorite.query.filter_by(user_id = g.user.id, college_id=id).first()
    user_favorites = g.user.favorites
    
    if college_id is None:
        favorite_college = UserFavorite(user_id = g.user.id, college_id=id, college_name=college_name)
        db.session.add(favorite_college)
        db.session.commit()
        flash("Shortlisted", 'info')

    elif college_id in user_favorites:
    
        flash("Already shortlisted", 'info')
    
    return jsonify({"result": "shortlisted"})

########### Delete / Remove from shortlist #############
@app.route("/user/<int:fav_id>/delete/", methods=["POST"])
@login_required
def remove_from_shortlist(fav_id):
    """ Remove unfavorited college id from table """
    unfavorite_id = UserFavorite.query.get_or_404(fav_id)
    
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(unfavorite_id) 
        db.session.commit()

    return redirect(url_for("homepage"))


@app.route('/user/tags')
@login_required
def user_college_tags():
    """Show user's tags on colleges  """
    if g.user:
        user_favorite = [fav for fav in g.user.favorites]
            
        return render_template('/user/tags.html', favorites=user_favorite,  alltags= g.tags)

    else:
        return render_template('home-anon.html')
##############################################################################
@app.route('/')
def homepage():
    """Show homepage:  """
    if g.user:
        user_favorite = [fav for fav in g.user.favorites]
    
        form = DeleteForm() 

        return render_template('home.html', favorites = user_favorite, form=form, tags= g.tags)

    else:
        return render_template('home-anon.html')
        
    
@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404


@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
