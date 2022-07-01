from django.contrib import admin
from .models import *

# Register your models here.
class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email']
    search_fields = ['email', 'first_name']
    
class taskModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_team', 'status']
    search_fields = ['name', 'team__name','status', 'started_at', 'completed_at']
    
    def get_team(self, obj):
        return obj.team.name
    get_team.short_description = 'Team'
    
class teamModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_leader']
    search_fields = ['name', 'team_leader__first_name']
    
    def get_leader(self, obj):
        return str(obj.team_leader.first_name)+ " " + str(obj.team_leader.last_name)
    get_leader.short_description = 'Team Leader'
    #get_leader.admin_order_field = 'book__author'
    
admin.site.register(CustomUserModel, CustomUserModelAdmin)
admin.site.register(taskModel, taskModelAdmin)
admin.site.register(teamModel, teamModelAdmin)