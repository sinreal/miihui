#!/bin/bash

ll `pgrep -f "/www/imihui/app.py"`;
spawn-fcgi -d /www/imihui  -f /www/imihui/app.py -a 127.0.0.1 -p 10000;:
