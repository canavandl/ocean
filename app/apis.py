from app import app
from flask.ext.restful import Resource, Api

from sts.sts_interface import (SocketClient,
                               STS_INTERFACE,
                               DAEMON_CONSTANTS,
                               create_sts_command)

api = Api(app)


def send_and_recv(message, **args):
    """
    things and stuff
    """
    socketclient = SocketClient(DAEMON_CONSTANTS.get('hostname'),
                                DAEMON_CONSTANTS.get('port'))
    socketclient.send_message(create_sts_command(message, args))
    if args:
        response = socketclient.receive_message()
    else:
        response = None
    socketclient.close_connection()
    return response


class AcquireSpectrum(Resource):
    def post(self):
        values = send_and_recv(STS_INTERFACE.get('get_spectrum'))
        for c in values: print(c)
        return "200"

class AcquireWavelengths(Resource):
    def post(self):
        message = create_sts_command(STS_INTERFACE.get('get_wavelengths'))
        socketclient = SocketClient(DAEMON_CONSTANTS.get(hostname),
                                    DAEMON_CONSTANTS.get(port))
        socketclient.send_message(message)
        wavelengths = socketclient.receive_message()
        socketclient.close_connection()
        return wavelengths


api.add_resource(AcquireSpectrum, '/api/acquire_spectrum')
api.add_resource(AcquireWavelengths, '/api/acquire_wavelengths')
