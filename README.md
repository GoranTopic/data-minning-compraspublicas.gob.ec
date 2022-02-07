# Compras Publicas Scrapper 

  

##### Hello there.  

This project is an example of the [Selenium](https://www.selenium.dev/)  and [Scrapy](https://scrapy.org/) framework working together. Because the target website uses Ajax and XML to render dynamic HTML content, Scrapy alone is not able to extract the data rendered and presented dynamically by the JavaScript library. Selenium, on the other hand, uses the engine of a web-browser and thus it is able to run the JavaScript code rending all the generated dynamic values. However, the downside to Selenium is that is it slow. When it comes to scrapping lager amounts of pages and data it becomes unfeasible and time consuming to render every response. Also, Selenium interaction with the server is very high-level; any changes made to the front-end code would 'break' the Selenium script, prompting the need to rewrite them. 

There is no perfect implementation, but leveraging the two framework strengths and weaknesses we can have a solution where we have the compatibility of Selenium with the speed, parallelism and efficiency of Scrapy. 

Selenium is able to handle the login an authentication of the website. It is able to talk with the server with the dynamic generated content, and catch any hidden authorization, techniques such as hidden cookies. While Scrappy is able to follow up those request making Requests directly to the Backend API for the statis values in the database. I am able to get Selenium to login in and capture the user session, cookies, CSRF tokens and headers. Once Selenium has been able to authenticated, it is able to use the website’s front-end framework dynamic functions to ask the server for a list of all the project's ID. 

The target server orders it database with a unique primary key ID value for every project it has. 

Once we have a list of the ID’s there is no need for dynamic content to be requested or generated. I pass on all the headers, cookies and tokens to Scrapy so that the server would be none the wiser. Then we can query the backend API directly using the Project ID to extract the Projects information. We get the information and save it in a tree structure of the projects. While it took painstaking amount of calibration to recreate the same types of requests between the two frame works, I was able to make this work in the end. I have added a docker file along with the Firefox Gecko-driver, for greater compatibility between operating systems.  

  
## How to Download this Project 

You can download this GitHub repository by either using the command line or by using the GitHub website. To download with the command line, you must run have Git installed and run: 

`git clone git@github.com:GoranTopic/compras_publicas_scrapper.git` 

This will download a copy of this repository to your working directory. You can also download a zip copy with the Download button on this repository: 

![github_download](https://github.com/GoranTopic/compras_publicas_scrapper/blob/master/assets/github_download.png)  

## How to Running this Project 

Write in the comand line:

`cd compras_publicas_scrapper` 
or click on the folder: ‘compras_publicas_scrapper' to enter the home directory of this folder 

To run this scraper, you have to create a file called ".env" in the home directory for this project. Be careful to enable extensions in Windows, so that you don’t accidently create a file called “.env.txt”. The ".env" file must have the following format:  

``` 
DEST_FOLDER=output 
HEADLESS=1 
RUC=ruc_number 
USER=username 
PASS=password 
``` 

Where you must fill in the RUC number, username and password with your information. 

**Note** that the values for DEST_FOLDER and HEADLESS **must** be `output` and `1` respectably for the project to work in a Docker container on a Windows machine. 

## Running on Linux 

After you have the file ‘.env’ in the 'compras_publicas_scrapper' directory you can run it on Linux with the start.py script.  

`python3 start.py' 

and then running:  

`scrapy crawl compras` 

## Running on Windows 

To run this script on Windows you must first install Docker. Head over to the official Docker [website](https://www.docker.com/products/docker-desktop) to download the latest version of docker of windows. 

Once installed open the CMD line and go the project home directory. 

Run the command `Docker build -t compras .` 
![](https://github.com/GoranTopic/compras_publicas_scrapper/blob/master/assets/build_docker_image.png)
After that you must open the docker app and go to images, where you will be able to see the image you have just build.  
![](https://github.com/GoranTopic/compras_publicas_scrapper/blob/master/assets/docker_image.png)
Click on the run button ‘run’ on the image 
In optional setting fill in:

- The container name. This can anything you want, expect that it must not contain spaces.  
- The destination where you want to the scrapped Data to be send to. This can be any folder most convent for you. 
- The directory inside the container where the file will be written to. This MUST be '/output'. 

![](https://github.com/GoranTopic/compras_publicas_scrapper/blob/master/assets/host_continer_path.png)
Then run the container. You can inspect the standard output of the scraper on the Docker app.  
![](https://github.com/GoranTopic/compras_publicas_scrapper/blob/master/assets/container_inspecting.png)
And be able to see it file in the directory you have chosen. 
![](https://github.com/GoranTopic/compras_publicas_scrapper/blob/master/assets/files_in_desktop.png)
If you have encountered any problems do not heisted to contact me.  
