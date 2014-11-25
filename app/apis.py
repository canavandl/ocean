from flask import request
from flask.ext.restful import (Resource,
                               Api)

from colour import (SpectralPowerDistribution,
                    spectral_to_XYZ,
                    CMFS)

from app import app
from sts import (STS_INTERFACE,
                 SocketClient,
                 send_sts_command)

api = Api(app)


class AcquireSpectrum(Resource):
    """
    API endpoint to read spectrum from sts
    """
    def post(self):
        values = send_sts_command(SocketClient(),
                                  STS_INTERFACE.get('get_spectrum'))
        response = [float(i) for i in values[6:-1].split()]
        return response


class AcquireWavelengths(Resource):
    """
    API endpoint to read wavelengths from STS
    """
    def post(self):
        wavelengths = send_sts_command(SocketClient(),
                                       STS_INTERFACE.get('get_wavelengths'))
        response = [float(i) for i in wavelengths[6:-1].split()]
        return response


class ColourCalculation(Resource):
    def post(self):
        data = request.json
        data = dict(zip(data['wavelengths'], data['values']))
        spd = SpectralPowerDistribution('spd', data)
        cmfs = CMFS.get('CIE 1931 2 Degree Standard Observer')
        return spectral_to_XYZ(spd, cmfs).tolist()


class OceanSettings(Resource):
    def get(self):


api.add_resource(AcquireSpectrum, '/api/acquire_spectrum')
api.add_resource(AcquireWavelengths, '/api/acquire_wavelengths')
api.add_resource(ColourCalculation, '/api/colour_calculation')

