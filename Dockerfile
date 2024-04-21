FROM python:3.12 

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN rm config/settings.toml

COPY config/settings.prod.toml config/settings.toml

EXPOSE 5000

CMD ["flask", "run"]