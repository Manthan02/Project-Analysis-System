from django.contrib import admin
from .models import User,Project,Task,Friend,Groups,Friend_Request,Groups_Members,Groups_Request
# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Friend)
admin.site.register(Groups)
admin.site.register(Friend_Request)
admin.site.register(Groups_Members)
admin.site.register(Groups_Request)