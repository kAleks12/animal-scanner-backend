import logging
import os.path
import sys
from configparser import ConfigParser


class ConfigParserWrapper:
    def __init__(self):
        self.logger = logging.getLogger('ConfigParser')
        self.parser = ConfigParser()

        if not os.path.isfile(sys.argv[1]):
            self.logger.error('Config file not found')
            raise FileNotFoundError('Config file not found')

        self.parser.read(sys.argv[1])
        self.logger.info('Config file loaded')

    def get_attr(self, section, option):
        self.logger.debug(f'Getting attribute {option} from section {section}')
        return self.parser.get(section, option)


parser = ConfigParserWrapper()