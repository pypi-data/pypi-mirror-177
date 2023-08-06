from asyncio.log import logger
import socketio
from typing import Any
import logging
import base64

sio = socketio.Client()

# {'task_id' : str, 'struct' : dict}
task_id = ''
# target log for where intercepted logs should be forwarded to
logging_target = {'element_key' : 'Logs'}

def safe_emit(event, data):
    try:
        sio.emit(event, data)
    except:
        pass

def connect(HOST : str = 'localhost', PORT : str = '8000') -> None:
    sio.connect('http://' + HOST + ':' + PORT, headers={'type':'app'})
    print(f'sid is {sio.sid}')

def disconnect() -> None:
    sio.disconnect()
    print('socket disconnected')

# struct: { 'name' : 'type' }
# send a new task to be added to the server's task manager
def set_task_id(id : str) -> None:
    global task_id
    task_id = id

# edit one of the elements in the task, this allows data updating
def edit_element(element_uid : str, value : Any) -> None:
    ''' images must be base 64 encoded '''
    safe_emit('edit_element', {'task_id' : task_id, 'element_key' : element_uid, 'value' : value})

# mark the task as completed
def deactivate_task(task_id : str) -> None:
    safe_emit('deactivate_task', task_id)

def notify(txt : str, type : str) -> None:
    safe_emit('notify', {'txt':txt, 'type':type})

def logging_intercept(msg) -> None:
    edit_element(logging_target['element_key'],msg)

# http://naoko.github.io/intercept-python-logging/
class RequestHandler(logging.Handler):
    def emit(self, record):
        ''' Intercept logs '''
        logging_intercept(record.getMessage())

#@sio.on('connect')
#def on_connect():
#    global current_task
#    # when a server connects it is pushed the current task structure, if this already exists on the server that's ok - the server should ignore
#    # a request to create a task with a duplicate id
#    if current_task != {'task_id':''}:
#        safe_emit('create_task', current_task)





