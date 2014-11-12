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
    if not args:
        response = socketclient.receive_message()
    else:
        response = "200"
    socketclient.close_connection()
    return response


class AcquireSpectrum(Resource):
    def post(self):
        values = send_and_recv(STS_INTERFACE.get('get_spectrum'))
        response = values[6:-1].split()
        return response

class AcquireWavelengths(Resource):
    def post(self):
        wavelenghts = send_and_recv(STS_INTERFACE('get_wavelengths'))
        response = values[5:]
        return response


api.add_resource(AcquireSpectrum, '/api/acquire_spectrum')
api.add_resource(AcquireWavelengths, '/api/acquire_wavelengths')
