import uuid
from .choices import ChoicesBancos
from django.contrib import messages
from .models import Conta, Categoria
from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.core.exceptions import ValidationError
from .utils import calcula_total

def home(request):
    contas = Conta.objects.all()

    total_contas = calcula_total(contas, 'valor')

    context = {
        'contas': contas,
        'total_contas': total_contas,
    }

    return render(request, 'home.html', context)

def manage(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    total_contas = calcula_total(contas, 'valor')

    for conta in contas:
        conta.banco_nome = ChoicesBancos.get_banco_nome(conta.banco)

    context = {
        'contas': contas,
        'categorias': categorias,
        'total_contas': total_contas,
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
            conta.full_clean()  # Valida o objeto de acordo com as restrições do modelo
            conta.save()
            messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')
        except ValidationError as e:
            messages.add_message(request, constants.ERROR, 'Erro ao cadastrar conta: {}'.format(e))
        except Exception as e:
            messages.add_message(request, constants.ERROR, 'Erro desconhecido: {}'.format(e))

    return redirect('/UserProfile/manage/')


def deletar_banco(request, token):
    if request.method == 'POST':
        conta = Conta.objects.get(token=token)

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