import configparser

__Credentials = "credentials"
__ApiKey = "ApiKey"
__ApiKeySecret = "ApiKeySecret"

__CONFIG_INI_PATH = "config.ini"
__CONFIG_DEFAULT = f"[{__Credentials}]\n{__ApiKey} = PUT_YOUR_TOKEN_HERE\n{__ApiKeySecret} = PUT_YOUR_TOKEN_HERE"
__INVALID_DATA = ('', 'PUT_YOUR_TOKEN_HERE')

def get_credentials():
    parser = configparser.RawConfigParser()
    try:
        config_file = open(__CONFIG_INI_PATH)
        parser.read_file(config_file)
        credentials = parser[__Credentials]
        if credentials[__ApiKey] not in __INVALID_DATA and credentials[__ApiKeySecret] not in __INVALID_DATA:
            return (credentials[__ApiKey], credentials[__ApiKeySecret])
    except FileNotFoundError as e:
        with open(__CONFIG_INI_PATH, 'w') as f:
            f.write(__CONFIG_DEFAULT)
    except:
        pass

    raise ValueError("Please, configure your credentials correctly => config.ini\n", __CONFIG_DEFAULT)

if __name__ == '__main__':
	get_credentials()