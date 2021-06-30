# Currency Exchange
#### Web Application Url: http://3.108.171.229/
This Application is a small demonstration of Integrating Third-party API (Currency Conversion API) in our web application.

A User when registered will have a personal Wallet to save money, here the user can save money in any currency type (example: INR, USD, GBP etc).
user can also change his Currency type. 

Basically, the amount in the Wallet supports all the international currency types. So one can add/withdraw/transfer money in any currency value.

### Web Application Features:
1. Registration and login into the Application 
2. User can store the currency in any currency type.
3. User can change his/her wallet default currency type.
4. User can **Add money** to his/her wallet. Any currency type value can be added to Wallet.
5. User can **Withdraw money** from his/her wallet. Any currency type value can be Withdrawn from the wallet.
6. User can **Transfer money** to other users in any type of currency.
7. User can change his/her profile picture.

### Project details:
The web application is developed using Python Django rest framework, sqlite3, Jquery, bootstrap, CSS, HTML.

Deployed using Docker, Docker-compose, Nginx, uwsgi, supervisord, AWS Ec2.
We can use Redis for caching conversion data (which is fetched daily)  

### Improvements in Development
- As the Currency exchange API data needs to be updated only once a day we can store the data against a Standard currency type (INR/USD) in a database table.
- We can also store the frequent access data in a cache such as Redis. 
- Unit test cases and Integration Test cases must be written.
- Better UI can be designed.
- Testing and Exception Handling can be more precise. 


### Currency Exchange Deployment Process:
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
1. Pull the latest Code. 
2. Build the docker using Docker build command.
- Command: `sudo docker build -f Deployment/Dockerfile --no-cache -t ravitejamallozala/projects:curr_exc_app .`
3. Push the new docker image to the Docker register.
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
	
	- Docker-swarm can be used to pull and deploy the image which makes sure we have zero downtimes while deployment
	- Also Using Ansible playbook we can deploy containers on application server and we can also mount volumes so that data can be maintained when new container is deployed.

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
### Improvements in Deployment Process:

- In Ideal case, we use a CICD  tool such as Jenkins to trigger job whenever new code is merged (as we can integrate with GitHub)
- We build the docker in the Jenkins server where new code is pulled and building docker is done.
- New docker image can be pushed to the Docker registry from where ansible can access and deploy the container in the list of servers. We can use Docker-swarm for orchestration.
- While deploying we should have Volumes set up for the container & NFS can be mounted to the server so that the media files can be saved in NFS (or we can save files directly in S3).
- As we are using sqlite3 and volumes are not set to dockers the DB is cleared on every deployment. In a normal case, we connect to a database which is outside the application docker. 

### Scenario
If the number of requests would increase on the server. Suggest
the ways in which the system would be able to handle the increased number of requests in
the most optimised way.

=> Firstly, the main bottleneck in the current application is hitting third party API to get the currency conversion data, to overcome that we can have a table that gets updated daily once with the conversion values.

=> We can use Redis to cache the frequently accessed data.

=> If we are hosting in AWS we can use Autoscaling to increase the resources, as we are using dockers adding new resources will be seamless.
