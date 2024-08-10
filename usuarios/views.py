from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
# Create your views here.


def cadastro(request):
   #print (request.method)
   # print(request.POST)

    if request.method == "GET":
        return render(request,'cadastro.html')
    elif request.method == "POST":
       username = request.POST.get("username")
       senha = request.POST.get("senha")
       confirmar_senha = request.POST.get("confirmar_senha")
     
# If confirmar senha
    if senha != confirmar_senha:
      #  print(1)
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem.')
        return redirect('/usuarios/cadastro')
# If confirmar senha menos de 6 digitos
    if len(senha)<6:
       # print('2')
        messages.add_message(request, constants.ERROR, 'A senha precisa ter ao menos 6 digitos.')
        return redirect('/usuarios/cadastro') 

# Criando um filtro para validar se usuario já cadastrado no banco
    users = User.objects.filter(username=username)
    if users.exists():
       # print(3)
        messages.add_message(request, constants.ERROR, 'Já existe usuário com esse username.')
        return redirect('/usuarios/cadastro')
  
# criando uma classe usuario para criar um novo usuario
    user = User.objects.create_user(username=username, password=senha)
    messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
    return redirect('/usuarios/login')
          
    return HttpResponse(f'{username} - {senha} - {confirmar_senha}')

def login(request):
    messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
    return render(request, 'login.html')