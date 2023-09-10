import logging
import logging.config
import os.path
import sys

import uvicorn

from src.database.database import db_provider
from src.server.server import Server
from src.utils.config_parser import parser


if not os.path.isfile(sys.argv[2]):
    print('Logging config file not found')
    raise FileNotFoundError('Logging config file not found')
logging.config.fileConfig(sys.argv[2], disable_existing_loggers=False)


class Main:
    def __init__(self):
        self.logger = logging.getLogger('Main')
        self.server = Server()
        self.server.prepare()
        self.server.app.add_event_handler("shutdown", self.shutdown_event_handler)
        self.server.wrap_cors()

    def shutdown_event_handler(self):
        self.logger.info('Shutting down')
        db_provider.close_connection()
        self.logger.info('Shutting down')


if __name__ == '__main__':
    host = parser.get_attr('server', 'host')
    port = parser.get_attr('server', 'port')
    main = Main()
    uvicorn.run(app=main.server.app, host=host, port=port, log_config=None, lifespan='on')
