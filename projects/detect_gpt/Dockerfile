FROM python:3.9

WORKDIR /app

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install git -y
RUN apt-get -y install libgl1-mesa-glx

RUN git clone https://github.com/IDEA-Research/GroundingDINO.git

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install Cython
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/GroundingDINO

RUN pip install -e .
RUN mkdir /app/GroundingDINO/weights
WORKDIR /app/GroundingDINO/weights
#RUN wget -q https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth


COPY . .