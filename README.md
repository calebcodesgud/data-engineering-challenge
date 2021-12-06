# How to run

0. this project was build with python 3.8. run:
```buildoutcfg
pip install -r requirements.txt
```

1. Download and install postgresql for windows from here https://get.enterprisedb.com/postgresql/postgresql-14.1-1-windows-x64.exe
```buildoutcfg
username: postgres
password: password
```
2. Add the PostgreSQL bin directory path to the PATH environmental variable.

3. in windows terminal run:
```buildoutcfg
psql -U postgres
```
and enter your password

4. in the postgresql command line run
```buildoutcfg
CREATE DATABASE myDatabase WITH ENCODING 'UTF8' LC_COLLATE='English_United States' LC_CTYPE='English_United States';
\quit
```
5. in the windows terminal run 
```buildoutcfg
pg_ctl -D "<path to postgres data dir>/data" start
```

6. run setUpDb.py in the project directory to create the tables

7. run main.py

8. in the windows terminal run 
```buildoutcfg
pg_ctl -D "<path to postgres data dir>/data" stop
```

Note: if you run into issues running the webdriver, please install the most recent version of chrome. this requires chrome version 96.*

it's also possible you may have to add the line
```buildoutcfg
host  	all  		all 		0.0.0.0/0 		md5
```
to the end of data/pg_hba.conf in you postgres install. I was having issues connection from the application and i don't really know if this helped or not...