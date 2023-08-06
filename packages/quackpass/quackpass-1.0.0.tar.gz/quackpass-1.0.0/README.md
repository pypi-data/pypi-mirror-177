## QuackPass

World's most secure password thingle thangle.

### Setup

```
pip install quackpass
```

You need to be using a version greater then 3.6 for this library to work. 

### Usage

CODE
```py
from quackpass import quackpass


manager = quackpass.LoginManager(salt=os.environ['salt'], mode="txt", file="passwords.txt")

manager.add_user("test", "secretpassword")

user = manager.login()

print(f"Logged in as {user}")
```

OUTPUT
```
Username: test
Password: secretpassword
Logged in as test
```
