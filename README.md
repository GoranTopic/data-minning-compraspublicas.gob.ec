# Compras Publicas Scrapper

Hello there. 

This proect is a exmaple of Selenium and scrapy working together. 

Becust of the ajax and XML nature of the taget website, Scrapy alone would not be able to access the DOM being create by Javascript.
Selenium uses the engeing of a webbroser and thus it is able to run the JavaScript and render all the dynamic value being generated.
However the downside to selenium is that is it slow, and scrapping lage about of page and data becomes unfeasable and time consuming.
Also any change to the fronot end code woudld 'break' the selerium script and be in need of fixing. 

Levergain the two frameowrk we can have a solution where, Selenium handles the authetifucation and Srapy does the, well, scrapping.

once we have made a script fo Selenium to autheticate, we can pass on the cookies, headers, csrf token to scrapy.

every get request scrappy makes to the backend api woudd autheticated and accepted, thus allowing us to use scrappies paralleismin to quic

## Downloading the project

You can download this git repositoy by eighterusing the command line or by using the github website. 

To download with the comand line you must run have github installed and run:

`git clone git@github.com:GoranTopic/compras_publicas_scrapper.git`

this will donwload a copy of this repository to working directory.
 
you can alternatibly download a zip copy with the Download button on this repository:




## Running the Scrapper
Run 

`cd compras_publicas_scrapper`

or click on the foldercompras_publicas_scrapper'

to enter thr home directory of this folder


To run this scrapper you will need a file called ".env" in the home directory for this project.

".env" must have the following format: 

```
DEST_FOLDER=output
HEADLESS=1
RUC=ruc_number
USER=username
PASS=password
```

Where you must fill in the ruc number, username and password.
Note that the values for DEST_FOLDER and HEADLESS must be `oputput` and `1` for the script to work in a Docker container on in Windows machine.

## Running on Linux
After you have the file .evn in the 'compras_publicas_scrapper' you can run it on linux by running the start.py script. 

`python3 start.py'

and then running: 

`scrapy crawl compras`

 
## Running on Windows

To run this script on Windows you must set up a Docker container first. Head over to the docker [website](https://www.docker.com/products/docker-desktop) to donwload th latest version of docker fo windows.

Once installed open the CMD line and go the the project home directoy.

run the command `Docker build -t compras .`

after that you must open the docker app and go to images

Click on the run 'button' ont he image

the fill in the filed:
1.- the container name, this cna anything you want, cannot have spaces. 
2.- the destination where you want to the scrapped file to be written in you computer.
3.- the directory inside the container where the file will be written to. This MUST be '/output'

the run the contatin. 

should be able to inspect it progress

and be able to see it file in the directory you have choosen

