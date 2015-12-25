import gevent.monkey; gevent.monkey.patch_all()

import bottle
import httplib
import logging

app = bottle.Bottle()

log = logging.getLogger(__name__)


@app.get('/health')
def health_check():
    """
    Health check endpoint
    """
    return {'OK': 1}

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        server='gevent'
    )
