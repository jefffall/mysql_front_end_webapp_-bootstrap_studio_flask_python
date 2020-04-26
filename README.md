# mysql_front_end_webapp_-bootstrap_studio_flask_python
Complete mysql front end for mysql DB queries built with bootstrap studio, python and jQuery

This is not actually a cmdb. This is a front end app which can connect to a mysql database. The app is to be run via Flask from the same server hosting the mySQL db. THere need to be a user1 or some user who can access the database which you want to run mysql commands against. The design can be opened and altered on Bootstrap Studio Version 5.03 or later. The cmdb folder can be placed under your Eclipse 'eclipse-workspace' directory and code edited. The 'pydev' personality for Eclipse has to be installed to properly edit Python in Eclipse.

However, you don't need eclipse to run this program. You need Pythno 3.6 or later. You need to pip install all the inports in the flask_server.py program. Then just run ./flask_server.py provided you change the first line in flask_server.py to point to your Python 3 directory. I have used Active State Python on Apple MacOS Catalina and it works well. Thte first line of flask_server.py has to be like: #!/<path>/python3 or whatever you called your python3.
