# issues/models.py
from django.db import models
from django.conf import settings  # to reference AUTH_USER_MODEL

# Issue status choices
STATUS_CHOICES = [
    ('Open', 'Open'),
    ('In Progress', 'In Progress'),
    ('Closed', 'Closed'),
]

# Issue category choices
CATEGORY_CHOICES = [
    ('Pothole', 'Pothole'),
    ('Lighting', 'Lighting'),
    ('Fly-tipping', 'Fly-tipping'),
    ('Blocked Drain', 'Blocked Drain'),
    ('Graffiti', 'Graffiti'),
    ('Other', 'Other')
]

class Issue(models.Model):
    title = models.CharField(max_length=100)  # Title of the issue
    description = models.TextField()  # Detailed description of the issue
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
        null=True, blank=True, related_name='reported_issues'
    )  # User who reported the issue
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
        null=True, blank=True, related_name='assigned_issues'
    )  # User who is assigned to resolve the issue
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')  # Current status of the issue
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Other')  # Category of the issue
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the issue was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the issue was last updated

    def __str__(self):
        return self.title  # String representation of the issue (returns title)
    
    class Meta:
        ordering = ['-created_at']  # Order issues by creation date (newest first)
