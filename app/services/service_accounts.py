from services.k8s_service import K8SService


class ServiceAccounts:
    def __init__(self, config):
        self.k8s = K8SService(config.kubernetes, config.discovery)
