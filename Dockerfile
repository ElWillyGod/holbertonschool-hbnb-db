# docker build . -t hbnb-hb && docker run hbnb-hb 

FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk add --no-cache bash && \
  pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000

EXPOSE $PORT

CMD ["gunicorn"]
