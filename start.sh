#!/bin/bash

# this script is used to open the tmux terminal, and start running the scrapper
# it check is the node program is not already running
# this script is mean to be started by crontabs

export DISPLAY=:0.0

PROJECTDIR='/home/telix/compraspublicas.gob.ec'

PROCESS=$(ps aux | grep 'node src/main.js' | wc -l)

if [ "${PROCESS}" -lt 2 ]; then
    echo "starting scrapper"
    gnome-terminal --full-screen --title=supercias_scraper -- tmux new "cd $PROJECTDIR; npm start; bash";
else
    echo "scrapper already running"
fi;


