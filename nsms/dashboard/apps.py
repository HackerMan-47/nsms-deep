from django.apps import AppConfig
from django.core.signals import request_started
from django.db.utils import OperationalError
from threading import Thread

class DashboardConfig(AppConfig):
    name = 'dashboard'

    def start_capture_thread(self):
        from .packet_capture import start_capture  # يتم استيراده هنا لتجنب مشاكل التحميل المبكر
        try:
            capture_thread = Thread(target=start_capture)
            capture_thread.daemon = True
            capture_thread.start()
        except OperationalError:
            print("Database not ready, packet capture won't start.")

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(lambda sender, **kwargs: self.start_capture_thread(), sender=self)
