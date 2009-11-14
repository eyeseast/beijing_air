from django.contrib import admin
from beijing_air.models import AqiDefinition, SmogUpdate

class AqiDefinitionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class SmogUpdateAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'concentration', 'aqi', 'definition')

admin.site.register(AqiDefinition, AqiDefinitionAdmin)
admin.site.register(SmogUpdate, SmogUpdateAdmin)
