from django.contrib import admin
from beijing_air.models import AqiDefinition, SmogUpdate

class AqiDefinitionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(AqiDefinition, AqiDefinitionAdmin)
admin.site.register(SmogUpdate)
