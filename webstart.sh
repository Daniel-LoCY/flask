#!/bin/bash
rm nohup.out
nohup flask run --host 0.0.0.0 --port 5000 &
echo 'Start Web Server'
