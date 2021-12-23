# Set Up

## Install 

### [Python](https://www.python.org/) & [pip](https://pypi.org/project/pip/)

```sh
sudo apt update && sudo apt upgrade
sudo apt upgrade python3
sudo apt install python3-pip
```

### [venv](https://docs.python.org/3/library/venv.html)

This will set up a virtual python environment just for this folder. This allows you to use `python3` just by typing `python` (and many more things)

```sh
sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate
deactivate # To deactivate
```

## Running the server

### Production

```sh
pip install -r requirements.txt
python server.py
```

### Development

```sh
pip install -r requirements/dev.txt
./server.sh # This just runs a watchmedo command to auto-reload on file changes
```

### Testing the server through the terminal

You can connect to the websocket server directly without the need of a website. This allows you to send any message, however if an invalid message is sent then the server will close the connection.

```sh
python -m websockets ws://localhost:8080/
```

## Running the website

```sh
python web.py
```

Open [http://localhost:8000/](http://localhost:8000/) in your browser

## Heroku

```sh
brew install heroku/brew/heroko
heroku login
heroku create sporcle-together
git push heroku main
heroku ps:scale web=1
heroku open
```
