# -*- coding: utf-8 -*-
import json
import os

class Config:

    def __init__(self, config_file='config.json'):
        self.config = self._load_config(config_file)  
        
    def _load_config(self, config_file):
        with open(config_file) as f:
            config = json.load(f)
                
        domain = os.environ.get('STATIC_DOMAIN')
        if domain:
            config['static_domain'] = domain

        static_type = os.environ.get('STATIC_TYPE')
        if static_type:
            config['static_type'] = static_type

        static_max_file_size = os.environ.get('STATIC_MAX_FILE_SIZE')
        if static_max_file_size:
            config['static_max_file_size'] = static_max_file_size
            
        return config
    
    def get(self, name):
        return self.config.get(name)
     
    