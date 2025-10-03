from background_task import background
from datetime import timedelta
from django.utils import timezone

@background(schedule=3600)  # roda após 1 (uma) hora 
def verificar_lotes_task():
    from .models import Lote, Notificacao

    print("RODANDO A CADA 60 SEGUNDOS NOVO")
    agora = timezone.now()

    # Lista de notificações que queremos criar
    notificacoes_regras = [
        {
            "titulo": "Lote completou 24h",
            "mensagem": lambda lote: f"O lote {lote.nome} completou 24 horas.",
            "horas_antes": -24,  # negativo indica depois da criação
            "comparar_criado": True
        },
        {
            "titulo": "Desligar giro dos ovos",
            "mensagem": lambda lote: "Está a 48h do fim da incubação. Desligue o giro.",
            "horas_antes": 48,  # positivo indica antes do fim
            "comparar_criado": False
        },
    ]

    lotes = Lote.objects.all()
    for lote in lotes:
        for regra in notificacoes_regras:
            titulo = regra["titulo"]

            # Evita duplicatas
            if Notificacao.objects.filter(lote=lote, titulo=titulo).exists():
                continue

            if regra["comparar_criado"]:
                # Verificação baseada na data de criação
                limite = agora - timedelta(hours=abs(regra["horas_antes"]))
                if lote.criado_em <= limite:
                    Notificacao.objects.create(
                        lote=lote,
                        usuario=lote.usuario,
                        titulo=titulo,
                        mensagem=regra["mensagem"](lote),
                        data=agora
                    )
            else:
                # Verificação baseada no fim da incubação
                fim = lote.fim_previsto
                if not fim:
                    continue

                delta = fim - agora
                # Considera uma janela de 1 hora para tolerância
                if timedelta(hours=regra["horas_antes"]-1) <= delta <= timedelta(hours=regra["horas_antes"]):
                    Notificacao.objects.create(
                        lote=lote,
                        usuario=lote.usuario,
                        titulo=titulo,
                        mensagem=regra["mensagem"](lote),
                        data=agora
                    )
