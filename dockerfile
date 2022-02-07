FROM ubuntu:20.04

WORKDIR /.

# update apt
RUN apt update -y
RUN apt upgrade -y

#  need properties
RUN apt install software-properties-common -y

# install python 
RUN apt install python3.8 -y
RUN apt install python3-pip -y

# install firefox 
RUN apt install firefox -y

RUN apt install vim -y

# install scrapy requirements
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN mv geckodriver /bin/

CMD [ "python3", "-m" , "scrapy", "crawl",  "compras"]
