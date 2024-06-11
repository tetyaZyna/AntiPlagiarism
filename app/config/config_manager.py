import configparser
import os
import platform


class ConfigManager:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file_path = self.get_config_path()
        self.downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    def get_config_path(self):
        os_type = platform.system()
        app_name = 'AntiPlagiat'
        if os_type == 'Windows':
            config_dir = os.path.join(os.getenv('APPDATA'), app_name)
        elif os_type == 'Linux':
            config_dir = os.path.join(os.path.expanduser('~'), '.config', app_name)
        elif os_type == 'Darwin':
            config_dir = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', app_name)
        else:
            raise NotImplementedError(f"OS '{os_type}' is not supported.")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, 'config.ini')

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

