import logging
import configparser
import os


_proj_root = os.path.dirname(os.path.realpath(__file__))

confpars = configparser.SafeConfigParser()
confpars.read(os.path.join(_proj_root, 'conf.ini'))
confpars['main']['proj_root'] = _proj_root

logging_format = "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s"
logging.basicConfig(format=logging_format)
if confpars['main']['logging_level'] == 'DEBUG':
    logging.getLogger('ipnotebook').setLevel(logging.DEBUG)
elif confpars['main']['logging_level'] == 'ERROR':
    logging.getLogger('ipnotebook').setLevel(logging.ERROR)
elif confpars['main']['logging_level'] == 'CRITICAL':
    logging.getLogger('ipnotebook').setLevel(logging.CRITICAL)
elif confpars['main']['logging_level'] == 'FATAL':
    logging.getLogger('ipnotebook').setLevel(logging.FATAL)
elif confpars['main']['logging_level'] == 'INFO':
    logging.getLogger('ipnotebook').setLevel(logging.INFO)
