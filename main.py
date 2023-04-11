from flask import Flask, render_template, request, redirect
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

    if id_token:
        try:
            # verify id token
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

            # get user data
            user_data = my_user.get_user(claims)
            if user_data == None:
                my_user.create_user(claims)
                user_data = my_user.get_user(claims)

            # update username
            # if claims['name']:
            #     my_user.update_username(claims)

            # create a default calendar called personal.
            # pprint('claims')
            # pprint(claims)
            # pprint('user_data')
            # pprint(user_data)

            if len(user_data['calendar_ids']) < 1:
                id = my_calendar.create_calendar('personal')
                my_calendar.add_calendar_to_user(user_data, id)
                user_data = my_user.get_user(claims)

            # read from the default calendar
            # get calendars and events for the next seven days

            if len(user_data['calendar_ids']):
                calendars = my_calendar.get_calendars_from_user(user_data)

        except ValueError as exc:
            error_message = str(exc)
    return render_template('index.html', claims=claims, error_message=error_message, user_data=user_data, calendars=calendars)


@app.route('/create_calendar', methods=['POST'])
def create_calendar():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    user_data = None

    if id_token:
        try:
            # verify id token
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

            # get user data
            user_data = my_user.get_user(claims)
        
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


# start here. create event route
@app.route('/create_event', methods=['POST'])
def create_event():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    user_data = None
    calendars = None

    if id_token:
        try:
            # verify id token
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

            # get user data
            user_data = my_user.get_user(claims)

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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
