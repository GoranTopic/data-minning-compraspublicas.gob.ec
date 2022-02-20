cd compras_publicas_scrapper/

git pull

sudo apt-get install docker.io -y

sudo docker build . -t compras  

sudo docker run -t compras -v output:/output
