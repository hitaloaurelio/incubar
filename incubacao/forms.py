from django import forms
from .models import Lote, EggType
from django.utils.timezone import localtime

from django.contrib.auth.forms import AuthenticationForm

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        exclude = ['usuario']  # 🔹 usuário será setado automaticamente
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

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ("email",)   # só e-mail, senha já vem do UserCreationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        # 🔹 Define o username como email para satisfazer a constraint do banco
        user.username = user.email
        if commit:
            user.save()
        return user




class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="E-mail",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Digite seu e-mail"})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Digite sua senha"})
    )