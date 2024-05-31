import configparser
import os


class ConfigManager:

    def __init__(self):
        self.config = configparser.ConfigParser()
        base_folder = os.path.dirname(os.path.abspath(__file__))
        self.config_file_path = os.path.join(base_folder, 'config.ini')
        if os.name == 'nt':
            self.downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        else:
            self.downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    def write_config(self, path_to_save=''):
        if path_to_save == '':
            path_to_save = self.downloads_folder
        self.config['Settings'] = {
            'path_to_save': path_to_save
        }
        with open(self.config_file_path, 'w') as configfile:
            self.config.write(configfile)

    def read_config(self):
        config = {}
        if os.path.exists(self.config_file_path):
            self.config.read(self.config_file_path)
            if 'Settings' in self.config:
                if 'path_to_save' in self.config['Settings']:
                    path_to_save = self.config['Settings']['path_to_save']
                    config["path_to_save"] = path_to_save
                    return config
        self.write_config()
        return self.read_config()

