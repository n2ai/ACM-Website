from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import SignupForm, EmailError
import random
from app import db
from app.models import  UserPassword, UserAccount, Staff, Trending, News

with app.app_context():
    db.create_all()

@app.route('/')
def homepage():
    staff_members = Staff.query.limit(3).all()
    news = News.query.limit(5).all()
    trending = Trending.query.limit(5).all()
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


    


