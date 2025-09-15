# Register your models here.

from django.contrib import admin
from .models import Lote

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_ovos', 'dias_incubacao', 'inicio_incubacao', 'fim_previsto', 'progresso_percent', 'status')
    list_filter = ('tipo_ovos',)
    search_fields = ('nome',)