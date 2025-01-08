from django.shortcuts import render, redirect, get_object_or_404
from .models import AntiSala, SalaCofre, SalaEnergia, SalaTelecom, RegistroGeral
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.utils import DataError
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.dateparse import parse_date
from pytz import timezone as pytz_timezone
from datetime import datetime   

def ignore_favicon(request):
    return HttpResponse(status=204)
# Função auxiliar para verificar se o usuário é gerente
def is_manager(user):
    return user.groups.filter(name='Gerenciamento').exists()

# View para exibir os registros de gerenciamento (apenas para gerentes)
def gerenciamento_registros(request):
    registros = RegistroGeral.objects.all().order_by('-data_criacao')

    # Define o fuso horário de São Paulo
    fuso_br = pytz_timezone('America/Sao_Paulo')

    # Ajusta a data de criação dos registros para o fuso horário correto
    for registro in registros:
        if registro.data_criacao:
            registro.data_criacao = registro.data_criacao.astimezone(fuso_br)

    # Filtragem por data
    data_filtrada = request.GET.get('data')
    if data_filtrada:
        try:
            data_filtrada_obj = datetime.strptime(data_filtrada, "%Y-%m-%d").date()
            registros = registros.filter(data_criacao__date=data_filtrada_obj)
        except ValueError:
            registros = registros.none()

    # Paginação
    paginator = Paginator(registros, 12)
    page_number = request.GET.get('page')
    registros = paginator.get_page(page_number)

    return render(request, 'app/gerenciamento_registros.html', {'registros': registros})

 
# View para login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciais inválidas. Verifique seu login.')
            return redirect('login')
    
    return render(request, 'app/login.html')

# View para logout
def logout_view(request):
    logout(request)
    return redirect('login')

# View para a home
@login_required
def home(request):
    return render(request, 'app/home.html')

# View para registrar salas
@login_required
def registrar_sala(request, tipo_sala):

    if request.method == 'POST':
        observation = request.POST.get('observation')
        temperature = request.POST.get('temperature')
        limpeza = request.POST.get('limpeza')
        image = request.FILES.get('image')
        
        try:
            if tipo_sala == 'antisala':
                sala = AntiSala(observation=observation, temperature=temperature, limpeza=limpeza, image=image)
                tipo_sala_registro = 'ANTISALA'
            elif tipo_sala == 'salacofre':
                sala = SalaCofre(observation=observation, temperature=temperature, limpeza=limpeza, image=image)
                tipo_sala_registro = 'COFRE'
            elif tipo_sala == 'salaenergia':
                sala = SalaEnergia(observation=observation, temperature=temperature, limpeza=limpeza, image=image)
                tipo_sala_registro = 'ENERGIA'
            elif tipo_sala == 'salatelecom':
                sala = SalaTelecom(observation=observation, temperature=temperature, limpeza=limpeza, image=image)
                tipo_sala_registro = 'TELECOM'
            else:
                messages.error(request, "Tipo de sala inválido.")
                return redirect('home')

            sala.save(user=request.user)

        except DataError:
            messages.error(request, "O texto na observação é muito longo. Reduza o tamanho e tente novamente.")
            return redirect(request.path_info)

        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao salvar os dados: {e}")
            return redirect('home')
        
        messages.success(request, "Registro salvo com sucesso!")
        return redirect('home')
    
    template_name = f'app/{tipo_sala}.html'
    return render(request, template_name)

# View para deletar registros
@login_required
def deletar_registro(request, registro_id):
    registro = get_object_or_404(RegistroGeral, id=registro_id)
    try:
        registro.delete()  # Exclui diretamente; o sinal post_delete fará o resto.
        messages.success(request, "Registro excluído com sucesso!")
    except Exception as e:
        messages.error(request, f"Erro ao excluir o registro: {e}")
    return redirect('home')