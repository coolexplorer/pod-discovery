import os

from config.discovery_config import DiscoveryConfig
from config.k8s_config import K8SConfig


class Configuration:
    def __init__(self):
        self.discovery = DiscoveryConfig()
        self.kubernetes = K8SConfig()

    def read_env(self):
        self._read_discovery_evn()
        self._read_k8s_env()

    def _read_discovery_evn(self):
        self.discovery.config_service_protocol = os.environ.get('SERVICE_PROTOCOL', 'https')
        self.discovery.config_service_host = os.environ.get('SERVICE_HOST', 'biom2.eakr.io')
        self.discovery.config_pod_annotation_prefix = os.environ.get('POD_ANNOTATION_PREFIX', "consul-registrator")
        self.discovery.config_use_db = os.environ.get('USE_DB', True)

    def _read_k8s_env(self):
        self.kubernetes.config_type = os.environ.get('K8S_CONFIG_TYPE', 'FILE')  # ['FILE', 'IN_CLUSTER']
        self.kubernetes.config_path = os.environ.get('K8S_CONFIG_PATH', '~/.kube/config')
