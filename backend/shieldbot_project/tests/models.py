from django.db import models
from django.conf import settings
from django.utils import timezone
from celery.result import AsyncResult
from datetime import timedelta

class Test(models.Model):
    """Model for storing security test data"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tests")
    base_url = models.URLField(max_length=255)
    test_type = models.CharField(max_length=50, default="comprehensive")
    test_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default="Pending")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    logs = models.JSONField(default=dict, blank=True)
    ai_insights = models.JSONField(blank=True, null=True)
    celery_task_id = models.CharField(max_length=128, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Test {self.id} ({self.test_type}): {self.status}"
    
    @property
    def task_result(self):
        if self.celery_task_id:
            return AsyncResult(self.celery_task_id)
        return None

class RequestLog(models.Model):
    """Model for logging individual security test requests"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=50)
    base_url = models.TextField()
    options = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=50, default="Pending")
    execution_time = models.FloatField(null=True, blank=True)
    result = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    celery_task_id = models.CharField(max_length=128, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"RequestLog {self.id} - {self.test_type} - {self.status}"
    
    @staticmethod
    def validate_fields(data):
        """Validate and truncate fields to conform to database constraints."""
        data["test_type"] = data.get("test_type", "")[:50]
        data["base_url"] = data.get("base_url", "")[:255]
        data["status"] = data.get("status", "Pending")[:50]
        return data

class AppLog(models.Model):
    """Model for storing application-wide logs"""
    log_message = models.CharField(max_length=500)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.log_message[:50]}" 