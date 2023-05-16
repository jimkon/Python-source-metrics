FROM python:3.8.16-slim

RUN apt-get update && apt-get install git -y

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . ./app
WORKDIR app
RUN pip install -e .

CMD [ "flask", "--debug", "run", "--host=0.0.0.0"]
