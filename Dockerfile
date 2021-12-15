FROM python:3.9

RUN apt-get update
RUN pip install --upgrade pip
RUN apt-get -y install gcc
RUN pip install Cython
RUN apt-get update

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e mapping-career-causeways/.

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]