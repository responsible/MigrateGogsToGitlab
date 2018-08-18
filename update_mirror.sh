#!/bin/sh

cat mirrors.txt | awk -F',' '{system("cd "$1" && git remote add origin "$2" && git remote set-url origin "$2" && git fetch origin +refs/heads/*:refs/heads/* -p")}'
