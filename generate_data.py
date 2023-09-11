import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pds2.settings')

import django
django.setup()

from faker import Faker
from its.models import User, Tema, Tarea, PreguntaAlternativa, Alternativa, UsuarioTarea, TareaPregunta, Variables

fake = Faker()
#crear admin
User.objects.create_superuser(
    email="admin@example.com",
    first_name="admin",
    last_name="admin",
    role=User.ADMIN,
    password="Admin123",
    tema1=None,
    tema2=None,
    tema3=None,
    tema4=None,
    tema5=None,
)

User.objects.create_user(
    email="student@example.com",
    first_name="student",
    last_name="custom",
    password="Student123",
    role=User.STUDENT,
    tema2 = 0,
    )

User.objects.create_user(
        email="teacher@example.com",
        first_name="teacher",
        last_name="custom",
        password="Teacher123",
        role=User.TEACHER,
        tema1=None,
        tema2=None,
        tema3=None,
        tema4=None,
        tema5=None,
    )

for _ in range(10):  # crear 30 students
    User.objects.create_user(
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        password="Student123",
        role=User.STUDENT,
    )

for _ in range(3): #crear 3 profesores
    User.objects.create_user(
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        password="Teacher123",
        role=User.TEACHER,
        tema1=None,
        tema2=None,
        tema3=None,
        tema4=None,
        tema5=None,
    )
Tema.objects.create(titulo="Ecuacion Fundamental")
Tema.objects.create(titulo="Péndulo Simple")
Tema.objects.create(titulo="Potenciales")
Tema.objects.create(titulo="Puntos de Equilibrio")
Tema.objects.create(titulo="Osciladores Acoplados")


temas = Tema.objects.all()

PreguntaAlternativa.objects.create(enunciado="¿Qué representa la constante k en la ecuación diferencial del oscilador armónico?",tema = temas[0])
PreguntaAlternativa.objects.create(enunciado="¿Cuál es la ecuación diferencial que rige el comportamiento de un oscilador armónico simple?",tema = temas[0])
PreguntaAlternativa.objects.create(enunciado="¿Cuál es la relación entre la frecuencia angular y la constante k en la ecuación diferencial del oscilador armónico?",tema = temas[0])

preguntas_alternativas_todas = PreguntaAlternativa.objects.all()

Alternativa.objects.create(texto="y'' + ky = 0",preguntaasociada=preguntas_alternativas_todas[1],correcta=True)
Alternativa.objects.create(texto="La amplitud de la oscilación",preguntaasociada=preguntas_alternativas_todas[0],correcta=False, hint="La amplitud es la distancia máxima que alcanza el objeto que oscila")

Alternativa.objects.create(texto="y'' - ky = 0",preguntaasociada=preguntas_alternativas_todas[1],correcta=False, hint="y'' es la segunda derivada de y con respecto al tiempo")
Alternativa.objects.create(texto="y' + ky = 0",preguntaasociada=preguntas_alternativas_todas[1],correcta=False, hint="y' es la primera derivada de y con respecto al tiempo")
Alternativa.objects.create(texto="y' - ky = 0",preguntaasociada=preguntas_alternativas_todas[1],correcta=False, hint="y' es la primera derivada de y con respecto al tiempo")

Alternativa.objects.create(texto="ω = k",preguntaasociada=preguntas_alternativas_todas[2],correcta=False, hint="ω es la frecuencia angular")

Alternativa.objects.create(texto="La frecuencia angular de la oscilación",preguntaasociada=preguntas_alternativas_todas[0],correcta=False, hint="La frecuencia angular es la cantidad de oscilaciones que realiza el objeto por unidad de tiempo")
Alternativa.objects.create(texto="La constante de proporcionalidad del resorte",preguntaasociada=preguntas_alternativas_todas[0],correcta=True)
Alternativa.objects.create(texto="La masa del objeto que oscila",preguntaasociada=preguntas_alternativas_todas[0],correcta=False, hint="La masa es la cantidad de materia que posee el objeto que oscila")

Alternativa.objects.create(texto="ω = 1/k",preguntaasociada=preguntas_alternativas_todas[2],correcta=False , hint="ω es la frecuencia angular")
Alternativa.objects.create(texto="ω = √k",preguntaasociada=preguntas_alternativas_todas[2],correcta=True)
Alternativa.objects.create(texto="ω = 1/√k",preguntaasociada=preguntas_alternativas_todas[2],correcta=False, hint="ω es la frecuencia angular")

Tarea.objects.create(
        puntaje=6,
        tipo='A',
        destacada=False,  # 30% de probabilidad de que sea True
        dificultad='Facil',
    )
TareaPregunta.objects.create(tarea=Tarea.objects.all()[0],pregunta_alternativa=PreguntaAlternativa.objects.all()[0])
TareaPregunta.objects.create(tarea=Tarea.objects.all()[0],pregunta_alternativa=PreguntaAlternativa.objects.all()[1])
TareaPregunta.objects.create(tarea=Tarea.objects.all()[0],pregunta_alternativa=PreguntaAlternativa.objects.all()[2])




usuarios = User.objects.all()


for _ in range(4): 
    Tarea.objects.create(
        puntaje=fake.random_int(min=0, max=100),
        tipo=fake.random_element(elements=('A','C')),
        destacada=fake.boolean(chance_of_getting_true=30),  # 30% de probabilidad de que sea True
        dificultad=fake.random_element(elements=('Facil', 'Media', 'Dificil')),
    )
    
        
tareas = Tarea.objects.all()
# print(tareas)
# Crear preguntas de cálculo ficticias


for tarea in tareas:
    for _ in range(5):  # Cambia el número según cuántas preguntas de cálculo desees por tarea
        PreguntaAlternativa.objects.create(
            enunciado=fake.text(max_nb_chars=200),
            tema = fake.random_element(elements=temas),
        )

preguntas_de_alternativas = PreguntaAlternativa.objects.all()

for i,pregunta in enumerate(preguntas_de_alternativas):
    if i in [0,1,2,3]:
        continue
    for i in range(4):
        aux = False
        if i == 3:
            aux = True
        Alternativa.objects.create(
            texto=fake.text(max_nb_chars=200),
            preguntaasociada=pregunta,
            correcta=aux,
        )
        

    
tareas_todas = Tarea.objects.all()
usuarios_todos = User.objects.all()
preguntas_alternativas_todas = PreguntaAlternativa.objects.all()




UsuarioTarea.objects.create(tarea=tareas_todas[0],usuario=usuarios_todos[0])
UsuarioTarea.objects.create(tarea=tareas_todas[0],usuario=usuarios_todos[1])
UsuarioTarea.objects.create(tarea=tareas_todas[0],usuario=usuarios_todos[2])
UsuarioTarea.objects.create(tarea=tareas_todas[1],usuario=usuarios_todos[1])
UsuarioTarea.objects.create(tarea=tareas_todas[1],usuario=usuarios_todos[3])
UsuarioTarea.objects.create(tarea=tareas_todas[0],usuario=usuarios_todos[3])


TareaPregunta.objects.create(tarea=tareas_todas[1],pregunta_alternativa=preguntas_alternativas_todas[4])
TareaPregunta.objects.create(tarea=tareas_todas[1],pregunta_alternativa=preguntas_alternativas_todas[5])
TareaPregunta.objects.create(tarea=tareas_todas[1],pregunta_alternativa=preguntas_alternativas_todas[6])
TareaPregunta.objects.create(tarea=tareas_todas[1],pregunta_alternativa=preguntas_alternativas_todas[7])
TareaPregunta.objects.create(tarea=tareas_todas[2],pregunta_alternativa=preguntas_alternativas_todas[8])
TareaPregunta.objects.create(tarea=tareas_todas[2],pregunta_alternativa=preguntas_alternativas_todas[9])
TareaPregunta.objects.create(tarea=tareas_todas[2],pregunta_alternativa=preguntas_alternativas_todas[10])
TareaPregunta.objects.create(tarea=tareas_todas[2],pregunta_alternativa=preguntas_alternativas_todas[11])
TareaPregunta.objects.create(tarea=tareas_todas[3],pregunta_alternativa=preguntas_alternativas_todas[12])
TareaPregunta.objects.create(tarea=tareas_todas[3],pregunta_alternativa=preguntas_alternativas_todas[13])
TareaPregunta.objects.create(tarea=tareas_todas[3],pregunta_alternativa=preguntas_alternativas_todas[14])
TareaPregunta.objects.create(tarea=tareas_todas[3],pregunta_alternativa=preguntas_alternativas_todas[15])

usuario_tarea_todos = UsuarioTarea.objects.all()
