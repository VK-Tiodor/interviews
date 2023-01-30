FROM python

RUN pip install Flask

WORKDIR /reportesApi
COPY . .
ENV PORT=8000
EXPOSE 8000

CMD python ./flaskApi.py