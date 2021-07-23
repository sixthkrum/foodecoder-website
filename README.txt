Foodecoder is a website that converts images of food into recipes
It first checks if an image is that of a food item using a deep learning model then extracts the recipe using facebook's inverse-cooking  https://ai.facebook.com/blog/inverse-cooking/
-- You can make an account to store uploaded images and recipes generated from them
-- Alternatively you may upload images anonymously too

This repository only contains the server side code and the front end code, it does not contain the implementation of the models or the helper scripts to interact with them.
This was a group project and that part of the code was not done by me.
All the references and interactions with those scripts has been commented out and dummy values have been put in place instead.
All the files in this repository are authored by me other than static/style/theme.css which is from bootstrap.

The website was originally hosted on an old dell laptop and is no longer online.

Setup instructions:

Name of the flask app is “config.py”
Name of the systemd service is “foodecoder.service”
Name of the uwsgi config file is “foodecoder.ini”

To run locally on an ubuntu(18.04+) machine:
    1. Change paths to your local paths in ”config.py”
    2. Make a python3 virtual environment
    3. Install all the requirements in “requirements.txt” in the environment
    4. From the environment run:
        a. “export FLASK_APP=config.py”
        b. “flask run”

To run on an ubuntu(18.04+) server in a production environment:
    1. Install nginx, uwsgi, python3 and sqlite3
    2. Enable nginx in ufw
    3. Change paths to your local paths in ”config.py”
    4. Make a python3 virtual environment
    5. Install all the requirements in “requirements.txt” in the environment
    6. Add the website configuration file (in the code directory) to /etc/nginx/sites-available and rename the “server_name” variable in the configuration file to your domain name. Change the directory of the root of your website as you want and make a similar directory in the /var/www folder. Make sure to set the permissions of the folder carefully and allow the www-data user access to access the directory (or any other user depending on how you change the nginx configuration)
    7. Make a symbolic link to the file in the /etc/nginx/sites-enabled directory
    8. Use acme.sh to get ssl certificates for your website and fix the directories in the nginx configuration file for these certificates accordingly (The configuration file in the code directory only allows access on port 443, no HTTP connections are allowed. So either run the website on port 80 or install certificates using the DNS entry method of acme.sh)
    9. Edit “foodecoder.service” and “foodecoder.ini” according to your local paths and environment name.
    10. Enable and start the systemd service “foodecoder.service”
    11. Update the DNS records for your domain to point to the IP address of the server
    12. The foodecoder app should now be running on your website

For security:
    1. Deny default incoming connections in ufw
    2. Setup cloudflare and allow only cloudflare IPs to access the server using iptables
    3. Setup a physical firewall
