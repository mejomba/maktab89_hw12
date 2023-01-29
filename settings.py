import configparser

config = configparser.ConfigParser()
config.read('credential.conf')
super_user_password = config['SUPERUSER']['password']


DEBUG = True
