from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta
import uuid
from django.contrib import messages
from django.contrib.messages import constants
from .choices import ChoicesBancos, ChoicesTipoConta

def home(request):
    return render(request, 'home.html')

def manage(request):
    contas = Conta.objects.all()
    total_contas = 0

    for conta in contas:
        conta.banco_nome = ChoicesBancos.get_banco_nome(conta.banco)
        total_contas += conta.valor

    context = {
        'contas': contas,
        'total_contas': total_contas,
    }

    return render(request, 'manage.html', context)

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
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
    conta.save()

    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')
    return redirect('/UserProfile/manage/')


def deletar_banco(request, token):
    conta = Conta.objects.get(token=token)

    conta.delete()

    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso!')
    return redirect('/UserProfile/manage/')