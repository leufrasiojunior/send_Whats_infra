import requests

url = "https://whatsapp-number-validator3.p.rapidapi.com/WhatsappNumberHasIt"

payload = { "number": "551197979797" }
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "43540365d7msh166745d0c9aa746p112efcjsn534dec584af4",
	"X-RapidAPI-Host": "whatsapp-number-validator3.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers)
statusNumber = response.json()

print(statusNumber["status"])