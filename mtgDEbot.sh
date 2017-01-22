#!/bin/bash

# Umgebung für https://uberspace.de/
# muss angepasst werden, wenn Python 3.5 Defauklt ist.

pypath=/package/host/localhost/python-3.5/bin

#$pypath/pip3.5 install --upgrade pip --user
#$pypath/pip3.5 install telepot --user
#$pypath/pip3.5 install requests --user
#$pypath/pip3.5 install beautifulsoup4 --user

cd ~/bin/mtgDEbot/
token=$(cat tokenfile)
$pypath/python3.5 mtgDEbot.py $token
