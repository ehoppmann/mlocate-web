# mlocate-web
A very simple Python web application that offers a web interface for searching a system's filesystem by name using locate / mlocate. 

## Requirements:
* Python3 (developed using 3.5.2)
* Flask (developed using 0.11 installed in a venv with pip)
* A linux distribution with locate/mlocate set up (developed on Ubuntu 16.04)

## Installing and running, in short:
* Clone to local filesystem
* cd to directory
* `python3 app.py`
* **For detailed instructions, with autostart and using gunicorn to serve the webapp, see below screenshot**

## Screenshot

![ScreenShot](screenshot.png?raw=true "Screenshot")

## Set up as system service on ubuntu 16.04
* `git clone https://github.com/eric11/mlocate-web.git`
* `cd mlocate-web`
* `sudo apt-get install python3-pip`
* `pip3 install virtualenv`
* `virtualenv venv`
* `source venv/bin/activate`
* `pip3 install -r requirements.txt`
* `pip3 install gunicorn`
* Create the file `/etc/systemd/system/gunicorn.service` with this content:
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
PIDFile=/run/gunicorn/pid
User=<USER YOU WANT THIS TO RUN AS - SUGGEST LIMITED USER>
Group=<GROUP YOU WANT THIS TO RUN AS>
WorkingDirectory=<BASE DIRECTORY - WHERE YOU CLONED TO>
ExecStart=<BASE DIRECTORY - WHERE YOU CLONED TO>/venv/bin/gunicorn --workers 3 -b 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
```
* `systemctl start gunicorn`
* `systemctl enable gunicorn`

The search service should now be available on port 8000 and will automatically start with the system.
