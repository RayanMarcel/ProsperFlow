from django.shortcuts import render, redirect
from UserProfile.models import Conta, Categoria
from .models import Valores
from django.contrib.messages import constants
from django.contrib import messages
from decimal import Decimal
from datetime import datetime
from django.template.loader import render_to_string
import os
from django.conf import settings
from django.http import FileResponse
from weasyprint import HTML
from io import BytesIO

def new_value(request):
    if request.method == "GET":
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        
        context = {
            'contas': contas, 
            'categorias': categorias
        } 
        return render(request, 'extrato.html', context)
    elif request.method == "POST":
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')
        
        valores = Valores(
            valor=valor,
            categoria_id=categoria,
            descricao=descricao,
            data=data,
            conta_id=conta,
            tipo=tipo,
        )

        valores.save()

        conta = Conta.objects.get(id=conta)

        valor = Decimal(valor)

        if tipo == 'E':
            conta.valor += valor
            fluxo = "Entrada"
        else:
            conta.valor -= valor
            fluxo = "Saída"

        conta.save()

        messages.add_message(request, constants.SUCCESS, f'{fluxo} cadastrada com sucesso')
        return redirect('/extract/new_value')
    
def view_extract(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    valores = Valores.objects.filter(data__month=datetime.now().month)
    
    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')

    if conta_get:
        valores = valores.filter(conta__id=conta_get)
    if categoria_get:
        valores = valores.filter(categoria__id=categoria_get)

    context = {
        'valores': valores,
        'contas': contas,
        'categorias': categorias
    }

    return render(request, 'view_extrato.html', context)

def export_pdf(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    
    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato_pdf.html')
    path_output = BytesIO()

    context = {
        'valores': valores,
        'contas': contas,
        'categorias': categorias
    }

    template_render = render_to_string(path_template, context)
    HTML(string=template_render).write_pdf(path_output)

    path_output.seek(0)
    

    return FileResponse(path_output, filename="extrato.pdf")