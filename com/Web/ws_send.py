from . import connected_sids, socketio


def send_message(data):
    for sid in connected_sids:
        socketio.emit('my_response', {'data': f'{data}'}, room=sid)