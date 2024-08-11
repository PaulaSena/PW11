from django.shortcuts import render, redirect
from .models import Empresas
from django.contrib import messages
from django.contrib.messages import constants
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.cache import cache

# Create your views here.def cadastrar_empresa(request):

def cadastrar_empresa(request):
    cache_key = f'form_cadastrar_empresa{request.user.id}'

    if request.method == "GET":
         # Tenta recuperar os dados salvos no cache
        form_data = cache.get(cache_key, {})  # Inicializa form_data como um dicionário vazio se o cache estiver vazio

        return render(request, 'cadastrar_empresa.html', {
            'tempo_existencia': Empresas.tempo_existencia_choices, 
            'area': Empresas.area_choices,
            'form_data': form_data
            })
    elif request.method == "POST":
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        site = request.POST.get('site')
        tempo_existencia = request.POST.get('tempo_existencia')
        descricao = request.POST.get('descricao')
        data_final = request.POST.get('data_final')
        percentual_equity = request.POST.get('percentual_equity')
        estagio = request.POST.get('estagio')
        area = request.POST.get('area')
        publico_alvo = request.POST.get('publico_alvo')
        valor = request.POST.get('valor')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')
        
# Salva os dados no cache
        cache.set(cache_key, {
            'nome': nome,
            'cnpj': cnpj,
            'site': site,
            'tempo_existencia': tempo_existencia,
            'descricao': descricao,
            'data_final': data_final,
            'percentual_equity': percentual_equity,
            'estagio': estagio,
            'area': area,
            'publico_alvo': publico_alvo,
            'valor': valor,
        }, timeout=300)  # 5 minutos de timeout        
        
        if not nome:
            messages.add_message(request, constants.ERROR, 'O campo Nome é obrigatório.')
            return redirect('/empresarios/cadastrar_empresa')

        if not cnpj or len(cnpj) != 14:
            messages.add_message(request, constants.ERROR, 'CNPJ inválido. O CNPJ deve conter 14 dígitos.')
            return redirect('/empresarios/cadastrar_empresa')

        if not site or not site.startswith('http'):
            messages.add_message(request, constants.ERROR, 'URL do site inválida. Deve começar com http:// ou https://.')
            return redirect('/empresarios/cadastrar_empresa')

        if data_final:
            data_final_date = timezone.datetime.strptime(data_final, "%Y-%m-%d").date()
            if data_final_date < timezone.now().date():
                messages.add_message(request, constants.ERROR, 'A data final não pode ser anterior ao dia atual.')
                return redirect('/empresarios/cadastrar_empresa')

        if not estagio:
            messages.add_message(request, constants.ERROR, 'Você deve selecionar pelo menos um estágio.')
            return redirect('/empresarios/cadastrar_empresa')
        if percentual_equity:
            try:
                percentual_equity = float(percentual_equity)
                if percentual_equity <= 0:
                    messages.add_message(request, constants.ERROR, 'O percentual de equity deve ser maior que 0.')
                    return redirect('/empresarios/cadastrar_empresa')
            except ValueError:
                messages.add_message(request, constants.ERROR, 'Percentual de equity inválido.')
                return redirect('/empresarios/cadastrar_empresa')

        if valor:
            try:
                valor = float(valor)
                if valor <= 0:
                    messages.add_message(request, constants.ERROR, 'O valor da captação deve ser maior que 0.')
                    return redirect('/empresarios/cadastrar_empresa')
            except ValueError:
                messages.add_message(request, constants.ERROR, 'Valor de captação inválido.')
                return redirect('/empresarios/cadastrar_empresa')

        if pitch and pitch.size > 10 * 1024 * 1024:  # Limite de 10MB
            messages.add_message(request, constants.ERROR, 'O arquivo de pitch deve ter no máximo 10MB ex: mp4.')
            return redirect('/empresarios/cadastrar_empresa')

        if logo and logo.size > 5 * 1024 * 1024:  # Limite de 5MB
            messages.add_message(request, constants.ERROR, 'O arquivo de logo deve ter no máximo 5MB ex: jpeg, png.')
            return redirect('/empresarios/cadastrar_empresa')

        try:
            empresa = Empresas(
                user=request.user,
                nome=nome,
                cnpj=cnpj,
                site=site,
                tempo_existencia=tempo_existencia,
                descricao=descricao,
                data_final_captacao=data_final,
                percentual_equity=percentual_equity,
                estagio=estagio,
                area=area,
                publico_alvo=publico_alvo,
                valor=valor,
                pitch=pitch,
                logo=logo
            )
            empresa.full_clean()

            empresa.save()
            # Limpa os dados do cache após salvar
            cache.delete(cache_key)
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/empresarios/cadastrar_empresa')
        
        messages.add_message(request, constants.SUCCESS, 'Empresa criada com sucesso')
        return redirect('/empresarios/cadastrar_empresa')