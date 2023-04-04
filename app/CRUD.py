#crud databse commands here
from flask import jsonify, request, render_template

from app import app, db
from app.models import Events

#event CRUD commands
# Create a new event

@app.route('/events', methods=['POST'])
def create_event():
    title = request.form['title']
    summary = request.form['summary']
    presenter = request.form['presenter']
    place = request.form['place']
    time = request.form['time']
    date = request.form['date']
    event = Events(title=title, summary=summary, presenter=presenter, place=place, time=time, date=date)
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully!'})

# load all events into website
@app.route('/events', methods=['GET'])
def get_events():
    events = Events.query.all()
    return render_template('admin.html', events=events)



