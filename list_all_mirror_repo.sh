#!/bin/sh
# Run on gogs machine

grep "mirror" /var/lib/gogs/repositories/*/*/config | awk -F':' '{print $1}' | xargs grep url | sed -e "s/config\:.url.*= /,/g" > /tmp/mirrors.txt
