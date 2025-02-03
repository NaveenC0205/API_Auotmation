import configparser
from pathlib import Path
from API_Automation.E2E_Framework.logger_config import logger
cfgFile = 'env.ini'
cfgFileDir = 'config'

config = configparser.ConfigParser()
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR.joinpath(cfgFileDir).joinpath(cfgFile)
config.read(CONFIG_FILE)

urls_config = {
    'local-email': {'url': config['local-email']['url'], 'port': '7071'},
    'local-recipients': {'url': config['local-recipients']['url'], 'port': '7072'},
    'local-campaigns': {'url': config['local-campaigns']['url'], 'port': '7073'},
    'dev-email': {'url': config['dev-email']['url'], 'port': '7071'},
    'dev-receipents': {'url': config['dev-receipents']['url'], 'port': '7072'},
    'dev-campains': {'url': config['dev-campains']['url'], 'port': '7073'},
}

def get_URL(Env, clients):
    """
    Function to return a dictionary of client base URLs based on the environment and clients.
    """
    baseURLs = {}
    if Env == "local":
        for client in clients:
            try:

                url = urls_config[f'local-{client}']['url'].strip('"')
                if not url.lower().startswith('http://') and not url.lower().startswith('https://'):
                    url = 'http://' + url

                baseURLs[client] = url
                logger.info(f"Base URL for {client} in local environment: {baseURLs[client]}")
            except KeyError:
                baseURLs[client] = ''
                logger.warning(f"No matching URL found for 'local-{client}'")

    elif Env in ['dev', 'test', 'uat']:
        for client in clients:
            try:
                url = urls_config[f'{Env}-{client}']['url'].strip('"')
                if not url.lower().startswith('http://') and not url.lower().startswith('https://'):
                    url = 'http://' + url

                baseURLs[client] = url
                logger.info(f"Base URL for {client} in {Env} environment: {baseURLs[client]}")
            except KeyError:
                baseURLs[client] = ''
                logger.warning(f"No matching URL found for '{Env}-{client}'")

    if not baseURLs:
        logger.error("No matching URLs found for the given environment and clients.")
        raise ValueError("No URL matches the provided environment and client.")

    return baseURLs