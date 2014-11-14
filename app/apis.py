from app import app
from flask.ext.restful import Resource, Api

from sts import (
    SocketClient,
    STS_INTERFACE,
    DAEMON_CONSTANTS,
    create_sts_command)

api = Api(app)


def send_sts_query(message, **args):
    """
    Helper function for get and set commands for STS
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
    """
    API endpoint to read spectrum from sts
    """
    def post(self):
        values = send_sts_query(STS_INTERFACE.get('get_spectrum'))
        response = values[6:-1].split()
        return response


class AcquireWavelengths(Resource):
    """
    API endpoint to read wavelengths from STS
    """
    def post(self):
        wavelengths = send_sts_query(STS_INTERFACE.get('get_wavelengths'))
        response = wavelengths[6:-1].split()
        return response


api.add_resource(AcquireSpectrum, '/api/acquire_spectrum')
api.add_resource(AcquireWavelengths, '/api/acquire_wavelengths')
