sudo apt update && sudo apt upgrade
sudo apt upgrade python3
sudo apt install python3-pip
sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate
deactivate

https://docs.microsoft.com/en-us/windows/python/web-frameworks

## Connect

pip install websockets
python -m http.server
http://localhost:8000/
python -m websockets ws://localhost:8080/
python main.js

## Heroku

`brew install heroku/brew/heroku`
`heroku login`
`heroku create sporcle-together`
`git push heroku main`
`heroku ps:scale web=1`
`heroku open`