import configparser
import os
from re import search


def get_config_value(section, key):
    config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_file)

    try:
        value = config.get(section, key)
        
        # If the section is [files], resolve relative paths relative to the config file location
        if section == 'files' and value.startswith('..'):
            config_dir = os.path.dirname(config_file)
            value = os.path.abspath(os.path.join(config_dir, value))
        
        return value
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    key_value = get_config_value(search, 'search_0')
    print(f"Value for 'key1': {key_value}")
