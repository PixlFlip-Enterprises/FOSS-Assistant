<h1 align="center">FOSS-Assistant</h1>

<p>
  <a href="https://discord.gg/Pvy2HgGE9r">
    <img src="https://img.shields.io/discord/806142446094385153?color=7489d5&logo=discord&logoColor=ffffff" />
  </a>
  <img src="https://img.shields.io/static/v1?label=Status&message=Development&color=blue">
  </a>
</p>

<h2>API Server Documentation</h2>

The API Server runs using the REST Protocol, meaning simple requests can be made to it with the
usual operators of GET, POST, DELETE, and PATCH. In the case of this project things are categorized
in such a way that you only have to call a base and page then send a JSON from there (Example:
yourhost.com/journal is the address to send a journal request to). This makes it easy to follow
the logical flow of the program, and keeps functional use for both home run instances as well
as enterprise use.

Example API Call (Using Python requests library)
```
response = requests.get("http://127.0.0.1:5000/journal", json={"session_token": "active session using REST", "date": "2022-09-16"})
```

Example Error Return JSON
```
{"status": "Failed", "error_msg": "Not Specified"}
```

Example API Command Call
```
{"session_token": "token from login verification. From what I understand REST compliant", "argument1": "value1"}
```

