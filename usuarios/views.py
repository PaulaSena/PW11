from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth

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
  
# Criando uma classe usuario para criar um novo usuario
    user = User.objects.create_user(username=username, password=senha)
    messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
    return redirect('/usuarios/cadastro')

    return HttpResponse(f'{username} - {senha} - {confirmar_senha}')

   # if messages==SUCCESS:
     #   return redirect('/usuarios/login')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        senha = request.POST.get("senha")
# Autenticar usuario import auth
        user = auth.authenticate(request, username=username, password=senha)
        if user:
            auth.login(request,user)
            return redirect('/empresarios/cadastrar_empresa')
        messages.add_message(request, constants.ERROR,"Usuário ou senha invalidos")
        return redirect("/usuarios/login")
