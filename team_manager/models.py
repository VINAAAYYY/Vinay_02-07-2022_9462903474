from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from .task import send_mail_task

# Create your models here.
class CustomUserModel(AbstractUser):
    roleChoices = [
        ('usr','user'),
        ('tmr','team-member'),
        ('tlr','team-leader')
    ]
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(max_length = 3, choices=roleChoices, default='tmr')

class teamModel(models.Model):
    name = models.CharField(max_length = 50)
    team_leader = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True, blank=True, related_name="team_leader")
    team_members = models.ManyToManyField(CustomUserModel,  related_name="team_members", blank=True, null=True)  
    """  NOTE:  
        while sending request using postman form remember to send
        team_members 1 and another field of team_members 2 for both to be added as team members.
        Else doing something like:
        team_members [1, 2]
        it will be sent as {"team_members"}:"[1,2]" which will give error.  
    """
    
class taskModel(models.Model):
    statusChoices = [
        ('asgn','assigned'),
        ('prog','in-progress'),
        ('revw','under-review'),
        ('done','done')
    ]
    name = models.CharField(max_length = 50)
    team = models.ForeignKey(teamModel, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length = 4, choices=statusChoices, default='asgn')
    description = models.TextField(blank=True, null=True)
    started_at = models.DateField(default = date.today())
    completed_at = models.DateField(blank=True, null=True)
    
    # NOTE:
    # overriding the save function drawbacks:
    # even if someone simply changes the team even from the admin panel, this will send the mail to the team leader 
    def save(self, *args, **kwargs):
        send_mail_task.delay(self.id)
        super(taskModel, self).save(*args, **kwargs)
    
    