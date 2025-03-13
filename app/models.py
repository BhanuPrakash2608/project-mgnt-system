# models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)

    google_email = models.EmailField(null=True, blank=True)
    google_name = models.CharField(max_length=255, null=True, blank=True)
    github_email = models.EmailField(null=True, blank=True)
    github_name = models.CharField(max_length=255, null=True, blank=True)
    facebook_email = models.EmailField(null=True, blank=True)
    facebook_name = models.CharField(max_length=255, null=True, blank=True)

    profile_picture = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Project(models.Model):
    STATUS_CHOICES = [
        ('Planning', 'Planning'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    team_members = models.ManyToManyField(User)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planning')
    excalidraw_link = models.URLField(blank=True, null=True)
    room_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.room_id:
            self.room_id = str(uuid.uuid4())
        if not self.excalidraw_link:
            self.excalidraw_link = f"https://excalidraw.com/#room={self.room_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES = (
        ('BACKLOG', 'Backlog'),
        ('DOING', 'Doing'),
        ('ON_HOLD', 'On Hold'),
        ('DONE', 'Done'),
        ('UNFINISHED', 'Unfinished'),
    )
    title = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ManyToManyField(User, related_name='tasks')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='BACKLOG')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Whiteboard(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="whiteboard")
    drawing_data = models.JSONField(default=dict)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Whiteboard for {self.project.title}"

class ProjectStatusLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20, choices=Project.STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=Project.STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.title}: {self.old_status} -> {self.new_status} at {self.changed_at}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()  # Already supports HTML like <a href>
    link = models.URLField(null=True, blank=True)  # Optional: Store the meeting link separately
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    sent_sms = models.BooleanField(default=False)  # Added to track SMS sending

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"