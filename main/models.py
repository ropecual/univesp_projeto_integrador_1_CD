from django.db import models
from datetime import date

class Visitante(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField(blank=True, null=True)
    email = models.EmailField()
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    primeira_visita = models.DateField(default=date.today)
    ultima_visita = models.DateField(default=date.today)

    def __str__(self):
        return self.nome

class MaterialPDF(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    arquivo = models.FileField(upload_to='pdfs/')
    data_upload = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo



class Testemunhos(models.Model):
    nome = models.CharField(max_length=100)
    texto_sobre = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='testemunhos/',blank=True, null=True)


# professor
# aluno
# classe
