from django.db import models

from tourism.models.timestamp import TimestampMdl

class IssueMdl(TimestampMdl):
    ISSUE_PRIORITY_CHOICES = [
        ('P4','Low'),
        ('P3','Medium'),
        ('P2','Important'),
        ('P1','Urgent'),
        ('P0','Critical'),
    ]
    ISSUE_STATUS_CHOICES = [
        ('new','New'),
        ('assigned','Assigned'),
        ('in_progress','In-Progress'),
        ('resolved','Resolved'),
        ('verified','Verified'),
        ('closed','Closed'),
    ]
    desc = models.TextField()
    priority = models.CharField(max_length=255, choices=ISSUE_PRIORITY_CHOICES, default='P4')
    status = models.CharField(max_length=255, choices=ISSUE_STATUS_CHOICES, default='new')
    class Meta:
        abstract = True
