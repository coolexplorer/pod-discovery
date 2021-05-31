from kubernetes import client, config

from consts.annotation_key import *
from schemas.pod_service import PodServiceCreate
from database.database import SessionLocal
from repositories.pod_service_repository import *


class K8SService:
    def __init__(self, k8s_config, discovery_config):
        if k8s_config.config_type == 'IN_CLUSTER':
            config.load_incluster_config()
        else:
            config.load_kube_config(k8s_config.config_path)
        self.client = client
        self.pods = []
        self.pod_services = []
        self.discovery_config = discovery_config
        self.discovery_config.pod_annotation_prefix = discovery_config.config_pod_annotation_prefix
        if discovery_config.config_use_db:
            self.db = SessionLocal()

    def search_pods(self, namespaces=None):
        if namespaces is None:
            namespaces = []

        pods = []
        if len(namespaces) > 0:
            for namespace in namespaces:
                v1 = self.client.CoreV1Api()
                res = v1.list_namespaced_pod(namespace=namespace)
                pods += list(filter(self.check_pod, res.items))
        else:
            v1 = self.client.CoreV1Api()
            res = v1.list_pod_for_all_namespaces(watch=False)
            pods += list(filter(self.check_pod, res.items))

        self.pods = pods
        self.pod_services = self.extract_metadata()

    def extract_metadata(self):
        delete_service_all_rows(self.db)

        pod_services = []
        db_pod_services = []
        for pod in self.pods:
            projects = pod.metadata.annotations[f'{self.discovery_config.pod_annotation_prefix}/{ANNOTATION_PROJECTS}']
            environment = pod.metadata.annotations[f'{self.discovery_config.pod_annotation_prefix}/{ANNOTATION_ENVIRONMENT}']
            if projects == '' or environment == '':
                continue

            projects = projects.split(',')
            service_type = pod.metadata.annotations[f'{self.discovery_config.pod_annotation_prefix}/{ANNOTATION_SERVICE_TYPE}']
            name = pod.metadata.annotations[f'{self.discovery_config.pod_annotation_prefix}/{ANNOTATION_NAME}']
            major_version = pod.metadata.annotations[f'{self.discovery_config.pod_annotation_prefix}/{ANNOTATION_MAJOR_VERSION}']
            url = self.create_url(projects, service_type, name, major_version)

            biom2_service = PodServiceCreate(
                name=name,
                major_version=major_version,
                minor_version=pod.metadata.annotations[f'{self.discovery_config.pod_annotation_prefix}/{ANNOTATION_MINOR_VERSION}'],
                patch_version=pod.metadata.annotations[f'{self.discovery_config.pod_annotation_prefix}/{ANNOTATION_PATCH_VERSION}'],
                type=service_type,
                source_link=pod.metadata.annotations[f'{self.discovery_config.pod_annotation_prefix}/{ANNOTATION_SOURCE_LINK}'],
                description=pod.metadata.annotations[f'{self.discovery_config.pod_annotation_prefix}/{ANNOTATION_DESCRIPTION}'],
                docs_link=pod.metadata.annotations[f'{self.discovery_config.pod_annotation_prefix}/{ANNOTATION_DOCS_LINK}'],
                friendly_name=pod.metadata.annotations[f'{self.discovery_config.pod_annotation_prefix}/{ANNOTATION_FRIENDLY_NAME}'],
                icon_url=pod.metadata.annotations[f'{self.discovery_config.pod_annotation_prefix}/{ANNOTATION_ICON_URL}'],
                environment=environment,
                url=url
            )
            pod_services.append(biom2_service)
            db_pod_services.append(create_pod_service(self.db, biom2_service, projects))
        insert_services(self.db, db_pod_services)
        service_names = list(map(lambda service: (service.name, service.environment), pod_services))
        logger.debug(f'Discovered services - {service_names}')
        return pod_services

    def check_pod(self, pod):
        if pod.metadata.annotations is not None:
            for key in pod.metadata.annotations.keys():
                if self.discovery_config.pod_annotation_prefix in key:
                    return pod
        return None

    def create_url(self, projects, service_type, name, major_version):
        if len(projects) == 0:
            projects = ["horde"]

        if service_type.lower() == 'service':
            url_type = 'services'
        else:
            url_type = 'apps'

        return f'{self.discovery_config.config_service_protocol}://{self.discovery_config.config_service_host}/{projects[0]}/{url_type}/{name}/v{major_version}/'
