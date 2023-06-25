# Event Management API

This is a simple Event Management API.
This application uses Oauth2 for authentication.
Below documentation assumes application is running in a localhost environment
***Postman collection and API documentation(available inside postman collection) is available in GitHub repository***

## System Setup

 1. Clone this repository
 2. Create a ``.env`` file in root directory add following keys in ``.env`` file
	```
	DJANGO_SECRET
	DB_NAME
	DB_USERNAME
	DB_PASSWORD
	DB_HOST	
	```
 3. Build and run the docker container
	```
	docker build -t event_management .
	docker run -p 8000:8000 event_management
	```
## Application Setup
Once your docker is up and running, First thing we need to do is create an application for Oauth2. To do this follow below steps
 1. Create a superuser for django admin site. ``python manage.py createsuperuser``
 2. Login into django admin site in your browser ``http://localhost:8000/admin/login/?next=/oauth2/applications/``
 3. Once you land into ``/oauth2/applications/`` page, create an application. During filling application detail, copy `Client id` and `Client secret`. Select client type as `confidential` and Authorization grant type as `Resource owner password-based`. Click on Save button.

## Authorization Process
**Generate Token**
`curl -X POST -d "grant_type=password&username=<user_name>&password=<password>" -u"<client_id>:<client_secret>" http://localhost:8000/oauth2/token/`

**Refresh Token**
`curl -X POST -d "grant_type=refresh_token&refresh_token=<your_refresh_token>&client_id=<your_client_id>&client_secret=<your_client_secret>" http://localhost:8000/oauth2/token/`

