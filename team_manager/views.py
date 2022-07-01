from datetime import date
from rest_framework.response import Response
from rest_framework.views import APIView
from .task import send_mail_task_status
from team_manager.serializers import GeneralSerializer
from .models import taskModel, teamModel
from rest_framework.decorators import api_view
# Create your views here.

class teamView(APIView):
    def get(self, request):
        teamId = request.GET.get('id')
        data = teamModel.objects.filter(id=teamId).values().first()
        return Response(data, status=200)
    
    def post(self, request):
        user = request.user
        if user.role!="usr":
            return Response("Sorry! You are not authenticated for this view", status=401)
        GeneralSerializer.Meta.model = teamModel
        cpy = request.POST.copy()
        if_remooved = ""
        if "team_members" in request.POST:
            if_remooved = " We have removed all added members, only team leader can add members to the team"
            del cpy['team_members']
        ser = GeneralSerializer(data=cpy, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(f"Hooray! Changes Saved.{if_remooved}", status=200)
        return Response(ser.errors, status=400)
            
class taskView(APIView):
    def get(self, request):
        data = taskModel.objects.all().values()
        return Response(data, status=200)
    
    def post(self, request):
        user = request.user
        if user.role!="usr":
            return Response("Sorry! You are not authenticated for this view", status=401)
        GeneralSerializer.Meta.model = taskModel
        ser = GeneralSerializer(data=request.POST, partial=True)
        if ser.is_valid():
            ser.save()
            # send mail here
            return Response("Hooray! Changes Saved", status=200)
        return Response(ser.errors, status=400)
    
    def patch(self, request):
        user = request.user
        if user.role=="tmr":
            return Response("Sorry! You are not authenticated for this view", status=401)
        try:
            taskId = int(request.POST['id'])
        except:
            taskId=None
        taskObj = taskModel.objects.filter(id=taskId)
        if not taskObj.exists():
            return Response("Enter a valid team ID for updation", status=400)
        taskObj = taskObj.first()
        GeneralSerializer.Meta.model = taskModel
        ser = GeneralSerializer(taskObj, data=request.POST, partial=True)
        if ser.is_valid():
            ser.save()
            return Response("Hooray! Changes Saved", status=200)
        return Response(ser.errors, status=400)
    
@api_view(['PATCH'])
def updateMembers(request):
    try:
        teamId = int(request.POST['id'])
    except:
        return Response("Enter a valid team ID for updation", status=400)
    teamObj = teamModel.objects.filter(id=teamId)
    if not teamObj.exists():
        return Response("Enter a valid team ID for updation", status=400)
    teamObj = teamObj.first()
    if(request.user.role!="tlr" or teamObj.team_leader.id!=request.user.id):
        return Response("Sorry! You are not authenticated for this view", status=401)
    dic = request.POST.copy()
    for a in list(dic.keys()):
        if(a!="team_members"):
            del dic[a]
    GeneralSerializer.Meta.model = teamModel
    ser = GeneralSerializer(teamObj, data=dic, partial=True)
    if ser.is_valid():
        ser.save()
        return Response("Hooray! Members Updated", status=200)
    return Response(ser.errors, status=400)

@api_view(["PATCH"])
def updateStatus(request):
    try:
        taskId = int(request.POST['id'])
    except:
        taskId=None
    try:
        taskStatus = request.POST['status']
    except:
        return Response("Enter a valid task status for updation", status=400)   
    taskObj = taskModel.objects.filter(id=taskId)
    if not taskObj.exists():
        return Response("Enter a valid ID for updation", status=400)
    try:
        taskObj.update(status=taskStatus)
    except Exception as exp:
        return Response(str(exp), status=400)
    if taskStatus=="done":
        taskObj.update(status=taskStatus, completed_at=date.today())
        #send mail here
        send_mail_task_status.delay(request.user.id, taskId)
    return Response("Status Updated", status=200)
