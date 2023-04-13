from flask import Flask, render_template, request, redirect, session
from google.cloud import datastore
from google.auth.transport import requests
from pprint import pprint
import datetime
import google.oauth2.id_token


# import custom classes
from user import User
from mycalendar import MyCalendar
from event import Event

# instantiate objects
app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

# instantiate objects from custom classes
my_user = User()
my_calendar = MyCalendar()
my_event = Event()


@app.route('/')
def root():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    user_data = None
    calendars = None
    personal_events = None

    if id_token:
        try:
            # verify id token
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

            # get user data
            user_data = my_user.get_user(claims)

            # store user data in session
            session['user_data'] = user_data

            pprint(session)

            if user_data == None:
                my_user.create_user(claims)
                user_data = my_user.get_user(claims)

            # update username
            # if claims['name']:
            #     my_user.update_username(claims)

            
            # create a default personal calendar
            if len(user_data['calendar_ids']) < 1:
                id = my_calendar.create_calendar('personal')
                my_calendar.add_calendar_to_user(user_data, id)
                user_data = my_user.get_user(claims)

            # get calendars
            if len(user_data['calendar_ids']):
                calendars = my_calendar.get_calendars_from_user(user_data)
                
            # Get personal events from the default personal calendar
            for calendar in calendars:
                if calendar['name'] == 'personal':
                    personal_events = my_event.get_personal_events(calendar['event_ids'])

        except ValueError as exc:
            error_message = str(exc)
    return render_template(
        'index.html', 
        claims=claims, 
        error_message=error_message, 
        user_data=user_data, 
        calendars=calendars,
        personal_events=personal_events)



@app.route('/create_calendar', methods=['POST'])
def create_calendar():
    error_message = None
    user_data = None

    try:
        # get user data
        user_data = session['user_data']
    
        # get calendar name from form
        # make sure to validate user input
        calendar_name = request.form['calendar_name']

        # create calendar
        id = my_calendar.create_calendar(calendar_name)

        # add the created calendar to the current user
        my_calendar.add_calendar_to_user(user_data, id)

    except ValueError as exc:
        error_message = str(exc)

    return redirect('/')

@app.route('/update_calendar_form', methods=['POST'])
def update_calendar_form():
    id_token = request.cookies.get("token")
    error_message = None
    user_data = None

    if id_token:
        try:
            # get user data
            user_data = session['user_data']

            # fetch calendars
            calendar_list = my_calendar.get_calendars_from_user(user_data)
            pprint(calendar_list)

        except ValueError as exc:
            error_message = str(exc)

    return render_template('update_calendar_form.html', user_data=user_data, calendars=calendar_list)

@app.route('/update_calendar', methods=['POST'])
def update_calendar():
    id_token = request.cookies.get("token")
    error_message = None
    
    if id_token:
        try:
            # get user data
            user_data = session['user_data']

            # get form data
            # validate form data
            current_name = request.form['current_name']
            new_calendar_name = request.form['new_calendar_name']

            # fetch calendars
            calendar_list = my_calendar.get_calendars_from_user(user_data)
    
            # update calendar entity
            for calendar in calendar_list:
                if calendar['name'] == current_name:
                    my_calendar.update_calendar_name(calendar, new_calendar_name)
                    
        except ValueError as exc:
            error_message = str(exc)

    return redirect('/')


@app.route('/create_event', methods=['POST'])
def create_event():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    user_data = None
    calendars = None

    if id_token:
        try:
            # get user data
            user_data = session['user_data']

            # get event details from the form
            # make sure to validate user input
            event_name = request.form['event_name']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            event_notes = request.form['event_notes']
            calendar_name = request.form['calendar_name']
            
            # create event
            event_id = my_event.create_event(
                event_name, start_time, end_time, event_notes)

            # add avent to calendar
            calendar_list = my_calendar.get_calendars_from_user(user_data)
            for calendar in calendar_list:
                if calendar['name'] == calendar_name:
                    # my_event.add_event_to_calendar(calendar, id)
                    my_calendar.update_calendar(calendar, event_id)

        except ValueError as exc:
            error_message = str(exc)

    return redirect('/')


@app.route('/update_event_form/<int:event_id>', methods=['POST'])
def update_event_form(event_id):
    error_message = None
    user_data = None
    calendars = None

    try:
        # get event entity
        event_entity = my_event.get_event_entity(event_id)            
    except ValueError as exc:
        error_message = str(exc)

    return render_template('update_event_form.html', user_data=user_data, event=event_entity)


@app.route('/update_event/<int:event_id>', methods=['POST'])
def update_event(event_id):
    error_message = None

    try:
        # get form data
        # validate form data
        name = request.form['event_name']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        notes = request.form['event_notes']

        # update event entity 
        my_event.update_event_entity(event_id, name, start_time, end_time, notes)
    
    except ValueError as exc:
        error_message = str(exc)
    
    return redirect('/')



@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    error_message = None
    user_data = None
    calendars = None

    try:
        # get user data
        user_data = session['user_data']

        # get all calendars
        calendars = my_calendar.get_calendars_from_user(user_data)

        # get personal calendar
        for calendar in calendars:
            if calendar['name'] == 'personal':
                calendar_entity = calendar
        
        # delete event entity
        my_event.delete_event(event_id)

        # delete event id from calendar event_ids
        my_calendar.delete_event_id(calendar_entity, event_id)

    except ValueError as exc:
        error_message = str(exc)

    return redirect('/')
# start here, delete entity, from event list



@app.route('/secondary_calendar')
def secondary_calendar():
    pass

@app.route('/share_calendar')
def share_calendar():
    pass

@app.route('/shared_calendar')
def shared_calendar():
    pass

@app.route('/remove_user')
def remove_user():
    pass



    


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='127.0.0.1', port=8080, debug=True)
