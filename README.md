# Fritill-Clinic Reservation Management System 

<br>

## Table of Contents

- [Fritill-Clinic Reservation Management System](#fritill-clinic-reservation-management-system)
  - [Table of Contents](#table-of-contents)
  - [Important Notes](#important-notes)
  - [About](#about)
    - [Build with](#build-with)
  - [Getting Started](#getting-started)
    - [Prerequisite for smooth installation](#prerequisite-for-smooth-installation)
    - [Installation](#installation)
    - [Post-installation](#post-installation)
    - [Running](#running)
  - [The Available endpoints that are provided by our API](#the-available-endpoints-that-are-provided-by-our-api)
    - [Client endpoints](#client-endpoints)
    - [Appointments endpoints](#appointments-endpoints)

<hr>

## Important Notes
> I am still working on the project, this is not the final verison of it, I just make it public to get feedback and imporve it.

> I want to clarify that i used ubuntu as Operating system, so may some commands don't work if you have another type of OS, so please if some command doesn't run correctly search for the alternative way of performing the same operation for your OS.

<hr>

## About
> Welcome to My project, it's a mimic for a clinic management system to handle reservations and deal with appointments of clients, i built it through doing a hiring task for [Fritill](https://fritill.com/), built with [Django](https://www.djangoproject.com/) for setting up the server-side of the system, used [Django Rest framework](https://www.django-rest-framework.org/) for creating the API endpoints, [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) for managing Json web tokens that is used for user authentication, [PostgreSQL](https://www.postgresql.org/) as DBMS for serving our data, [Bootstrap](https://getbootstrap.com/) for designing the layout of the whole app, [Celery](https://docs.celeryproject.org/en/stable/) and [Redis](https://redis.io/) for sending mails to clients if their appointments would start after 24,6 or 0 hours 

<hr>

### Build with
- [Django](https://www.djangoproject.com/)
- [Django Rest framework](https://www.django-rest-framework.org/)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [PostgreSQL](https://www.postgresql.org/)
- [Bootstrap](https://getbootstrap.com/)
- [Celery](https://docs.celeryproject.org/en/stable/)
- [Redis](https://redis.io/)

<hr>

## Getting Started
> This is an list of needed instructions to set up your project locally, to get a local copy up and running follow these instructuins.

<hr>

### Prerequisite for smooth installation

1. **_Make sure that you are already have python 3 and pip installed in your system_**
```sh
$ python3 --version
$ pip3 --version
```
If not so please download it from here
> [Download python](https://www.python.org/downloads/)
> [Download pip](https://pip.pypa.io/en/stable/installation/)

If you are an ubuntu user, do the following commands
```sh
$ sudo apt update
$ sudo apt -y upgrade
$ sudo apt install -y python3-pip
$ sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
```

<br>

2. **_install python3-venv to manage virtual environments_**

If you are an ubuntu user, do the following commands if not search for how to deal with virtual environments in your OS
```sh
$ sudo apt install -y python3-venv
```

<br>

3. **_install postgreSQL and configure it with the same credentails in `Settings.py` file_**

> [PostgreSQL: Download](https://www.postgresql.org/download/)
> [How to set up Postgres in your Django project](https://dev.to/mungaigikure/how-to-set-up-postgres-in-your-django-project-575i)
> [Databases | Django Documentation](https://docs.djangoproject.com/en/4.0/ref/databases/)

<hr>

### Installation

1. **_Clone the repository_**

```sh
$ git clone 'https://github.com/Suleiman99Hesham/Fritill_Clinic_RMS.git'
```

<br>

2. **_Create a Virtual environment to install our packages in_**
```sh
$ python3 -m venv 'my_env'
```

<br>

3. **_Run your virtual environment_**
```sh
$ source my_env/bin/activate
```

<br>

4. **_Install required packages_**
```sh
$ pip install -r Clinic_RMS/requirements.txt
```

You may face a problem while you are installing psycopg2, if this happened try these commands
```sh
$ sudo apt-get install python3-pip python3-dev libpq-dev
$ pip3 install psycopg2
```

<br>

5. **_Important steps for celery_**
   
to make rescheduled mailing service runs successfuly you have to install radis and celery on ur system, here are the commands

They are included in requirements.txt but too confirm that it's has been installed successfully, follow these commands

> Download the latest stable Redis package and build it.
```sh
$ wget http://download.redis.io/redis-stable.tar.gz
$ tar xzf redis-stable.tar.gz
$ cd redis-stable
$ sudo make install
```
> If celery not installed successfully run this command
```sh
$ pip3 install celery
```

> Also, if it's happened to redis
```sh
$ pip3 install redis
```

>Finally, to run the asynchronous task in the background

First step, we terminate any currently running workers (to make sure that there's no running celery processes in background
```sh
$ pkill -f "celery worker"
```

Or u can To terminate all running Celery processes
```sh
$ kill -9 $(ps aux | grep celery | grep -v grep | awk '{print $2}' | tr '\n'  ' ') > /dev/null 2>&1
```

Then start the service
```sh
$ celery -A Clinic_RMS beat -l info --logfile=celery.beat.log --detach
$ celery -A Clinic_RMS worker -l info --logfile=celery.log --detach
```

Last step, if you wanna see the logs and checks if everything is working well
```sh
$ cat celery.log
```
Or
```sh
$ cat celery.beat.log
```

<hr>

### Post-installation

**_Create a super user to be able to use the system as an admin with having all possible privileges_**
```sh 
$ python manage.py createsuperuser
```
Enter your username, email and password

<hr>

### Running

**_Finally run the server_**
```sh 
$ cd Clinic_RMS
$ python manage.py runserver
```
Open [http://localhost:8000](http://localhost:8000) to use the app.

<hr>


## The Available endpoints that are provided by our API

<br>

### Client endpoints

**_Creating a new client_**
```sh
http://localhost:8000/api/clientCreate/
```
> - The request body should include (name, email, password)
> - The response body would have the client data if it's ceated successfully

<br>

**_Login with Client credentials_**
```sh
http://localhost:8000/api/GetToken/
```
> - Get a `JWT` token for a client to authenticate given his username and password in request body
> - The response body would have the user access and refresh tokens
> - `Access token`: used to authenticate the user and it must be send with every request that require client to be authenticated and it has to be refreshed every 5 minutes with `Refresh token` 
> - `Refresh token`: used to refresh the `Access token` before it has becomed expired and its life span is 90 days

<br>

**_Get new tokens_**
```sh
http://localhost:8000/api/GetToken/refresh/
```
> - The request body should include the `Access token`
> - it Refreshs the `Access token` for client
> - The response body would have a new `Access token` and a new `Refresh token`

<br>

**_Get all clients (only admin allowed)_**
```sh
http://localhost:8000/api/getAllClients/
```
> - The request body should include the `Access token`
> - The response body would have all clients data on the system

<br>

**_Get a client by ID_**
```sh
http://localhost:8000/api/getClientById/<int:id>/
```
> - The request body should include the `Access token`
> - The response body would have the client data

<br>

**_Update a client_**
```sh
http://localhost:8000/api/updateClient/<int:id>/
```
> - The request body should include the `Access token`
> - The request body should have the new specefied data that you want to update
> - The response body would have the client data with the new data

<br>

**_Delete a client (only admin allowed)_**
```sh
http://localhost:8000/api/deleteClient/<int:id>/
```
> - The request body should include the `Access token`
> - The response body would have a message tells you that the client is deleted successfully 

<hr>

### Appointments endpoints

**_Get all appointments (only admin allowed)_**
```sh
http://localhost:8000/api/getAllAppointments/
```
> - The request body should include the `Access token`
> - The response body would have all appointments data on the system

<br>

**_Get a appointment by ID_**
```sh
http://localhost:8000/api/getAppointmentsById/<int:id>/
```
> - The request body should include the `Access token`
> - The response body would have the appointment data

<br>

**_Get all appointments of a client (only admin allowed)_**
```sh
http://localhost:8000/api/getAppointmentsByClient_admin/<int:id>/
```
> - The request body should include the `Access token`
> - On trying to prevent any client from getting the appointments of another client we permit this endpoint only for admin user
> - The response body would have the appointments of the specified client with his id

<br>

**_Get all appointments of authenticated client_**
```sh
http://localhost:8000/api/getApointmentsByClient/
```
> - The request body should include the `Access token`
> - The response body would have the appointments of the authenticated client

<br>

**_Creating a new appointment_**
```sh
http://localhost:8000/api/createAppointment/
```
> - The request body should include (appointment date: datetime field)
> - The response body would have the appointment data if it's ceated successfully

<br>

**_Update an appointment_**
```sh
http://localhost:8000/api/updateAppointment/<int:id>/
```
> - The request body should include the `Access token`
> - The request body should have the new appointment date
> - The response body would have the appointment data

<br>

**_Delete an appointment (only admin allowed)_**
```sh
http://localhost:8000/api/deleteAppointment/<int:id>/
```
> - The request body should include the `Access token`
> - The response body would have a message tells you that the appointment is deleted successfully