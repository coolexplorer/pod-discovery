
class DiscoveryConfig:
    def __init__(self, config_service_protocol='', config_service_host='', config_cron_enable=True,
                 config_pod_annotation_prefix=''):
        self.config_service_protocol = config_service_protocol
        self.config_service_host = config_service_host
        self.config_use_db = config_cron_enable
        self.config_pod_annotation_prefix = config_pod_annotation_prefix

    def __str__(self):
        return f"""
        Service Protocol: {self.config_service_protocol} Host: {self.config_service_host}
        Cron enable: {self.config_use_db}            
        """.strip()
