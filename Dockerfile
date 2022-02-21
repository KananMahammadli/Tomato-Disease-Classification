# we are using python-3.9 image from dockerhub
FROM python:3.9
# changing working directory 
WORKDIR /app
# we first copy requirements, upgrade pip to the latest version and install packages
# then copy the left of the files, it makes rebuild faster if necessary
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
# running our app
CMD ["python3", "app.py"]