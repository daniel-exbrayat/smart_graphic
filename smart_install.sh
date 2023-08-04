#!/bin/bash
#
[[ $EUID -ne 0 ]] && echo 'must be root' && exit

install -v -m 544 smart_graphic.py  /usrl/local/bin/
install -v -m 544 smart_logger      /etc/cron.daily/

