import configparser

__CONFIG_INI_PATH = "config.ini"
__CONFIG_DEFAULT = "[credentials]\nBearerToken = PUT_YOUR_TOKEN_HERE"

def get_bearer_token():
    parser = configparser.RawConfigParser(empty_lines_in_values=False)

    try:
        config_file = open(__CONFIG_INI_PATH)
        parser.read_file(config_file)
        if parser['credentials']['BearerToken'] not in ('', 'PUT_YOUR_TOKEN_HERE'):
            return parser['credentials']['BearerToken']
    except FileNotFoundError as e:
        with open(__CONFIG_INI_PATH, 'w') as f:
            f.write(__CONFIG_DEFAULT)
    except:
        pass

    raise ValueError("Please, configure your credentials correctly => config.ini\n", __CONFIG_DEFAULT)