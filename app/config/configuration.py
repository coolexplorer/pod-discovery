import os

from app.config.discovery_config import DiscoveryConfig
from app.config.k8s_config import K8SConfig


class Configuration:
    def __init__(self):
        self.discovery = DiscoveryConfig()
        self.kubernetes = K8SConfig()

    def read_env(self):
        self._read_discover_evn()
        self._read_k8s_env()

    def _read_discover_evn(self):
        self.discovery.config_biom2_protocol = os.environ.get('BIOM2_PROTOCOL', 'https')
        self.discovery.config_biom2_host = os.environ.get('BIOM2_HOST', 'biom2.eakr.io')

    def _read_k8s_env(self):
        self.kubernetes.config_type = os.environ.get('K8S_CONFIG_TYPE', 'FILE')  # ['FILE', 'IN_CLUSTER']
        self.kubernetes.config_path = os.environ.get('K8S_CONFIG_PATH', '~/.kube/config')
