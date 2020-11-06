FROM ubuntu:18.04

COPY requirements_docker.txt /

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update

RUN apt-get --assume-yes install python3-pip

RUN apt-get --assume-yes install git-all

RUN pip3 install --trusted-host pypi.python.org -r requirements_docker.txt

RUN git clone -b dev https://github.com/toms3t/Propalyzer.git

COPY secret.py /Propalyzer/propalyzer_site/propalyzer_app/

COPY settings.py /Propalyzer/propalyzer_site/propalyzer_site/

COPY wsgi.py /Propalyzer/propalyzer_site/propalyzer_site/

RUN cd Propalyzer/propalyzer_site

RUN git config --global user.email tomset@gmail.com

RUN git config --global user.name "Tom Setliffe"

EXPOSE 80

WORKDIR Propalyzer/propalyzer_site

COPY startup.sh /Propalyzer/propalyzer_site/

RUN python3 manage.py makemigrations propalyzer_app

RUN python3 manage.py migrate

RUN python3 manage.py collectstatic --noinput

CMD ["./startup.sh"]
