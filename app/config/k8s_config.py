
class K8SConfig:
    def __init__(self, config_type='', config_path=''):
        self.config_type = config_type
        self.config_path = config_path

    def __str__(self):
        return f"type: {self.config_type}, path: {self.config_path}"
