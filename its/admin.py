from django.contrib import admin
from its.models import User, Tema, Tarea, PreguntaAlternativa, Alternativa, UsuarioTarea, TareaPregunta, Variables

# Register your models here.
admin.site.register(User)
admin.site.register(Tema)
admin.site.register(Tarea)
admin.site.register(PreguntaAlternativa)
admin.site.register(Alternativa)
admin.site.register(UsuarioTarea)
admin.site.register(TareaPregunta)
admin.site.register(Variables)
