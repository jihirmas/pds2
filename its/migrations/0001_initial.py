# Generated by Django 4.2.3 on 2023-09-11 00:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('role', models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')], default='student', max_length=10)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('tema1', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(10, message='El valor maximo es 10'), django.core.validators.MinValueValidator(-1, message='El valor minimo es 0')])),
                ('tema2', models.IntegerField(blank=True, default=-1, null=True, validators=[django.core.validators.MaxValueValidator(10, message='El valor maximo es 10'), django.core.validators.MinValueValidator(-1, message='El valor minimo es 0')])),
                ('tema3', models.IntegerField(blank=True, default=-1, null=True, validators=[django.core.validators.MaxValueValidator(10, message='El valor maximo es 10'), django.core.validators.MinValueValidator(-1, message='El valor minimo es 0')])),
                ('tema4', models.IntegerField(blank=True, default=-1, null=True, validators=[django.core.validators.MaxValueValidator(10, message='El valor maximo es 10'), django.core.validators.MinValueValidator(-1, message='El valor minimo es 0')])),
                ('tema5', models.IntegerField(blank=True, default=-1, null=True, validators=[django.core.validators.MaxValueValidator(10, message='El valor maximo es 10'), django.core.validators.MinValueValidator(-1, message='El valor minimo es 0')])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PreguntaAlternativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enunciado', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje', models.IntegerField(default=0)),
                ('tipo', models.CharField(max_length=200)),
                ('destacada', models.BooleanField(default=False)),
                ('dificultad', models.CharField(choices=[('FACIL', 'Facil'), ('MEDIA', 'Media'), ('DIFICIL', 'Dificil')], default='MEDIA', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Variables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=500)),
                ('min_val', models.IntegerField(blank=True, null=True)),
                ('max_val', models.IntegerField(blank=True, null=True)),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='its.tarea')),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='its.tema')),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioTarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intentos', models.IntegerField(default=0)),
                ('puntaje_obtenido', models.IntegerField(default=0)),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='its.tarea')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TareaPregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta_alternativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='its.preguntaalternativa')),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='its.tarea')),
            ],
        ),
        migrations.AddField(
            model_name='preguntaalternativa',
            name='tema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='its.tema'),
        ),
        migrations.CreateModel(
            name='Alternativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correcta', models.BooleanField(default=False)),
                ('texto', models.CharField(max_length=500)),
                ('hint', models.CharField(blank=True, max_length=500, null=True)),
                ('preguntaasociada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='its.preguntaalternativa')),
            ],
        ),
    ]
