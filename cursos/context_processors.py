# cursos/context_processors.py

def cursos_matriculados(request):
    if request.user.is_authenticated:
        return {'cursos_matriculados': request.user.cursos_inscritos.all()}
    return {'cursos_matriculados': []}