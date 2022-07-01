# frejun

1. This Project is helpful for management of a team. 
2. Only Users can add team and tasks.
3. Anyone can check team details, users and team-leaders can edit the task details. Once task is created, an email is sent
to the team leader of the associated team with task details.
4. Get api in /tasks gives info of all tasks
5. Team members can only update the status of task

#### This project uses Django as the backend in the project and all APIs for POST and PATCH must be hit by postman or simillar applications. 
#### Uses Celery as async-background task.

# Steps to use:

Installed Python 3 required. This project uses version ```3.10.4```. Needs GIT installed.
## Open the terminal 
Install virtualenv
~~~
pip install virtualenv
~~~
Create a virtualenv
~~~
virtualenv venv
~~~
Move to the recently created directory using 
~~~
cd venv
~~~
Clone this repository.
~~~
 $ git clone https://github.com/VINAAAYYY/Vinay_02-07-2022_9462903474
~~~
Activate your virtual enviroment 
~~~
myenv\Scripts\activate
~~~
Install all dependencies of the project
~~~
pip install -r requirements.txt
~~~
Although the sqlite database is pushed still migrate files just for the sake of it.
~~~
 python manage.py makemigrations
 python manage.py migrate
~~~
Create a super user. Enter your details so that you have the admin controls.
~~~
 python manage.py createsuperuser
~~~ 
Start the server
~~~
python manage.py runserver
~~~
This starts the server in 8000 port.
You can visit `/admin` extention for the Django admin panel of this project.
