#crud databse commands here
from flask import jsonify, request, render_template, flash, redirect, url_for

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
    #return jsonify({'message': 'Event created successfully!'})
    
    return redirect(url_for('get_events'))

@app.route('/UPDATE', methods=['POST'])
def update_event():
    #template form read
    title = request.form['title']
    new_title = request.form['new_title']
    summary = request.form['summary']
    presenter = request.form['presenter']
    place = request.form['place']
    time = request.form['time']
    date = request.form['date']

    # Check if the event exists
    event = Events.query.filter_by(title=title).first()
    if not event:
        flash('Event not found!')
        return redirect(url_for('get_events'))

    #save variables to data columns
    event.title = new_title
    event.summary = summary
    event.presenter = presenter
    event.place = place
    event.time = time
    event.date = date
    db.session.commit()

    # Redirect the user back to the events page
    return redirect(url_for('get_events'))


# load all events into website
@app.route('/events', methods=['GET'])
def get_events():
    events = Events.query.all()
    return render_template('panel.html', events=events)


# Define a route to handle the DELETE request method for '/events'
@app.route('/DEL', methods=['POST'])
def delete_event():
    # Get the event to be deleted from the database
    title = request.form['title']
    todel = Events.query.filter_by(title=title).first()

    # If the event does not exist, return a 404 error
    if todel is None:
        return jsonify({'error': 'Event not found.'}), 404

    # Delete the event from the database
    db.session.delete(todel)
    db.session.commit()
    # Return a response indicating that the event was deleted successfully
    #return jsonify({'message': f'Event {title} deleted successfully.'}), 200
    return redirect(url_for('get_events'))



