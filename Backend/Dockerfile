FROM python:3.11

WORKDIR /srv/wps-backend

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir es-config

CMD [ "python3", "-m" , "flask", "run", "api_server", "--host=0.0.0.0"]
