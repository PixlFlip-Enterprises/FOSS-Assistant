<h1 align="center">FOSS-Assistant</h1>

<p>
  <a href="https://discord.gg/Pvy2HgGE9r">
    <img src="https://img.shields.io/discord/806142446094385153?color=7489d5&logo=discord&logoColor=ffffff" />
  </a>
  <img src="https://img.shields.io/static/v1?label=Status&message=Development&color=blue">
  </a>
</p>

<h2>User Profile Documentation</h2>

This file contains the following information
- How the Table is structured
- How to update Profile data safely
- Adding new fields to Profile table
- Removing fields from Profile table

<h2>Table Structure</h2>
The Profile Table has the following structure

| Place   | Name     | Data Type          |  Nullable?  |
| ------- | ------------- | --------      | ------------|
| 0       | USER          | VARCHAR(50)   | NOT NULL    |
| 1       | PASSWORD      | VARCHAR(50)   | NOT NULL    |
| 2       | EMAIL         | VARCHAR(50)   | NULL        |
| 3       | EMAILPASS     | VARCHAR(50)   | NULL        |
| 4       | DISCORD       | VARCHAR(20)   | NULL        |

<h2>Updating Profile Table Data</h2>
With the ideal setup this database will be Mariadb or Mongodb, so for easiest modification
simply pull up either in terminal or using a GUI program (such as Beekeeper Studio) the table
and update that way. When doing this ensure the program is offline and a data backup has been
made. This can be done from FOSS Assistant or manually by running a sql dump.

<h2>Adding New Data Fields To Profile</h2>
1. First ensure the program is offline and a backup has been made. 
2. Go to setup.py and add your field to the end of the Profile creation line (currently line 79).
3. in User.py go to the Profile object constructor and simply add a new variable for you data to be held in and a function to use it with.
4. Update this file with your new data type as shown in the table above.
5. Go to the updatedb.py file and follow the steps it gives you.
6. Congratulations, you've added a new data field to the Assistant without breaking all the existing code!