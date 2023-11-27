FROM python:3.11-alpine
WORKDIR /animal-scanner-backend
ADD requirements.txt .
RUN pip install -r requirements.txt
COPY  main.py docker/config/config.ini logger_config.ini ./
COPY ../src src
EXPOSE 8080
CMD ["python3", "main.py", "config.ini", "logger_config.ini"]