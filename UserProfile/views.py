import uuid
from .choices import ChoicesBancos, ChoicesTipoConta
from django.contrib import messages
from .models import Conta, Categoria
from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.core.exceptions import ValidationError
from .utils import calcula_total
from extract.models import Valores
from django.db.models import Sum
from datetime import datetime, timedelta, date
from django.utils import timezone
from bill.models import ContaPagar, ContaPaga

def home(request):
    contas = Conta.objects.all()
    contas_a_pagar = ContaPagar.objects.all()

    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    total_contas = calcula_total(contas, 'valor')
    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')
    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')
    saldo_mensal = total_entradas - total_saidas
    despesa_mensal = total_saidas
    total_livre = saldo_mensal
    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')
    contas_vencidas = contas_a_pagar.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)    
    contas_proximas_vencimento = contas_a_pagar.filter(dia_pagamento__lte = DIA_ATUAL + 5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)

    context = {
        'contas': contas,
        'total_contas': total_contas,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo_mensal': saldo_mensal,
        'despesa_mensal': despesa_mensal,
        'total_livre': total_livre,
        'percentual_gastos_essenciais':percentual_gastos_essenciais,
        'percentual_gastos_nao_essenciais':percentual_gastos_nao_essenciais,
        'contas_proximas_vencimento': contas_proximas_vencimento,
        'contas_vencidas': contas_vencidas,
    }

    return render(request, 'home.html', context)

def manage(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    total_contas = calcula_total(contas, 'valor')

    for conta in contas:
        conta.banco_nome = ChoicesBancos.get_banco_nome(conta.banco)

    tipo = ChoicesTipoConta.tipo
    bancos = ChoicesBancos.bancos

    context = {
        'contas': contas,
        'categorias': categorias,
        'total_contas': total_contas,
        'tipo': tipo,
        'bancos': bancos,
    }

    return render(request, 'manage.html', context)

def cadastrar_banco(request):
    if request.method == 'POST':
        apelido = request.POST.get('apelido')
        banco = request.POST.get('banco')
        tipo = request.POST.get('tipo')
        valor = request.POST.get('valor')
        icone = request.FILES.get('icone')

        if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/UserProfile/manage/')
        
        try:
            valor = float(valor)
        except ValueError:
            messages.add_message(request, constants.ERROR, 'Valor inválido')
            return redirect('/UserProfile/manage/')
        
        token = uuid.uuid4()

        conta = Conta(
            apelido = apelido,
            banco = banco,
            tipo=tipo,
            valor=valor,
            icone=icone,
            token=token
        )
        try:
            #conta.full_clean()  # Valida o objeto de acordo com as restrições do modelo
            conta.save()
            messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')
        except ValidationError as e:
            messages.add_message(request, constants.ERROR, 'Erro ao cadastrar conta: {}'.format(e))
        except Exception as e:
            messages.add_message(request, constants.ERROR, 'Erro desconhecido: {}'.format(e))

    return redirect('/UserProfile/manage/')


def deletar_banco(request, token):
    
    conta = Conta.objects.get(token=token)
    print(conta)
    conta.delete()

    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso!')
    return redirect('/UserProfile/manage/')

def cadastrar_categoria(request):
    if request.method == 'POST':
        nome = request.POST.get('categoria')
        essencial = bool(request.POST.get('essencial'))

        if not nome or len(nome.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'O nome da categoria não pode estar vazio.')
            return redirect('/UserProfile/manage/')

        token = uuid.uuid4()

        categoria = Categoria(
            categoria=nome,
            essencial=essencial,
            token=token
        )

        try:
            categoria.full_clean()
            categoria.save()
            messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
        except ValidationError as e:
            messages.add_message(request, constants.ERROR, 'Erro ao cadastrar categoria: {}'.format(e))
        except Exception as e:
            messages.add_message(request, constants.ERROR, 'Erro desconhecido: {}'.format(e))
    return redirect('/UserProfile/manage/')

def update_categoria(request, token):
    categoria = Categoria.objects.get(token=token)
    categoria.essencial = not categoria.essencial
    categoria.save()
    return redirect('/UserProfile/manage/')

def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        valor = Valores.objects.filter(categoria=categoria).aggregate(Sum('valor'))['valor__sum']
        dados[categoria.categoria] = float(valor) if valor else None

    context = {
        'labels': list(dados.keys()),
        'values': list(dados.values()),
    }

    return render(request, 'dashboard.html', context)

def calcula_equilibrio_financeiro():
    gastos_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=False)

    total_gastos_essenciais = calcula_total(gastos_essenciais, 'valor')
    total_gastos_nao_essenciais = calcula_total(gastos_nao_essenciais, 'valor')

    total = total_gastos_essenciais + total_gastos_nao_essenciais
    try:
        percentual_gastos_essenciais = total_gastos_essenciais * 100 / total
        percentual_gastos_nao_essenciais = total_gastos_nao_essenciais * 100 / total

        return percentual_gastos_essenciais, percentual_gastos_nao_essenciais
    except:
        return 0, 0