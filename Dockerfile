FROM python:2.7
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
ADD etc /etc/
COPY . /app/
WORKDIR /app
RUN python manage.py migrate
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password123')" | python manage.py shell
VOLUME ["/etc/nginx/conf.d", "/etc/nginx/ssl"]
EXPOSE  8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
