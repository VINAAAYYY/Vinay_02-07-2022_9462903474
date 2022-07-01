from datetime import date
from celery import shared_task
from django.core.mail import send_mail
from django.apps import apps
from django.contrib.auth import get_user_model

def posting(reciever, message, subject):
    from_id = "navccp69@gmail.com"
    send_mail(subject=subject,
              message=message,
              from_email=from_id,
              recipient_list=[reciever],
              fail_silently = False)
    return None

@shared_task(bind=True)
def send_mail_task(self, teamId=int()):
    model = apps.get_model("team_manager", "taskModel")
    taskObj = model.objects.get(id=teamId)
    taskMembers = list(taskObj.team.team_members.values('first_name', 'last_name', 'email'))
    name = taskObj.name
    leader_name = taskObj.team.team_leader.first_name +" "+ taskObj.team.team_leader.last_name
    team = taskObj.team.name
    description = taskObj.description
    subject = "Congrats! New Task Assigned Under You"
    message = f"Hello, {leader_name}. You have been assigned a new task named  {name} for your team {team}. Your team is \n {taskMembers}. Description for the task: \n {description} "
    posting(taskObj.team.team_leader.email, message, subject)
    return None

@shared_task(bind=True)
def send_mail_task_status(self, user_id=int(), taskId=int()):
    task_model = apps.get_model("team_manager", "taskModel")
    taskObj = task_model.objects.get(id=taskId)
    userObj = get_user_model().objects.get(id=user_id)
    leader_name = taskObj.team.team_leader.first_name +" "+ taskObj.team.team_leader.last_name
    task_name = taskObj.name
    team_name = taskObj.team.name
    subject = "Have a treat. Your Team has completed a task"
    message = f"Greetings, {leader_name}. Your team  {team_name} has reported the completion of task {task_name}. This status has been updated by {userObj.first_name} {userObj.last_name} ({userObj.email}) on " + str(date.today())
    posting(taskObj.team.team_leader.email, message, subject)
    return None
    
