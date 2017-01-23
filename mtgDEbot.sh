#!/bin/bash

# Umgebung für https://uberspace.de/
# muss angepasst werden, wenn Python 3.5 Defauklt ist.

pypath=/package/host/localhost/python-3.5/bin

#$pypath/pip3.5 install --upgrade pip --user
#$pypath/pip3.5 install telepot --user
#$pypath/pip3.5 install requests --user
#$pypath/pip3.5 install beautifulsoup4 --user

cd ~/bin/mtgDEbot/
if [ -e "tokenfile" ]; then
  token=$(cat tokenfile)
else
  echo "bitte Telegram API Token in tokenfile eintragen"
  echo "123456789:ABC-ABCDEFGHIJKLMNOPQRSTUVWXYZABCDE" > tokenfile
  echo "dummy file wurde erzeugt"
  exit 1
fi

$pypath/python3.5 mtgDEbot.py $token
