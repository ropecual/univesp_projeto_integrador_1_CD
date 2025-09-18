# cursos/models.py

from django.db import models
from django.contrib.auth.models import User

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)


    def __str__(self):
        return self.titulo

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=200)
    # A ordem em que os módulos aparecerão
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f'{self.curso.titulo} - {self.titulo}'

class Conteudo(models.Model):
    TIPO_CONTEUDO_CHOICES = (
        ('video', 'Vídeo'),
        ('pdf', 'PDF'),
    )
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='conteudos')
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CONTEUDO_CHOICES)
    # Para o vídeo, vamos armazenar a URL do vídeo (pode ser do YouTube, Vimeo, etc.)
    url_video = models.URLField(blank=True, null=True)
    # Para o PDF, vamos usar o FileField, assim como já fazíamos
    arquivo_pdf = models.FileField(upload_to='cursos/pdfs/', blank=True, null=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return self.titulo