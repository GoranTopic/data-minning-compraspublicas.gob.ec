#!/bin/bash

# this script is used to open the tmux terminal, and start running the scrapper
# it check is the node program is not already running

export DISPLAY=:0.0

PROCESS=$(ps aux | grep 'node src/companies/engined.js' | wc -l)

if [ "${PROCESS}" -lt 2 ]; then
    echo "starting scrapper"
    gnome-terminal --full-screen --title=supercias_scraper -- tmux new 'cd supercias; npm start; bash';
else
    echo "scrapper already running"
fi;


