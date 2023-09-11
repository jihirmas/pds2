from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import auth
from .forms import SignupForm
from django.db import connection
import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
import numpy as np
import io
import base64
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from its.models import User, Tema, Tarea, PreguntaAlternativa, Alternativa, UsuarioTarea, TareaPregunta, Variables



@login_required(login_url='accounts/login')
def index(request):
    cursor = connection.cursor()
    resultados = {}
    
    temas = ["Ecuacion Fundamental", "Péndulo Simple", "Potenciales", "Puntos de Equilibrio", "Osciladores Acoplados"]

    # Consultas de intentos por tema
    for i,tema in enumerate(temas):
        # cursor.execute(f'''SELECT SUM(its_usuariotarea.intentos) AS intentos_totales   
        #                 FROM   its_tarea, its_user, its_usuariotarea, its_tema
        #                 WHERE  its_tarea.id = its_usuariotarea.tarea_id
        #                 AND    its_user.id = its_usuariotarea.usuario_id
        #                 AND    its_tarea.tema_id = its_tema.id
        #                 AND    its_tema.titulo = {repr(tema)}
        #                 AND    its_user.id = {int(request.user.id)};''')
        # row = cursor.fetchone()
        resultados[f"intentos_tema_{i+1}"] = 0#row[0] if row[0] else 0

    # Consultas de tareas por tema
    for i,tema in enumerate(temas):
        # cursor.execute(f'''SELECT COUNT(*)       
        #                 FROM   its_tarea, its_user, its_usuariotarea, its_tema
        #                 WHERE  its_tarea.id = its_usuariotarea.tarea_id
        #                 AND    its_user.id = its_usuariotarea.usuario_id
        #                 AND    its_tarea.tema_id = its_tema.id 
        #                 AND    its_tema.titulo = {repr(tema)}
        #                 AND    its_user.id = {int(request.user.id)};''')
        # row = cursor.fetchone()
        resultados[f"tareas_tema_{i+1}"] = 0#row[0] if row[0] else 0

    # Consulta de puntajes y otros datos del usuario
    # cursor.execute(f'''SELECT its_user.tema1,
    #                         its_user.tema2,
    #                         its_user.tema3,
    #                         its_user.tema4,
    #                         its_user.tema5
    #                     FROM its_user       
    #                     WHERE its_user.id = {int(request.user.id)};''')
    # row = cursor.fetchone()
    for i, tema in enumerate(temas, start=1):
        resultados[f"puntaje_tema_{i}"] = 0#row[i-1]

    return render(request, "its/index.html", resultados)




class CustomLoginView(LoginView):
    template_name = 'login.html'  # Specify the login template

    
def logout(request):
    auth.logout(request)
    return redirect('/')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})



def temas_abiertos(usuario):
    cursor = connection.cursor()
    cursor.execute(f'''
                   select 
                        its_user.tema1,
                        its_user.tema2,
                        its_user.tema3,
                        its_user.tema4,
                        its_user.tema5 
                    from 
                        its_user
                    where 
                        its_user.id = {usuario}
                        ''')
    rows = cursor.fetchone()
    l = []
    for i in range(5):
        if rows[i] != -1:
            l.append(i+1)
    return l


def formar_tarea(tema, usuario):
    
    #se gestiona creacion de tarea
    
    return 1

    
def quiz(request):
    tema = request.GET.get('tema')
    retry = request.GET.get('retry')
    respuestas = request.GET.get('respuestas')
    temas_a = temas_abiertos(auth.get_user(request).id)
    tema = int(tema)
    if tema not in temas_a or tema not in range(1,6):
        return HttpResponseRedirect('/')
    tarea = formar_tarea(tema, request.user.id)
    if retry == "True":
        respuestas = request.GET.get('respuestas', '')
        try:
            respuestas_lista = json.loads(respuestas)
        except json.JSONDecodeError:
            respuestas_lista = [] 
            

    else:
        respuestas_lista = []
        
    
    data_tarea = []
    cursor = connection.cursor()
    cursor.execute(f'''
                    SELECT * 
                    FROM    its_tareapregunta,
                            its_tarea,
                            its_preguntaalternativa
                    WHERE     its_tareapregunta.tarea_id = its_tarea.id
                    AND     its_tareapregunta.pregunta_alternativa_id = its_preguntaalternativa.id
                    AND     its_tarea.id = {tarea};
                        ''')
    rows = cursor.fetchall()
    
    malas = []
    cont = 0
    
    for i in respuestas_lista:
        cursor.execute(f'''
                            SELECT its_alternativa.correcta
                            FROM its_alternativa
                            WHERE its_alternativa.id = {int(i)};
                        ''')
        correcta = cursor.fetchone()
        if correcta[0] == True:
            cont += 1
        else:
            malas.append(int(i))
    preguntas_malas = []
    for i in malas:
        cursor.execute(f'''
                            SELECT its_alternativa.preguntaasociada_id
                            FROM its_alternativa
                            WHERE its_alternativa.id = {int(i)};
                        ''')
        preguntas_malas.append(cursor.fetchone()[0])

    
    for i in rows:

        if int(i[1]) not in preguntas_malas and retry == "True":
            continue
        cursor.execute(f'''
                        SELECT its_alternativa.id,
                                its_alternativa.correcta,
                                its_alternativa.texto,
                                its_alternativa.hint
                            FROM its_alternativa
                            WHERE its_alternativa.preguntaasociada_id = {int(i[1])};
                            ''')
        alternativas = cursor.fetchall()

        alt = []
        for j in alternativas:
            alt.append({"id": int(j[0]), "correcta": j[1], "texto": j[2], "hint": j[3]})
        data_tarea.append({"pregunta_id": int(i[0]), "tarea_id": int(i[2]), "puntaje": int(i[4]), "tipo": i[5], "destacada": i[6], "dificultad": i[7], "enunciado": i[9], "tema": i[10], "alternativas": alt})

    return render(request, "its/quiz.html", {'data_tarea': data_tarea})

def quiz_results(request):
    tema = request.GET.get('tema')
    retry = request.GET.get('retry')
    incorrectas = request.GET.get('incorrectas')
    respuestas = request.GET.get('respuestas', '')
    temas_a = temas_abiertos(auth.get_user(request).id)
    tema = int(tema)
    if tema not in temas_a or tema not in range(1,6):
        return HttpResponseRedirect('/')
    tarea = formar_tarea(tema, request.user.id)
    try:
        respuestas_lista = json.loads(respuestas)
    except json.JSONDecodeError:
        respuestas_lista = [] 
    
    if retry == "True":
        aux = "TRUE"
    else:
        aux = "FALSE"
        
    data_tarea = []
    respuestas_usuario = {}
    cursor = connection.cursor()
    cursor.execute(f'''
                    SELECT * 
                    FROM    its_tareapregunta,
                            its_tarea,
                            its_preguntaalternativa
                    WHERE     its_tareapregunta.tarea_id = its_tarea.id
                    AND     its_tareapregunta.pregunta_alternativa_id = its_preguntaalternativa.id
                    AND     its_tarea.id = {tarea};
                        ''')
    rows = cursor.fetchall()
    malas = []
    cont = 0
    
    for i in respuestas_lista:
        cursor.execute(f'''
                            SELECT its_alternativa.correcta
                            FROM its_alternativa
                            WHERE its_alternativa.id = {int(i)};
                        ''')
        correcta = cursor.fetchone()
        if correcta[0] == True:
            cont += 1
        else:
            malas.append(int(i))
            
    preguntas_malas = []
    preguntas_todas = []
    for i in respuestas_lista:
        cursor.execute(f'''
                            SELECT its_alternativa.preguntaasociada_id
                            FROM its_alternativa
                            WHERE its_alternativa.id = {int(i)};
                        ''')
        resp = cursor.fetchone()
        if i in malas:
            preguntas_malas.append(resp[0])
        preguntas_todas.append(resp[0])
        
    for i in rows:
        if retry == "True":
            if int(i[1]) not in preguntas_todas:
                continue
        
        cursor.execute(f'''
                        SELECT its_alternativa.id,
                                its_alternativa.correcta,
                                its_alternativa.texto,
                                its_alternativa.hint
                            FROM its_alternativa
                            WHERE its_alternativa.preguntaasociada_id = {int(i[1])};
                            ''')
    
        
        alternativas = cursor.fetchall()

        alt = []
        for j in alternativas:
            alt.append({"id": int(j[0]), "correcta": j[1], "texto": j[2], "hint": j[3]})
        data_tarea.append({"pregunta_id": int(i[0]), "tarea_id": int(i[2]), "puntaje": int(i[4]), "tipo": i[5], "destacada": i[6], "dificultad": i[7], "enunciado": i[9], "tema": i[10], "alternativas": alt})
        
    context = {
        'preguntas_y_respuestas': zip(data_tarea, respuestas_lista),
        'retry': aux,
    }
    return render(request, "its/quiz_results.html", context)

def desarrollo_tema_2_a():
    masa = random.randint(2, 5)
    largo = random.randint(2, 5)
    angulo = random.choice([-60,-45,-30,-15,15,30,45,60])
    enunciado = f'''
                Suponga que se tiene un pendulo ideal empotrado en el techo el cual oscila armonicamente con respecto al eje y.
                Este pendulo tiene una masa m = {masa} kg concentrada alfinal del mismo (puede asumir que la barra tiene masa despreciable),
                una longitud del pendulo L = {largo} metros y un angulo a = {angulo} grados, con respecto al eje vertical. Los ejes mostrados muestran una
                cuadricula donde cada cuadrado equivale a 1 metro de distancia. Considere g = 9.81 m/s^2.
                '''
    omega = np.sqrt(9.81/largo)
    periodo = 2*np.pi/omega
    dic = {
        "titulo": "Péndulo Simple",
        "enunciado": enunciado,
        "param1": omega,
        "param2": periodo,
        "enunciadoA" : '¿Cúal es frecuencia de oscilación del péndulo? Resultado en [Hz]',
        "enunciadoB" : '¿Cúal es el periodo de oscilación del péndulo? Resultado en [s]',
        "titulo1" : "Frecuencia: (omega)",
        "titulo2" : "Periodo: (T)",
        "hint1" : "Ecuacion de oscilacion: θΩ^2=θ''",
        "hint2" : "Ecuacion del periodo: T = 2π/Ω",
    }
    params = {
        "masa" : masa,
        "largo" : largo,
        "angulo" : angulo,
    }
    return dic, params
    
def check_value(user_value, correct_value):
    tolerance = correct_value*0.1
    if user_value <= correct_value + tolerance and user_value >= correct_value - tolerance:
        return True
    return False

def desarrollo(request):
    tema = request.GET.get('tema')
    temas_a = temas_abiertos(auth.get_user(request).id)
    tema = int(tema)
    if tema not in temas_a or tema not in range(1,6):
        return HttpResponseRedirect('/')
    data_pregunta, params = desarrollo_tema_2_a()
    grafico = get_graph_pendulo(params["largo"], params["angulo"], params["masa"])
    data_toda = {
        "pregunta": data_pregunta,
        "grafico": grafico,
        "tarea" : 1,
    }
    # UsuarioTarea.objects.create(tarea=1,usuario=auth.get_user(request).id)
    return render(request, "its/desarrollo.html", {'data': data_toda})


def get_graph_pendulo(L,a,m):
    matplotlib.use('agg')
    m = m/10
    g = 9.81 
    theta = np.radians(a)
    text_angle = f"Angle: {a} Degrees"
    
    # Calcular las coordenadas x e y del extremo del péndulo
    x = [0, L * np.sin(theta)]
    y = [0, -L * np.cos(theta)]
    
    # Crear una figura y un eje
    fig, ax = plt.subplots()
    ax.grid(True)
    
    # Dibujar el péndulo como una línea
    circle = Circle((x[1],y[1]), m, color='black')
    l2 = plt.Line2D([0,0], [0,-10], linestyle="--", color="r")
    ax.add_line(l2)
    ax.add_patch(circle)
    
    # Definir el radio del arco
    radius = L-1

    # Definir los ángulos inicial y final del arco (en grados)
    theta_start = -90
    if a > 0:
        theta_end = -90 + a
        theta_start = -90
    else:
        theta_end = -90 
        theta_start = -90 + a

    # Crear el arco
    arc = Arc((0, 0), 2 * radius, 2 * radius, angle=0.0, theta1=theta_start, theta2=theta_end, color='b', lw=2)

    # Agregar el arco al eje
    ax.add_patch(arc)
    
    ax.plot(x, y, marker=' ', color='b', markersize=5, label=text_angle)
    ax.plot(x, y, marker=' ', color='black', markersize=10)
    
    
    # Configurar límites y etiquetas de los ejes
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 0)
    
    ax.legend()
    
    
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    return graphic


@csrf_exempt  # Usar csrf_exempt solo para simplificar; no se recomienda en producción
def procesar_desarrollo(request):
    if request.method == 'POST':
        # Obtén los valores enviados desde el formulario
        
        param1 = float(request.POST.get('param1', 0))
        param2 = float(request.POST.get('param2', 0))
        param1_user = float(request.POST.get('param1_user', 0))
        param2_user = float(request.POST.get('param2_user', 0))
        tarea = int(request.POST.get('tarea', 0))
        
        usuario_tarea = UsuarioTarea.objects.get(usuario=auth.get_user(request).id, tarea=tarea)
        usuario_tarea.intentos += 1
        usuario_tarea.save()

        # Devuelve una respuesta JSON con los resultados de verificación
        response_data = {
            'pregunta1_correcta': check_value(param1_user, param1),
            'pregunta2_correcta': check_value(param2_user, param2),
        }
        return JsonResponse(response_data)

    # Si no es una solicitud POST, puedes manejarlo de acuerdo a tus necesidades
    return JsonResponse({'error': 'Solicitud no válida'})

