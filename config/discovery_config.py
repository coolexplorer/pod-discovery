
class DiscoveryConfig:
    def __init__(self, config_biom2_protocol='', config_biom2_host=''):
        self.config_biom2_protocol = config_biom2_protocol
        self.config_biom2_host = config_biom2_host

    def __str__(self):
        return f"BioMetrics2 Protocol: {self.config_biom2_protocol} Host: {self.config_biom2_host}"
