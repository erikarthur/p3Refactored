

from webExample import app

import ssl, socket
import os

# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context = ssl.create_default_context(ssl.PROTOCOL_SSLv23)

cs_server_key = os.path.join(os.path.dirname(__file__), 'server.key')
cs_server_crt = os.path.join(os.path.dirname(__file__), 'server.crt')
context.load_cert_chain(certfile=cs_server_crt, keyfile=cs_server_key)


app.run(host='0.0.0.0', port=8000, debug=True, ssl_context=context)
