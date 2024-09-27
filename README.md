# MyPass
A open source self-hosted password manager built with Python.

## Setup

### Requirements:

[Python3](https://www.python.org/downloads/)

[Pip3](https://bootstrap.pypa.io/get-pip.py)

[Git](https://git-scm.com/)

## Step 1

Run the following commands (Git must be installed)

```
git clone https://github.com/SuperZekes/MyPass.git
cd MyPass
python -m pip install -r requirements.txt
python -m app.py
```

## Step 2

On line six you should see something like this:

```
http://<yourlocalip>:5000
```

Open that link in your browser of choice any one on your network will be able to access it as well.

![menuimage](https://i.imgur.com/6f7G85H.png)

By default the username is 'admin' and the password is 'admin123' this can be changed on line 13 in `app.py`.
