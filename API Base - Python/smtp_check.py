#!/usr/bin/env python3
import smtplib
import os

# Ler .env localmente
env = {}
with open('.env', 'r', encoding='utf-8') as f:
    for line in f:
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k,v=line.split('=',1)
            env[k.strip()]=v.strip()

user = env.get('EMAIL_USER')
passwd = env.get('EMAIL_PASS')
host = env.get('SMTP_HOST','smtp.gmail.com')
port = int(env.get('SMTP_PORT','587'))
use_tls = env.get('SMTP_USE_TLS','True').lower() in ('1','true','yes')

print('SMTP check using host:', host, 'port:', port, 'use_tls:', use_tls)
try:
    with smtplib.SMTP(host, port, timeout=20) as server:
        server.set_debuglevel(1)
        if use_tls:
            server.starttls()
        server.login(user, passwd)
        print('LOGIN OK')
except Exception as e:
    print('SMTP ERROR:', repr(e))
