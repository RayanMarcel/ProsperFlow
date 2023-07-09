from django.shortcuts import render, redirect
from UserProfile.models import Categoria
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from django.contrib.messages import constants

def define_planning(request):
    categorias = Categoria.objects.all()

    context = {
        'categorias': categorias,
    }

    return render(request, 'planning.html', context)

@csrf_exempt
def update_value_category(request, token):
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(token=token)
    categoria.valor_planejamento = novo_valor
    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso!')
    return JsonResponse({'status': 'Sucesso'})

def consultation_planning(request):
    categorias = Categoria.objects.all()

    context = {
        'categorias': categorias
    }

    return render(request, 'consultation_planning.html', context)