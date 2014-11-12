from app import app
from flask.ext.restful import Resource, Api

from sts.sts_interface import (SocketClient,
                               STS_INTERFACE,
                               create_sts_command)

api = Api(app)


class Settings(Resource):
    """
    Class about STS settings
    blah blah blah
    """
    def get(self):
        raise NotImplementedError
    def post(self):
        raise NotImplementedError


class AcquireSpectrum(Resource):
    def get(self):
        message = create_sts_command(STS_INTERFACE.get('get_spectrum'))
        socketclient = SocketClient(DAEMON_CONSTANTS.get(hostname),
                                    DAEMON_CONSTANTS.get(port))
        socketclient.send_message(message)
        values = socketclient.receive_message()
        return values



api.add_resource(AcquireSpectrum, '/api/acquire_spectrum')