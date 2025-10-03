from django.db import models
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # 🔹 garante que e-mails não se repitam

    USERNAME_FIELD = 'email'   # 🔹 login será feito com e-mail
    REQUIRED_FIELDS = ['username']        # ⚠️ necessário para superuser



    class TipoUsuario(models.TextChoices):
        FREE = 'FREE', 'Free'
        PAGO = 'PAGO', 'Pago'

    tipo = models.CharField(
        max_length=10,
        choices=TipoUsuario.choices,
        default=TipoUsuario.FREE,  # <-- padrão FREE
        help_text="Tipo de usuário: Free (1 lote) ou Pago (ilimitado)"
    )
    def __str__(self):
        return self.email


class EggType(models.TextChoices):
    CODORNA = 'CODORNA', 'Codorna (17 dias)'
    GALINHA = 'GALINHA', 'Galinha (21 dias)'
    GALINHA_DA_ANGOLA = 'GALINHA DA ANGOLA', 'Galinhas da Angola(26 a 28 dias)'
    PERU = 'PERU', 'Perú (28 dias)'
    PERSONALIZADO = 'PERSONALIZADO', 'Personalizado'


DEFAULT_DIAS = {
    EggType.CODORNA: 17,
    EggType.GALINHA: 21,
    EggType.GALINHA_DA_ANGOLA: 28,
    EggType.PERU: 28,
}


class Lote(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # 🔹 Agora sim, aponta para o CustomUser
        on_delete=models.CASCADE,
        related_name="lotes",
        null=True,
        blank=True,
    )
    tipo_ovos = models.CharField(max_length=20, choices=EggType.choices)
    dias_personalizados = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Se vazio, usa padrão do tipo de ovos"
    )
    inicio_incubacao = models.DateTimeField(default=timezone.now)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-inicio_incubacao']

    def __str__(self):
        return self.nome

    @property
    def dias_incubacao(self) -> int:
        if self.tipo_ovos == EggType.PERSONALIZADO:
            return self.dias_personalizados or 0
        return DEFAULT_DIAS.get(self.tipo_ovos, 0)

    @property
    def dia_atual(self):
        hoje = date.today()
        delta = (hoje - self.inicio_incubacao.date()).days + 1
        return max(1, min(delta, self.dias_incubacao))

    @property
    def fim_previsto(self):
        if not self.inicio_incubacao or not self.dias_incubacao:
            return None
        return self.inicio_incubacao + timedelta(days=self.dias_incubacao)

    @property
    def progresso_percent(self) -> int:
        fim = self.fim_previsto
        if not fim:
            return 0
        agora = timezone.now()
        total = (fim - self.inicio_incubacao).total_seconds()
        decorrido = max(0, (agora - self.inicio_incubacao).total_seconds())
        if total <= 0:
            return 0
        return int(max(0, min(100, round((decorrido / total) * 100))))

    @property
    def status(self) -> str:
        if self.progresso_percent >= 100:
            return 'Concluído'
        return 'Em andamento'


class Anotacao(models.Model):
    lote = models.ForeignKey(
        Lote,
        on_delete=models.CASCADE,
        related_name="anotacoes"
    )
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anotação em {self.lote.nome} - {self.criado_em.strftime('%d/%m/%Y')}"




class Notificacao(models.Model):
    lote = models.ForeignKey(
        Lote,
        on_delete=models.CASCADE,
        related_name="notificacoes"
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificacoes"
    )
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    data = models.DateTimeField()  # quando o alerta deve aparecer
    lida = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data']

    def __str__(self):
        return f"Notif: {self.titulo} ({self.lote.nome})"
