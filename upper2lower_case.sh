#!/bin/zsh

sudo apt install rename
# Upper case to Lower case
find TIMIT -depth | xargs -n 1 rename -v -f 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;