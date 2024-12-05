from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from pymongo import MongoClient
from .models import Usuario, Agendamento

# Create your views here.

def index(request):
    return render(request, 'home.html')

def perfil(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            email = request.POST.get('email')
            senha = request.POST.get('senha')

            client = MongoClient("mongodb+srv://<user>:<password>@cluster0.mongodb.net/")
            db = client['SusBd']
            collection = db['Usuarios']
            usuario = collection.find_one({"email": email, "senha": senha})
            
            if usuario:
                redirect('index')
            else:
                return HttpResponse("Credenciais inválidas!")

        elif 'cadastro' in request.POST: 
            nome = request.POST.get('nome')
            cpf = request.POST.get('cpf')
            email = request.POST.get('email')
            telefone = request.POST.get('telefone')
            senha = request.POST.get('senha')

            novo_usuario = Usuario(nome, cpf, email, telefone, senha)
            novo_usuario.salvar()
            return HttpResponse("Cadastro realizado com sucesso!")  # Substitua por um redirecionamento

    return render(request, 'perfil.html')

import folium
from django.shortcuts import render

def locais(request):
    # Localização central de Praia Grande-SP
    lat = float(request.GET.get('lat', -24.0055))
    lng = float(request.GET.get('lng', -46.4025))

    m = folium.Map(location=[lat, lng], zoom_start=13)

    unidades_saude = {
        "hospitais": [
            {"nome": "Hospital Irmã Dulce", "lat": -24.004556222801185, "lng": -46.4183997084837},
            {"nome": "Hospital Casa de Saúde Praia Grande", "lat": -24.014098, "lng": -46.411474},

        ],
         "usafas": [
            {"nome": "USAFA Aviação", "lat": -24.009396618187683, "lng": -46.439828998380925},
            {"nome": "USAFA Caiçara", "lat": -24.04449941676632, "lng": -46.52826988930517},
            {"nome": "USAFA Boqueirão", "lat": -24.002212237812085, "lng": -46.410733713148495},
            {"nome": "USAFA Tupi", "lat": -24.020088221797177, "lng": -46.460944663847094},
            {"nome": "USAFA Guilhermina", "lat": -24.006267859296443, "lng": -46.42758453777006},
            {"nome": "USAFA Ocian", "lat": -24.02230571516768, "lng": -46.4751918887121},
        ],
        "upas": [
            {"nome": "UPA Samambaia", "lat": -24.03779011832355, "lng": -46.524508783611424},
            {"nome": "UPA Quietude", "lat": -24.018270224867912, "lng": -46.4760144443424},
        ],
    }

    for tipo, locais in unidades_saude.items():
        if tipo == "hospitais":
            cor = "red"
        elif tipo == "usafas":
            cor = "blue"
        elif tipo == "upas":
            cor = "green"

        for local in locais:
            folium.Marker(
                location=[local["lat"], local["lng"]],
                popup=local["nome"],
                icon=folium.Icon(color=cor),
            ).add_to(m)

    # Salva o mapa em HTML
    locais = m._repr_html_()
    return render(request, 'locais.html', {'locais': locais})

def marcar_consulta(request):
    if request.method == "POST":
        cpf = request.POST.get("cpf")
        especialidade = request.POST.get("especialidade")
        data = request.POST.get("data")

        if not cpf or not especialidade or not data:
            messages.error(request, "Todos os campos são obrigatórios.")
            return render(request, "marcar_consultas.html")

        try:
            agendamento = Agendamento(
                paciente_id=cpf,
                data_horario=data,
                especialidade=especialidade,
            )
            agendamento.agendar()
            messages.success(request, "Consulta marcada com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao marcar consulta: {e}")

    return render(request, "marcar_consulta.html")

def consultar_exames(request):
    exames = []

    if request.method == "POST":
        cpf = request.POST.get("cpf")

        if not cpf:
            messages.error(request, "Por favor, insira o CPF para consultar os exames.")
            return render(request, "consultar_exames.html", {"exames": exames})

        try:
            # Conexão com o MongoDB
            client = MongoClient("mongodb+srv://guilhermeaqw24:QecII8Ow51jOOePs@cluster0.zile7.mongodb.net/?retryWrites=true&w=majority")
            db = client['SusBd']
            collection = db['Exames']

            exames = list(collection.find({"paciente_id": cpf}))

            if not exames:
                messages.warning(request, "Nenhum exame encontrado para o CPF informado.")
        except Exception as e:
            messages.error(request, f"Erro ao consultar exames: {e}")

    return render(request, "consultar_exames.html", {"exames": exames})

def consultar_calendario(request):
    eventos = []

    if request.method == "POST":
        cpf = request.POST.get("cpf")

        if not cpf:
            messages.error(request, "Por favor, insira o CPF para consultar o calendário.")
            return render(request, "consultar_calendario.html", {"eventos": eventos})

        try:
            client = MongoClient("mongodb+srv://guilhermeaqw24:QecII8Ow51jOOePs@cluster0.zile7.mongodb.net/?retryWrites=true&w=majority")
            db = client['SusBd']

            consultas = list(db['Consultas'].find({
                "cpf": cpf,
                "data": {"$gte": datetime.now()}
            }))

            exames = list(db['Exames'].find({
                "paciente_id": cpf,
                "data_realizacao": {"$gte": datetime.now().strftime('%Y-%m-%d')}
            }))

            # Formatar os eventos
            for consulta in consultas:
                eventos.append({
                    "tipo": "Consulta",
                    "especialidade": consulta["especialidade"],
                    "data": consulta["data"].strftime('%d/%m/%Y'),
                    "descricao": f"Consulta de {consulta['especialidade']}"
                })

            for exame in exames:
                eventos.append({
                    "tipo": "Exame",
                    "especialidade": exame["tipo"],
                    "data": exame["data_realizacao"],
                    "descricao": f"Exame de {exame['tipo']}"
                })

            eventos = sorted(eventos, key=lambda x: x["data"])
        except Exception as e:
            messages.error(request, f"Erro ao consultar o calendário: {e}")

    return render(request, "consultar_calendario.html", {"eventos": eventos})

