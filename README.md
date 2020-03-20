Recordings Engineering Test
---------------------------
This document will guide you through how to setup and test the Recordings Engineering 
Test. First, you will need to install some dependencies and then run the automated
test to verify the installation was successful. This guide will then explain how to
do the manual tests of the application. The application was built on Ubuntu 18.04 
using Django and the Django Rest Framework with a SQLite3 databse and Celery for 
the recording threads. 

Installation
------------
You will first need to setup a `pipenv` virtual environment before the dependencies 
can be installed. If you don't have it already, it can be installed running:
```bash
$ pip install pipenv
```
Once you have installed, navigate to the project folder and run:
```bash
$ pipenv --python 3.7
```
Next, you will need to activate the virtual environment and install all the required
packages:
```bash
$ pipenv shell
$ pipenv update
```
Aside from the Python packages, you will also need Redis. You can find installation
details [here](https://redis.io/topics/quickstart).

Running the server
------------------
To verify that everything is working, you can start the Django server and the run
all the API tests. Make sure you are in the project root folder, and then run:
```bash
$ python manage.py runserver
```
Following that, open up a new terminal window and run the tests:
```bash
$ python manage.py test recording.test_views
```

API
---
Below are is the API spec for the recording server. You can run these commands to
interact with the API and create, read, update or delete your own data.

**Create a new channel**
```bash
POST http://127.0.0.1:8000/api/channel/
```
Here is an example of the POST data that needs to be included.
```json
{
    "channel": {
        "name": "My Channel",
        "keyname": "my-channel",
        "channel_type": "radio",
        "url": "http://www.myradio.com"
    }
}
```

**View channel details**
```bash
GET http://127.0.0.1:8000/api/channel/<channel_id>/
```
The `channel_id` is the database primary key of the channel. Data will be returned
in the same JSON format as shown above. 

Tip: If you navigate to the above address in your browser, you will be provided with
a convenient interface to interact with the API.

**Update a channel**
```bash
PUT http://127.0.0.1:8000/api/channel/<channel_id>/
```

**Delete a channel**
```bash
DELETE http://127.0.0.1:8000/api/channel/<channel_id>/
```

**View a recording**
```bash
GET http://127.0.0.1:8000/api/recording/<recording_id>/
```
This gets the details of a single recording with the follow response:
```json
{
    "recording": {
        "channel": 1,
        "start_time": "2020-03-18T13:45:28.556889Z",
        "end_time": "2020-03-18T13:45:55.215624Z",
        "path": "radio/za-jozi-01/za-jozi-01_server01_20200318_134528.aac"
    }
}
```
The `channel` value above is the channel ID of the channel on which the recording
took place.

**View all recordings for a channel**
```bash
GET http://127.0.0.1:8000/api/recording/<recording_id>/
```
This gets all of the recordings that were performed on a channel
```json
{
    "recordings": [
        {
            "channel": 6,
            "start_time": "2020-03-18T13:45:28.556889Z",
            "end_time": "2020-03-18T13:45:55.215624Z",
            "path": "radio/za-jozi-01/za-jozi-01_server01_20200318_134528.aac"
        },
        {
            "channel": 6,
            "start_time": "2020-03-18T13:45:48.556046Z",
            "end_time": "2020-03-18T13:46:15.126754Z",
            "path": "radio/za-jozi-01/za-jozi-01_server01_20200318_134548.aac"
        },
        {
            "channel": 6,
            "start_time": "2020-03-18T13:46:08.567983Z",
            "end_time": "2020-03-18T13:46:35.017172Z",
            "path": "radio/za-jozi-01/za-jozi-01_server01_20200318_134608.aac"
        }
    ]
}
```
Once you have familiarised yourself with the API, you are now ready to use the
recording server! 

Tip: For convenience, you can also view and update your database using the Django
Admin at `127.0.0.1:8000/admin/`

Making Recordings
-----------------
Before we can make recordings, we need to run the Celery worker and Celery Beat
schedule that coordinates the recordings. Please make sure all of the commands below 
are executed within the project root directory. We use Redis as the message broker for
our tasks. Start Redis by running:
```bash
redis-server
```

Before starting up Celery, make sure that your Django server is running. Also make sure
that each of your commands are executed within your pipenv virtual environment.
 
Open up a new terminal window and run the following:
```bash
celery -A recording worker -l info --concurrency=4
```
The concurrency is the number of threads that the worker will be able to execute.
Please note that this has only been tested on a machine that has 4 CPU threads. As
such, the number of recording threads was limited to only 2 channels which each have up
to 2 threads each. You may include any number of threads that you have available. Next, start 
the Beat schedule by running the following in a new terminal window:
```bash
celery -A recording beat --loglevel=info
```
If you have any Channels in database, the tasks will automatically start doing the
recordings every 20 seconds with a 10 second overlap. You can find your recordings
in the `recording_files` directory.

If you add a new channel, it will start recording on the next beat cycle and will
continue until you delete the channel. You may stop the recordings by simply cancelling
the Celery Beat schedule process. 

Contact
-------
Email: flyholmes@gmail.com

GitHub: danielgholmes


