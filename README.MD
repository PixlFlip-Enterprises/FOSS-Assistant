<h1 align="center">FOSS-Assistant</h1>

<p>
  <a href="https://discord.gg/Pvy2HgGE9r">
    <img src="https://img.shields.io/discord/806142446094385153?color=7489d5&logo=discord&logoColor=ffffff" />
  </a>
  <img src="https://img.shields.io/static/v1?label=Status&message=Development&color=blue">
  </a>
</p>

<h2>About</h2>

This repository contains:

-   [FOSS-Assistant API Server](/API_Server)
-   [Documentation](/Documentation)

<h2>Contributing</h2>
As this is more of a personal project for me simply submitting pull requests or opening issues is fine.
Project development is inconsistent at best. If you want to get in touch or coordinate dev work please join the discord.

<h2>Setup</h2>
1. First, pull the repo:
```bash
$ git clone https://github.com/pixlflip/foss-assistant/
```

2. Install the needed Python libraries:
```bash
$ pip install wikipedia
$ pip install discord
$ pip install newspaper3k
$ pip install pymysql
$ pip install Flask
$ pip install Flask_RESTful
```

3. Install MariaDB (debian linux command shown as example):
```bash
$ sudo apt install mariadb-client mariadb-server
```

4. Run the following commands inside the mariadb
```sql
create user 'yourusername'@'localhost' identified by "password";
grant all privileges on * . * to 'yourusername'@'localhost';
exit;
```

5. Run setup.py
```bash
$ python setup.py
```

6. Follow the setup program inputs.


7. Done! Your instance should be fully up and operational. To run the server simply use enter the directory and put the following:
```bash
$ python __main__.py
```