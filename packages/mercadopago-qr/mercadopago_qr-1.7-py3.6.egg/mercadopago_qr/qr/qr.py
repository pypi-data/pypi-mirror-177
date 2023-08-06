from .. http.http import http
from .. http.server import server
from .. http.queries import queries
import qrcode
from io import BytesIO
import base64

import logging
_logger = logging.getLogger(__name__)

class qr:

    def __init__(self):
        _logger.warning("init qr code service...")

    def validate(self, data):
        if(len(data) > 0):
            return True
        return False

    def generate_qr_code(self, params={}):
        qr_request = queries()
        url = http(params['user_id'], params['external_pos_id'])

        endpoint = None
        if(bool(params['verify'])):
            endpoint = str(url.get_endpoint('unsecure_api')) + str(url.get_endpoint('qr'))            
        else:
            endpoint = str(url.get_endpoint('secure_api')) + str(url.get_endpoint('qr'))            
        
        mercadopago = server(client_secret=params['client_secret'])
        headers = qr_request.get_headers_qr(mercadopago)
        params['headers'] = headers
        params['url'] = endpoint
        response = qr_request.post(params)
        
        return response
    
    def get_qr_image_source(self, code):
        qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=20,
                            border=4,
                          )
        qr.add_data(code)
        qr.make(fit=True)
        img = qr.make_image()
        stream_out = BytesIO()
        img.save(stream_out, format="PNG")
        source = base64.b64encode(stream_out.getvalue())
        return str('data:image/png;base64,') + str(source.decode("utf-8"))