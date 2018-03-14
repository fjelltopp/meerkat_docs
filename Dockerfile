FROM python:3.6.3

RUN mkdir /var/www

WORKDIR /var/www

RUN apt-get update && apt-get install -y texlive latexmk
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["bash"]
