from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (ADMIN, 'Admin'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    tema1 = models.IntegerField(default=0, blank=True, null=True, validators=[
            MaxValueValidator(10, message="El valor maximo es 10"),
            MinValueValidator(-1, message="El valor minimo es 0"),
            ]
    )
    tema2 = models.IntegerField(default=-1, blank=True, null=True, validators=[
            MaxValueValidator(10, message="El valor maximo es 10"),
            MinValueValidator(-1, message="El valor minimo es 0"),
            ]
    )
    tema3 = models.IntegerField(default=-1, blank=True, null=True, validators=[
            MaxValueValidator(10, message="El valor maximo es 10"),
            MinValueValidator(-1, message="El valor minimo es 0"),
            ]
    )
    tema4 = models.IntegerField(default=-1, blank=True, null=True, validators=[
            MaxValueValidator(10, message="El valor maximo es 10"),
            MinValueValidator(-1, message="El valor minimo es 0"),
            ]
    )
    tema5 = models.IntegerField(default=-1, blank=True, null=True, validators=[
            MaxValueValidator(10, message="El valor maximo es 10"),
            MinValueValidator(-1, message="El valor minimo es 0"),
            ]
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

class Tema(models.Model):
    titulo = models.CharField(max_length=200)
    
class Tarea(models.Model):
    puntaje = models.IntegerField(default=0)
    tipo = models.CharField(max_length=200)
    destacada = models.BooleanField(default=False)
    FACIL = "FACIL"
    MEDIA = "MEDIA"
    DIFICIL = "DIFICIL"
    DIFICULTAD_OPCIONES = [
        (FACIL, "Facil"),
        (MEDIA, "Media"),
        (DIFICIL, "Dificil"),
    ]
    dificultad = models.CharField(
        max_length=7,
        choices=DIFICULTAD_OPCIONES,
        default=MEDIA,
    )
    

class PreguntaAlternativa(models.Model):
    enunciado = models.CharField(max_length=500)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    
class Alternativa(models.Model):
    correcta = models.BooleanField(default=False)
    texto = models.CharField(max_length=500)
    preguntaasociada = models.ForeignKey(PreguntaAlternativa, on_delete=models.CASCADE)
    hint = models.CharField(max_length=500, blank=True, null=True)
    
class TareaPregunta(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    pregunta_alternativa = models.ForeignKey(PreguntaAlternativa, on_delete=models.CASCADE)

class UsuarioTarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    intentos = models.IntegerField(default=0)
    puntaje_obtenido = models.IntegerField(default=0)

class Variables(models.Model):
    nombre = models.CharField(max_length=500)
    min_val = models.IntegerField(blank=True, null=True)
    max_val = models.IntegerField(blank=True, null=True)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    

