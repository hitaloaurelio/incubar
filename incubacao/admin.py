# Register your models here.

from django.contrib import admin
from .models import Lote

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Lote

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_ovos', 'usuario','dias_incubacao', 'inicio_incubacao', 'fim_previsto', 'progresso_percent', 'status')
    list_filter = ('tipo_ovos',)
    search_fields = ('nome',)




class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Campos que serão exibidos na listagem
    list_display = ('email', 'username', 'tipo', 'is_staff', 'is_active','tipo')
    list_filter = ('tipo', 'is_staff', 'is_active','tipo')

    # Campos do formulário de edição/criação
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'tipo')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'tipo', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)