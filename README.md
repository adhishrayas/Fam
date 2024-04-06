# Fam Task

Task to fetch Youtube videos on football asynchronously every 10 seconds, save them in the DB,and display them on a dashboard.

## Installation
Ensure that your machine has Python installed and has a strong internet connection.

Open this Repo in your IDE and install a virtualenv using the command of your choice, I used the one below
```bash
virtualenv foo
```

Then in your terminal,go the newly created virtualenv folder, go to scripts, and type in activate to activate the virtualenv.
Then go to the main directory and you should see "requirements.txt" and "manage.py", run the below command to install all the necessary packages.

```bash
pip install -r requirements.txt
```
After this is done, install redis on your machine from [here](https://github.com/tporadowski/redis/releases).(Download the .msi package)

After downloading it, open the downloaded file and follow the instructions to install.


Lastly, make database migrations by using these 2 commands in the first terminal:-  
```bash
python manage.py makemigrations
```
and then  
```bash
python manage.py migrate
```

Voila! You are ready to go
## Usage
Now you need to open 3 different terminals on your IDE.  
All 3 terminals should have the virtual environment up and running.  
You should also be in the directory that contains "manage.py" in all 3.

Now in the first terminal, run the below command to make a superuser so that you can access the admin panel:-  
```bash
python manage.py createsuperuser
```
Follow the instructions to create your superuser.(Remember the Email and Password!)
Then run the below command to start the server.
```bash
python manage.py runserver
```

In the second terminal, run the below command to start the celery worker:-  
```bash
celery -A youtube.celery worker --pool=solo -l INFO
```

In the last terminal, run the below command to start the celery scheduled job.

```bash
celery -A youtube beat -l INFO
```
 If all goes well to this point, you should see the celery beat scheduling a task every 10 seconds in the 3rd terminal.

The second terminal will have the celery worker printing "haha" and "hehe", denoting the success of the endeavor.

Whereas the first terminal should show you the server running.

Now open your local server(Usually:- http://127.0.0.1:8000/) to see the Latest Football related Videos!

To take a better look at the stored data and the task data, you can go to http://127.0.0.1:8000/admin and log in with your superuser credentials.

Thanks for your time!
## License

[MIT](https://choosealicense.com/licenses/mit/)