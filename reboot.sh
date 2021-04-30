#!/bin/bash

ps ax | grep monitoring.py | awk 'NR==1{print $1}' | xargs kill

nohup ./monitoring.py &