from django.contrib import admin
from core.models import Client

@admin.register(Client)
class AdminClient(admin.ModelAdmin):
    list_display  = ('id','name',)
    readonly_fields = ('id',)
    model = Client