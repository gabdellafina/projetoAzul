from datetime import datetime
from pymongo import MongoClient

class Usuario:
    def __init__(self, nome, cpf, email, telefone, senha):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.criado_em = datetime.now().strftime('%d-%m-%Y %H:%M')  

    def salvar(self):
        client = MongoClient("mongodb+srv://guilhermeaqw24:QecII8Ow51jOOePs@cluster0.zile7.mongodb.net/?retryWrites=true&w=majority")
        db = client['SusBd']
        collection = db['Usuarios'] 

        usuario_data = {
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "telefone": self.telefone,
            "senha": self.senha,  # Não use senha pura em produção
            "criado_em": self.criado_em
        }
        collection.insert_one(usuario_data)

    @staticmethod
    def autenticar(email, senha):
        client = MongoClient("mongodb+srv://guilhermeaqw24:QecII8Ow51jOOePs@cluster0.zile7.mongodb.net/?retryWrites=true&w=majority")
        db = client['SusBd']
        collection = db['Usuarios'] 
        usuario = collection.find_one({"email": email})
        if usuario and usuario['senha'] == senha:
            return True
        return False

from pymongo import MongoClient
from datetime import datetime
class Agendamento:
    def __init__(self, paciente_id, data_horario, especialidade):
        self.paciente_id = paciente_id
        self.data_horario = data_horario
        self.especialidade = especialidade
        self.criado_em = datetime.now().strftime('%d-%m-%Y %H:%M')

    def agendar(self):
        client = MongoClient("mongodb+srv://guilhermeaqw24:QecII8Ow51jOOePs@cluster0.zile7.mongodb.net/?retryWrites=true&w=majority")
        db = client['SusBd']
        collection = db['Consultas']
        consulta_data = {
            "paciente_id": self.paciente_id,
            "data_horario": self.data_horario,
            "especialidade": self.especialidade,
            "status": "pendente",
            "criado_em": self.criado_em
        }
        collection.insert_one(consulta_data)
        print(f"Consulta para o paciente {self.paciente_id} agendada com sucesso!")

class Exame:
    def __init__(self, paciente_id, tipo, resultado, medico_id, data_realizacao):
        self.paciente_id = paciente_id
        self.tipo = tipo
        self.resultado = resultado
        self.medico_id = medico_id
        self.data_realizacao = data_realizacao
        self.criado_em = datetime.now().strftime('%d-%m-%Y %H:%M')  # Formata a data no formato desejado

    def salvar(self):
        client = MongoClient("mongodb+srv://guilhermeaqw24:QecII8Ow51jOOePs@cluster0.zile7.mongodb.net/?retryWrites=true&w=majority")
        db = client['SusBd']
        collection = db['Exames']
        exame_data = {
            "paciente_id": self.paciente_id,
            "tipo": self.tipo,
            "resultado": self.resultado,
            "medico_id": self.medico_id,
            "data_realizacao": self.data_realizacao,
            "criado_em": self.criado_em
        }
        collection.insert_one(exame_data)
        print("Exame cadastrado com sucesso!")

class CarteiraVacina:
    def __init__(self, paciente_id, vacina, data_prevista, status="pendente"):
        self.paciente_id = paciente_id
        self.vacina = vacina
        self.data_prevista = data_prevista
        self.status = status
        self.criado_em = datetime.now().strftime('%d-%m-%Y %H:%M')

    def salvar(self):
        client = MongoClient("mongodb+srv://guilhermeaqw24:QecII8Ow51jOOePs@cluster0.zile7.mongodb.net/?retryWrites=true&w=majority")
        db = client['SusBd']
        collection = db['CarteiraVacinas']
        vacina_data = {
            "paciente_id": self.paciente_id,
            "vacina": self.vacina,
            "data_prevista": self.data_prevista,
            "status": self.status,
            "criado_em": self.criado_em
        }
        collection.insert_one(vacina_data)
        print("Vacina registrada com sucesso!")

class EventoSaude:
    def __init__(self, titulo, descricao, data_evento, local):
        self.titulo = titulo
        self.descricao = descricao
        self.data_evento = data_evento
        self.local = local
        self.criado_em = datetime.now().strftime('%d-%m-%Y %H:%M')

    def salvar(self):
        client = MongoClient("mongodb+srv://guilhermeaqw24:QecII8Ow51jOOePs@cluster0.zile7.mongodb.net/?retryWrites=true&w=majority")
        db = client['SusBd']
        collection = db['EventosSaude']
        evento_data = {
            "titulo": self.titulo,
            "descricao": self.descricao,
            "data_evento": self.data_evento,
            "local": self.local,
            "criado_em": self.criado_em
        }
        collection.insert_one(evento_data)
        print("Evento de saúde registrado com sucesso!")

class EventoSaude:
    def __init__(self, titulo, descricao, data_evento, local):
        self.titulo = titulo
        self.descricao = descricao
        self.data_evento = data_evento
        self.local = local
        self.criado_em = datetime.now().strftime('%d-%m-%Y %H:%M')

    def salvar(self):
        client = MongoClient("mongodb+srv://guilhermeaqw24:QecII8Ow51jOOePs@cluster0.zile7.mongodb.net/?retryWrites=true&w=majority")
        db = client['SusBd']
        collection = db['EventosSaude']
        evento_data = {
            "titulo": self.titulo,
            "descricao": self.descricao,
            "data_evento": self.data_evento,
            "local": self.local,
            "criado_em": self.criado_em
        }
        collection.insert_one(evento_data)
        print(f"Evento '{self.titulo}' registrado com sucesso!")

evento1 = EventoSaude(
    titulo="Campanha de Vacinação Contra a Gripe",
    descricao="Vacinação gratuita para todas as idades. Compareça ao posto de saúde mais próximo.",
    data_evento=datetime(2024, 12, 10, 9, 0),  # Data e hora do evento
    local="Posto de Saúde Central"
)
evento1.salvar()

evento2 = EventoSaude(
    titulo="Feira de Saúde e Bem-Estar",
    descricao="Atendimento médico gratuito, palestras e distribuição de brindes.",
    data_evento=datetime(2024, 12, 15, 8, 30),
    local="Praça da Liberdade"
)
evento2.salvar()