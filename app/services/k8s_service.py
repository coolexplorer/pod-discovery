from kubernetes import client, config

from consts.annotation_key import *
from schemas.biom2_service import Biom2ServiceCreate
from database.database import SessionLocal
from repositories.biom2_service_repository import *

BIOM2_ANNOTATION_PREFIX = "consul-registrator"
db = SessionLocal()


def check_biom2_pod(pod):
    if pod.metadata.annotations is not None:
        for key in pod.metadata.annotations.keys():
            if BIOM2_ANNOTATION_PREFIX in key:
                return pod
    return None


class K8SService:
    def __init__(self, k8s_config, discovery_config):
        if k8s_config.config_type == 'IN_CLUSTER':
            config.load_incluster_config()
        else:
            config.load_kube_config(k8s_config.config_path)
        self.client = client
        self.biom2_pods = []
        self.biom2_services = []
        self.discovery_config = discovery_config

    def search_biom2_pods(self, namespaces=None):
        if namespaces is None:
            namespaces = []

        biom2_pods = []
        if len(namespaces) > 0:
            for namespace in namespaces:
                v1 = self.client.CoreV1Api()
                res = v1.list_namespaced_pod(namespace=namespace)
                biom2_pods += list(filter(check_biom2_pod, res.items))
        else:
            v1 = self.client.CoreV1Api()
            res = v1.list_pod_for_all_namespaces(watch=False)
            biom2_pods += list(filter(check_biom2_pod, res.items))

        self.biom2_pods = biom2_pods
        self.biom2_services = self.extract_biom2_metadata()

    def extract_biom2_metadata(self):
        delete_service_all_rows(db)

        biom2_services = []
        db_biom2_services = []
        for pod in self.biom2_pods:
            projects = pod.metadata.annotations[f'{BIOM2_ANNOTATION_PREFIX}/{ANNOTATION_PROJECTS}']
            environment = pod.metadata.annotations[f'{BIOM2_ANNOTATION_PREFIX}/{ANNOTATION_ENVIRONMENT}']
            if projects == '' or environment == '':
                continue

            projects = projects.split(',')
            service_type = pod.metadata.annotations[f'{BIOM2_ANNOTATION_PREFIX}/{ANNOTATION_SERVICE_TYPE}']
            name = pod.metadata.annotations[f'{BIOM2_ANNOTATION_PREFIX}/{ANNOTATION_NAME}']
            major_version = pod.metadata.annotations[f'{BIOM2_ANNOTATION_PREFIX}/{ANNOTATION_MAJOR_VERSION}']
            url = self.create_url(projects, service_type, name, major_version)

            biom2_service = Biom2ServiceCreate(
                name=name,
                major_version=major_version,
                minor_version=pod.metadata.annotations[f'{BIOM2_ANNOTATION_PREFIX}/{ANNOTATION_MINOR_VERSION}'],
                patch_version=pod.metadata.annotations[f'{BIOM2_ANNOTATION_PREFIX}/{ANNOTATION_PATCH_VERSION}'],
                type=service_type,
                source_link=pod.metadata.annotations[f'{BIOM2_ANNOTATION_PREFIX}/{ANNOTATION_SOURCE_LINK}'],
                description=pod.metadata.annotations[f'{BIOM2_ANNOTATION_PREFIX}/{ANNOTATION_DESCRIPTION}'],
                docs_link=pod.metadata.annotations[f'{BIOM2_ANNOTATION_PREFIX}/{ANNOTATION_DOCS_LINK}'],
                friendly_name=pod.metadata.annotations[f'{BIOM2_ANNOTATION_PREFIX}/{ANNOTATION_FRIENDLY_NAME}'],
                icon_url=pod.metadata.annotations[f'{BIOM2_ANNOTATION_PREFIX}/{ANNOTATION_ICON_URL}'],
                environment=environment,
                url=url
            )
            biom2_services.append(biom2_service)
            db_biom2_services.append(create_biom2_service(db, biom2_service, projects))
        insert_services(db, db_biom2_services)
        service_names = list(map(lambda service: (service.name, service.environment), biom2_services))
        logger.debug(f'Discovered services - {service_names}')
        return biom2_services

    def create_url(self, projects, service_type, name, major_version):
        if len(projects) == 0:
            projects = ["horde"]

        if service_type.lower() == 'service':
            url_type = 'services'
        else:
            url_type = 'apps'

        return f'{self.discovery_config.config_biom2_protocol}://{self.discovery_config.config_biom2_host}/{projects[0]}/{url_type}/{name}/v{major_version}/'
