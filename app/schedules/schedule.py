from apscheduler.schedulers.background import BackgroundScheduler

from utils.logger import logger


class Schedule:
    def __init__(self, k8s_service):
        self.schedule = BackgroundScheduler()
        self.k8s_service = k8s_service

    def start(self):
        self.schedule.start()

    def add_discovery_cron_job(self, cron_expression, schedule_id):
        self.schedule.add_job(self.k8s_service.search_pods, 'cron', second=cron_expression, id=schedule_id)
