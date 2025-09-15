from django.db import models

# Create your models here.


from django.db import models
from django.utils import timezone
from datetime import timedelta

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
from datetime import date
class Lote(models.Model):
    nome = models.CharField(max_length=100)
    tipo_ovos = models.CharField(max_length=20, choices=EggType.choices)
    dias_personalizados = models.PositiveIntegerField(null=True, blank=True, help_text="Se vazio, usa padrão do tipo de ovos")
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
        """Progresso 0–100 baseado no tempo decorrido entre início e fim previsto."""
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