@echo off
cd /d "%~dp0"
python main.py >> quotes_mailer.log 2>&1
echo Auto quotes executed at %date% %time% >> quotes_mailer.log