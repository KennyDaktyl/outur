import hashlib
import os
import requests

def send_sms(number, text, client=False):
    
    login = os.environ.get('SMS_LOGIN')
    password = os.environ.get('SMS_PASSWORD')
    password_md5 = hashlib.md5(password.encode()).hexdigest()

    api_url = "https://api.mobitex.pl/sms.php"
    
    text_message = text
        
    payload = {
        'user': login,
        'pass': password_md5,
        'number': f"48{number}",
        'text': text_message,
        'type': 'sms',  
        'from': "Tordo.pl" 
    }

    response = requests.post(api_url, data=payload)
    if response.status_code == 200:
        return f"SMS wysłany pomyślnie! Odpowiedź: {response.text}"
    else:
        return f"Błąd wysyłania: {response.status_code}"
