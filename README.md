# Currency Exchange
This Application is a small demonstration of Integrating Third party API (Currency Conversion API) in our web application.

A User when registered will have a personal Wallet to save money, here user can save money in any currency type (example: INR, USD, GBP etc).
user can also change his Currency type. 

Basically the amount in the Wallet supports all the international currency types. So one can add/withdraw/transfer money in any currency value.

### Web Application Features:
1. Registration and login into the Application 
2. User can store the currency in any currency type.
3. User can change his/her wallet default currency type.
4. User can **Add money** to his/her wallet. Any currency type value can be added to Wallet.
5. User can **Withdraw money** from his/her wallet. Any currency type value can be Withdrawn from the wallet.
6. User can **Transfer money** to other users in any type of currency.
7. User can change his/her Profile picture.

###Project details:
Web application is developed using Python Django rest framework, sqlite3, Jquery, bootstrap, CSS, HTML.

Deployed using Docker, Docker-compose, Nginx, uwsgi, supervisord, AWS Ec2.
We can use redis for caching conversion data (which is fetched daily)  

###Currency Exchange Deployment Process:
The Application is deployed on AWS Ec2 machine.
	- Ubuntu Ec2 Instance - t2.micro
	- installed docker.io & docker-compose using user-data script.
		- Userdata script:
			#!/bin/bash
			apt-get update
			apt install docker.io
			apt install docker-compose
	- Added required Security group for server.

On Local :
1. Pull latest Code. 
2. Build the docker using Docker build command.
- Command: `sudo docker build -f Deployment/Dockerfile --no-cache -t ravitejamallozala/projects:curr_exc_app .`
3. Push the new docker image to Docker register.
	- Command: `sudo docker push ravitejamallozala/projects:curr_exc_app`

On Aws server:
1. Pulling new Docker image on server
	Command: `sudo docker pull ravitejamallozala/projects:curr_exc_app`
2. To Run the docker using the latest image using docker compose:

		version: "3.5"
		services:
		  web:
		  	image: "ravitejamallozala/projects:curr_exc_app"
		    build: .
		    ports:
		      - "80:80"

	- with Docker run command:	
    
	Command:` docker run -d -p 0.0.0.0:80:80/tcp -n curr_exc_app ravitejamallozala/projects:curr_exc_app`
	
	- Docker-swarm can be used to pull and deploy the image which makes sure we have zero downtimes while deployement
	- Also Using Ansible playbook we can deploy containers on applciation server and we can also mount volumes so that data can be maintained when new container is deployed.

Ansible Example:
````
---
- hosts: application
  become: yes
  gather_facts: no
  tasks:
  - name: starting Currency Exchange container
    docker_container:
      name: "curr_exc_app"
      image: "ravitejamallozala/projects:curr_exc_app"
      state: started
      recreate: yes
      pull: yes
      restart: yes
    restart_policy: unless-stopped
      ports:
         - "80:80"
      volumes:
         - /data/currency_exchange/media:/opt/app/media 
````
###Improvements in Deployment Process:

- In Ideal case we use CICD  tool such as Jenkins to trigger job whenever new code is merged (as we can integrate with github)
- We build the docker in Jenkins server where new code is pulled and building docker is done.
- New docker image can be pushed to docker registry from where ansible can access and deploy the container in list of servers. We can use Docker swarm to orchestration.
- While deploying we should have Volumes setup for container & NFS can be mounted to server, so that the media files can be saved in NFS (or we can save files directly in S3).
- As we are using sqlite3 and volumes are not set to dockers the db is cleared on every deployment. In normal case we connect to database  which is outside the application docker. 

### Improvements in Development
- As the Conversion API data needs to be updated only once a day we can store the data against
- Unit test cases and Integration Test cases must be written.
- Better UI can be designed.
- Proper testing and Exception Handling can be better. 

