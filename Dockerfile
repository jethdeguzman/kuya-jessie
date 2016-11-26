FROM python:2.7
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
ADD etc /etc/
COPY . /app/
WORKDIR /app
RUN python manage.py migrate
VOLUME ["/etc/nginx/conf.d", "/etc/nginx/ssl"]
EXPOSE  8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
