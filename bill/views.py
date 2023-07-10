from django.shortcuts import render, redirect
from UserProfile.models import Categoria
import uuid
from .models import ContaPaga, ContaPagar
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
import uuid

def define_bill(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()

        context = {
            'categorias': categorias
        }

        return render(request, 'define_bill.html', context)
    else:
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        token = uuid.uuid4()

        conta = ContaPagar(
            titulo=titulo,
            categoria_id=categoria,
            descricao=descricao,
            valor=valor,
            dia_pagamento=dia_pagamento,
            token=token
        )

        conta.save()

        messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
        return redirect('/bill/define_bill')

def check_bill(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day
    
    contas = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')

    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte = DIA_ATUAL + 5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)
    
    restantes = contas.exclude(id__in=contas_vencidas).exclude(id__in=contas_pagas).exclude(id__in=contas_proximas_vencimento)

    context = {
        'contas_vencidas': contas_vencidas,
        'contas_proximas_vencimento': contas_proximas_vencimento,
        'restantes': restantes
    }

    return render(request, 'check_bill.html', context)

def pay_bill(request, token):
    contapagar = ContaPagar.objects.get(token=token)

    token = uuid.uuid4()

    contapaga = ContaPaga(
            conta=contapagar,
            data_pagamento=datetime.now(),
            token=token
        )
    contapaga.save()
    messages.add_message(request, constants.SUCCESS, 'Excelente, mais uma conta paga.')
    return redirect('/bill/check_bill')