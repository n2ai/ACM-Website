from app import app, jwt
from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from app.forms import SignupForm, EmailError, LoginForm
import random
from app import db
from app.models import  UserPassword, UserAccount, Staff,TokenBlocklist
from flask_jwt_extended import create_access_token,jwt_required, get_jwt
from datetime import timedelta





with app.app_context():
    db.create_all()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None



@app.route('/')
def homepage():
    staff_members = Staff.query.limit(3).all()
    return render_template('homepage.html', staff_members=staff_members)

@app.route('/staff')
def staff():
    staff_members = Staff.query.limit(3).all()
    return render_template('staff.html', staff_members=staff_members)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # create a new user instance
        new_user = UserAccount(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            member_number = random.randrange(1000000, 9999999)
        )
        # add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # save the password in the UserPassword table
        new_password = UserPassword(
            email=form.email.data,
            password=form.password.data,
            user_account_id=new_user.member_number
        )
        db.session.add(new_password)
        db.session.commit()

        # flash a success message and redirect to index page
        flash('You have successfully signed up!')
        #return render_template('homepage.html', form=form) #images do not load with this?
        return redirect(url_for('homepage'))
    # if the email is already in the database, flash an error message
    elif form.email.errors == [EmailError.EMAIL_IN_DB.value]:
        flash(EmailError.EMAIL_IN_DB.value)
        return render_template('signup.html', form=form)
    
    # if the email is not a gator email, flash an error message
    elif form.email.errors == [EmailError.INVALID_EMAIL_DOMAIN.value]:
        flash(EmailError.INVALID_EMAIL_DOMAIN.value)
        #clrear the email field
        form.email.data = ''
        return render_template('signup.html', form=form)
    
    else:  
        return render_template('signup.html', form=form)
    
@app.route('/login', methods=["POST","GET"])
def login():
    
    form=LoginForm()
    if request.method == "POST":
        user = UserPassword.query.filter_by(email=form.email.data).first()
        if not user:
            return render_template('login.html',form=form)
        if user.password != form.password.data:
            return render_template('login.html',form=form)
        access_token = create_access_token(identity=form.email.data,expires_delta=timedelta(minutes=120)) # Creating a token stores user email that expires in 2 hours
        return make_response(jsonify(access_token=access_token))#return token for front-end
    else:
        return render_template('login.html', form=form)
        
        
    

@app.route("/logout", methods=["PUT"])
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    return make_response(jsonify(msg="Loged out"))#add an unvalid token to blocklist so it's no longer usable to access protected route


    



    


