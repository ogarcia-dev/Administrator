FROM python:3.11.4-slim-buster

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

WORKDIR /cephalopodus/administrator

COPY ./requirements.txt /cephalopodus/administrator/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /cephalopodus/administrator/requirements.txt

COPY ./app /cephalopodus/administrator

CMD ["uvicorn", "core:app", "--reload", "--host", "0.0.0.0", "--port", "8002"]