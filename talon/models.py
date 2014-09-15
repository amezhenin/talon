"""
Models for Todo application
"""
from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    """
    Main model for storing todo's information
    """
    user = models.ForeignKey(User)
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=2)
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    text = models.TextField()

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['created']
