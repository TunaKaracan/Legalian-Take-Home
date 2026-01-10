FROM python:3.11-slim

WORKDIR /opt/legalian

COPY ./requirements.txt /opt/legalian/requirements.txt
COPY ./app /opt/legalian/app

RUN pip install --no-cache-dir --upgrade -r /opt/legalian/requirements.txt

ENV PORT=8000
CMD ["fastapi", "run", "app/main.py"]