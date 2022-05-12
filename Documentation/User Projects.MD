<h1 align="center">FOSS-Assistant</h1>

<p>
  <a href="https://discord.gg/Pvy2HgGE9r">
    <img src="https://img.shields.io/discord/806142446094385153?color=7489d5&logo=discord&logoColor=ffffff" />
  </a>
  <img src="https://img.shields.io/static/v1?label=Status&message=Development&color=blue">
  </a>
</p>

<h2>User Projects Documentation</h2>

This file contains the following information
- How the Table is structured
- Details on how each parameter functions
- General parameters for using table
- Adding new fields to the table
- Important notes for protection and security
- Known issues and thoughts on future development

<h2>Table Structure</h2>
The Profile Table has the following structure

| Place | Name        | Data Type          |  Nullable?  |
|-------|-------------|--------------------| ------------|
| 0     | KEY         | INT AUTO_INCREMENT | NOT NULL    |
| 1     | PROFILE_ID  | VARCHAR(50)        | NOT NULL    |
| 2     | PROJECT_ID  | VARCHAR(50)        | NULL        |
| 3     | DATE        | VARCHAR(50)        | NULL        |
| 4     | DATA_ORIGIN | VARCHAR(200)       | NULL        |
| 5     | DATA_FORMAT | MEDIUMTEXT         | NULL        |
| 6     | DATA_LOG    | MEDIUMTEXT         | NULL        |

The table above is designed to allow what is more or less long term project data storage
with virtually no reliance on hardcoded data, or more simply put it will allow any user of
an instance to create a project, label data via json format, and safely store that data
for easy retrieval and use at a later time. The first two variables are a composite key. 
The next field (PROJECT_ID) is a unique identifier for the user's project. The next field
is a date which, while it is not hardcoded and could be different things, is mostly just
designed to be a datetime string put in by FOSS-Assistant instead of SQL. The final three are
what makes this table unique. The DATA_ORIGIN field can be anything from the title of a note
to a serial number of a device recording data. It will vary per project but will always be
retrieved as a string and will be treated as one by the code. The DATA_FORMAT field is meant
to hold either a JSON file, or alternatively a long set of data that is not the data proper.
The honor of housing the real data goes to DATA_LOG, which is meant to and can only hold JSON
formatted string sequences. To repeat, DATA_LOG CANNOT BE USED TO HOUSE ANYTHING BUT JSON. 


<h2>Updating Table Data</h2>
With the ideal setup this database will be Mariadb or Mongodb, so for easiest modification
simply pull up either in terminal or using a GUI program (such as Beekeeper Studio) the table
and update that way. When doing this ensures the program is offline and a data backup has been
made. This can be done from FOSS Assistant or manually by running a sql dump.

<h2>Adding New Data Fields To The Table</h2>
1. First ensure the program is offline and a backup has been made. 
2. Go to setup.py and add your field to the end of the Profile creation line (currently line 79).
3. Check all relevant files for use of data as it pertains to data and update.
4. Update this file with your new data type as shown in the table above.
5. Go to the updatedb.py file and follow the steps it gives you.
6. Congratulations, you've added a new data field to the Assistant without breaking all the existing code!