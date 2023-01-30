FROM ubuntu

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install python3
RUN apt-get install python3-pip
RUN pip install Flask

WORKDIR /reportesApi
COPY ./src .
ENV PORT=8080
EXPOSE 8080

CMD python ./flaskApi.py