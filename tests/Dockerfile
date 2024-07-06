FROM alpine:3.20.1

RUN apk add --no-cache python3 py3-pip

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --break-system-packages -r \
  requirements.txt

COPY . .

EXPOSE 5000
EXPOSE 8000

CMD ["./runall.py", "flask"]
