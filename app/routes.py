from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import SignupForm, EmailError
import random
from app import db
from app.models import  UserPassword, UserAccount, Staff, Trending, News, Events

with app.app_context():
    db.create_all()

"""
fake_events = [    {        'date': {'day': '26', 'month': 'Jun'},        'title': 'Robotathon',        'location': 'A300 UHD Main campus',        'contact_number': '0905136250',        'contact_email': 'longhai2511@gmail.com'    },
              {        'date': {'day': '27', 'month': 'Jun'},        'title': 'Hackathon',        'location': 'B200 UHD Main campus',        'contact_number': '0905136251',        'contact_email': 'longhai2512@gmail.com'    },    
              {        'date': {'day': '28', 'month': 'Jun'},        'title': 'CodeFest',        'location': 'C300 UHD Main campus',        'contact_number': '0905136252',        'contact_email': 'longhai2513@gmail.com'    }]

"""
fake_articles   =      [  {
            "title": "The Unbelievable Zombie Comeback of Analog Computing",
            "image_url": "	https://media.wired.com/photos/6423519d6881d9d60824b5ee/1:1/w_120,c_limit/Analog-web.jpg",
            "summary": "Computers have been digital for half a century. Why would anyone want to resurrect the clunkers of yesteryear.",
            "url": "https://www.wired.com/story/unbelievable-zombie-comeback-analog-computing/#intcid=_wired-verso-hp-trending_ab75f7c4-fe44-47b0-9921-220e251960de_popular4-1"
        },
        {
            "title": "New study finds link between coffee and longevity",
            "image_url": "	https://media.wired.com/photos/641e1cf44d133330b16…st-In-Space-Best-Netflix-Shows-Update-Culture.jpg",
            "summary": "From Naoki Urasawa’s Monster to Lost in Space, these are our picks for the best streaming titles to binge this week.",
            "url": "https://www.wired.com/story/netflix-best-shows-this-week/#intcid=_wired-verso-hp-trending_ab75f7c4-fe44-47b0-9921-220e251960de_popular4-1"
        },
        {
            "title": "Local community hosts fundraiser for animal shelter",
            "image_url": "	https://media.wired.com/photos/6414b4f0b19ad4e3186…:1/w_120,c_limit/0_TopArt_BVARGAS_Wrenches-14.jpg",
            "summary": "Six years ago, I moved my family into a 50-year-old RV—not just to see America, but to test my belief that anything worth fixing can be fixed. ",
            "url": "https://www.wired.com/story/vintage-van-home-repair-way-of-life/#intcid=_wired-verso-hp-trending_ab75f7c4-fe44-47b0-9921-220e251960de_popular4-1"
        }
    ]

@app.route('/')
def homepage():
    staff_members = Staff.query.limit(3).all()
    return render_template('homepage.html', staff_members=staff_members,events = fake_events, articles = fake_articles)

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


    


