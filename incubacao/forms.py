from django import forms
from .models import Lote, EggType
from django.utils.timezone import localtime

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['nome', 'tipo_ovos', 'dias_personalizados', 'inicio_incubacao']
        # widgets = {
        #     'inicio_incubacao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        # }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_ovos': forms.Select(attrs={'class': 'form-select'}),
            'dias_personalizados': forms.NumberInput(attrs={'class': 'form-control'}),
            'inicio_incubacao': forms.DateInput(attrs={'type': 'datetime-local', 'class': 'form-control'}, format='%Y-%m-%dT%H:%M'),
        }

    def clean(self):
        data = super().clean()
        tipo = data.get('tipo_ovos')
        dias = data.get('dias_personalizados')
        if tipo == EggType.PERSONALIZADO and not dias:
            self.add_error('dias_personalizados', 'Informe os dias para o tipo personalizado.')
        return data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 🔹 Para garantir que na edição a data seja exibida no formato correto
        # if self.instance and self.instance.pk and self.instance.inicio_incubacao:
        #     self.initial['inicio_incubacao'] = self.instance.inicio_incubacao.strftime('%Y-%m-%dT%H:%M')

        if self.instance and self.instance.pk and self.instance.inicio_incubacao:
            local_dt = localtime(self.instance.inicio_incubacao)  # 🔹 converte UTC → TIME_ZONE
            self.initial['inicio_incubacao'] = local_dt.strftime('%Y-%m-%dT%H:%M')