from django.db import models

class Alert(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    source_ip = models.CharField(max_length=15)
    destination_ip = models.CharField(max_length=15)
    threat_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=10, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])

    def __str__(self):
        return f"{self.threat_type} from {self.source_ip}"

class Packet(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    source_ip = models.CharField(max_length=15)
    destination_ip = models.CharField(max_length=15)
    protocol = models.CharField(max_length=10)
    length = models.IntegerField()

    def __str__(self):
        return f"{self.protocol} packet from {self.source_ip} to {self.destination_ip}"