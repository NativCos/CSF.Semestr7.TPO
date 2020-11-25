import logging
import configparser
import os


_proj_root = os.path.dirname(os.path.realpath(__file__))

configs = configparser.SafeConfigParser()
configs.read(os.path.join(_proj_root, 'baseconfig.ini'))
configs['main']['proj_root'] = _proj_root
configs['main']['strftime_format'] = '%%H:%%M %%d %%B %%Y'

logging_format = "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s"
logging.basicConfig(format=logging_format)
if configs['logging']['level'] == 'DEBUG':
    logging.getLogger('ipnotebook').setLevel(logging.DEBUG)
elif configs['logging']['level'] == 'ERROR':
    logging.getLogger('ipnotebook').setLevel(logging.ERROR)
elif configs['logging']['level'] == 'CRITICAL':
    logging.getLogger('ipnotebook').setLevel(logging.CRITICAL)
elif configs['main']['level'] == 'FATAL':
    logging.getLogger('ipnotebook').setLevel(logging.FATAL)
elif configs['logging']['level'] == 'INFO':
    logging.getLogger('ipnotebook').setLevel(logging.INFO)
