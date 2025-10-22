#!/bin/sh

# Aguarda o banco de dados estar pronto
echo "Aguardando o banco de dados..."
sleep 10  # Espera 10 segundos para o MariaDB inicializar

# Aplica as migrações do banco de dados
echo "Aplicando migrações..."
python manage.py migrate --noinput

# Coleta arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Cria o superusuário (se não existir)
echo "Criando superusuário (se necessário)..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='administrador').exists():
    User.objects.create_superuser('administrador', 'admin@example.com', 'A123456b')
    print('Superusuário "administrador" criado.')
else:
    print('Superusuário "administrador" já existe.')
EOF

# Inicia o servidor de desenvolvimento do Django
echo "Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000