# Karma

Sync UGVLE assignment with Google Calender

## Setup

### Step 1 - Generate ```credentials.json```
A ```credentials.json``` file from a Google Cloud Platform project is needed to used the Calender API.

1. Create a new Google Cloud Platform project (https://console.cloud.google.com/projectcreate).
2. Goto APIs & Services > Credentials
3. Create a 'OAuth2 Client ID' from 'CREATE CREDENTIALS'
4. Select 'Desktop App' as the application type and enter a name for the credentials
5. Finish creation using 'CREATE'
6. Download the credentials and move it to the ```karma``` directory

> Note: ```Google Calender API``` should be enabled from the console's API library.

### Step 2 - Configure the environment

Use ```setup.py``` to create an environment for scripts to be run.

1. Change permissions of ```setup.sh```
```sh
sudo chmod 755 setup.sh
```

2. Run the ```setup.sh```
```sh
./setup.sh
```

### Step 3 - Configure run script
Run ```karma``` scripts using ```run.sh```.

1. Create ```run.sh```
```sh
cp run.sh.sample run.sh
```

2. Change ```<username>``` and ```<password>``` inside ```run.sh``` to UGVLE username and password respectively

3. Change permissions of ```run.sh```
```sh
sudo chmod 755 run.sh
```

4. Run the ```run.sh```
```sh
./run.sh
```

### Step 4 (Optional) - Setup a cron job

Setup up a cron job to run ```run.sh``` in intervals to automatically sync assignments with Google Calender.

Check out [how to create a cron job](https://help.ubuntu.com/community/CronHowto).

----------

## License
```
"THE BEER-WARE LICENSE"

<mail@udesh.xyz> wrote this files. As long as you retain this 
notice you can do whatever you want with this stuff. If we meet
some day, and you think this stuff is worth it, you can buy me 
a beer in return.

Udesh Kumarasinghe
```

---------

## Author

Udesh Kumarasinghe – [@ThatUdeshUK](https://twitter.com/ThatUdeshUK)



