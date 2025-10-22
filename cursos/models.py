# cursos/models.py

from django.db import models
from django.contrib.auth.models import User


class Curso(models.Model):
	titulo = models.CharField(max_length=200)
	descricao = models.TextField(blank=True)
	alunos = models.ManyToManyField(User, related_name='cursos_inscritos', blank=True)

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
	url_video = models.URLField(blank=True, null=True)
	arquivo_pdf = models.FileField(upload_to='cursos/pdfs/', blank=True, null=True)
	ordem = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['ordem']

	def __str__(self):
		return f'{self.modulo.titulo} - {self.titulo}'


class Comentario(models.Model):
	conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE, related_name='comentarios')
	autor = models.ForeignKey(User, on_delete=models.CASCADE)
	texto = models.TextField()
	data_criacao = models.DateTimeField(auto_now_add=True)

	# Campo para respostas (comentários aninhados)
	resposta_para = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respostas')

	class Meta:
		ordering = ['data_criacao']  # Ordena os comentários do mais antigo para o mais novo

	def __str__(self):
		return f'Comentário de {self.autor.first_name} em {self.conteudo.titulo}'