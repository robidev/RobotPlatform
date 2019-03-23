#!/usr/bin/env python

#layoutit.com for layout-wise controls

from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

led1 = 0
led2 = 0
connected = 0

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        #socketio.emit('my_response',
        #              {'data': 'Server generated event', 'count': count},
        #              namespace='/test')

        #time.sleep(.7)
        response = genericresponse()		
        socketio.emit('serverUpdate', response, namespace='/test')
		
def genericresponse():
    dateStr = "31/01/18"
    timeStr = "13:33:40"

    resp = {}
    resp['date'] = dateStr
    resp['time'] = timeStr
    resp['spinnerStarted'] = connected
    resp['sessionID'] = 42

    resp['send'] = 2
    resp['received'] = 0

    resp['led1On'] = led1
    resp['led2On'] = led2

    print('led1=%i',led1)
    print('led2=%i',led2)

    return resp

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('ledButtonID', namespace='/test') #namespace=namespace)
def ledButton(msg):
    global led1
    global led2
    led = msg['led']
    on = msg['on']
    #print 'ledButton()', led, on
    if led == 1:
        led1 = on
        print('led1=%i',led1)
    elif led == 2:
        led2 = on
        print('led2=%i',led2)
    response = genericresponse()		
    emit('serverUpdate', response, namespace='/test')


@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.on('connect', namespace='/test')
def test_connect():
    global connected
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    connected = 1;
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    global connected
    connected = 0;
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)