#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json

config_data = {
    "telegram_token": "6019854993:AAHTbTZu8g2RKQQyDXZD9bzsERo27y6ya_Y",
    "telegram_chat_id": "6580852850",
    "chrome_driver_path": "D:\\chromedriver\\chromedriver.exe"
}

with open('config.json', 'w') as f:
    json.dump(config_data, f, indent=4)

