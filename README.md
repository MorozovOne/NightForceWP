# NightForceWP
NightForceWP, представляет собой инструмент для брутфорс-атаки на WordPress-сайты, позволяя пользователю пытаться подобрать логин и пароль для входа в систему

Инструкция по установке:
1. git clone https://github.com/MorozovOne/NightForceWP
2. cd NightFroceWP
3. python3 -m venv venv 
4. source venv/bin/activate 
5. pip install -r requirements.txt
6. запускаем скрипт

EXAMPLE:
python nightforce.py --usernames user.txt --passwords pass.txt --url "https://example.com/ --use-proxies
   

ENGLISH ==============
#NightForceWP
NightForceWP is a tool for brute force attacks on WordPress sites, allowing the user to try to guess the username and password to log in to the system.

Installation instructions:
1. git clone https://github.com/MorozovOne/NightForceWP
2. cd NightFroceWP
3. python3 -m venv venv 
4. source venv/bin/activate 
5. pip install -r requirements.txt
6. run the script

EXAMPLE:
python nightforce.py --usernames user.txt --passwords pass.txt --url "https://example.com/ --use-proxies
