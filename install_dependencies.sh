#!/bin/sh
sudo apt-get install -y python python-pip npm
sudo npm install -g pm2 n npm
sudo n latest

cd `dirname $0`/server
npm install

pip install -r requirements.txt
python -m nltk.downloader all-corpora
