import configparser
import os

class ConfigManager:

    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.default_config = self.config['DEFAULT']

    @property
    def downloads_blocks_folder(self):
        return self.default_config.get('downloads_blocks_folder', '')

    @property
    def output_folder(self):
        return self.default_config.get('output_folder', '')
    
    @property
    def processed_blocks_folder(self):
        return self.default_config.get('processed_blocks_folder', '')


    def get(self, key, default=None):
        return self.default_config.get(key, default)
