import requests

CAPTCHA_SECRET_KEY = 'ES_8a044741efde4d5f90310e7d4ce94aaf'

def verify_captcha(captcha_response):
    """Verificar la respuesta del CAPTCHA con la API de hCAPTCHA."""
    url = 'https://hcaptcha.com/siteverify'
    data = {
        'secret': CAPTCHA_SECRET_KEY,
        'response': captcha_response
    }
    response = requests.post(url, data=data)
    result = response.json()
    return result.get('success', False)
