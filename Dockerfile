FROM python:3.9
RUN apt-get update \
    && apt-get -yy install libmariadb-dev
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ADD requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["flask", "run"] 