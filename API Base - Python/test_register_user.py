#!/usr/bin/env python3
import requests
BASE='http://127.0.0.1:8000'
user={
  "username":"GameBros",
  "email":"gamebros@gmail.com",
  "full_name":"Game Bros",
  "password":"123456"
}
resp=requests.post(f"{BASE}/auth/register", json=user)
print(resp.status_code)
print(resp.text)
