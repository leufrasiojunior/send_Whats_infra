import datetime

current_apre = datetime.datetime.now().strftime('%H')


if int(current_apre) < 12:
    apre = "Bom dia"
elif int(current_apre) >= 12 and int(current_apre) <= 18:
    apre = "Boa tarde"
else:
    apre = "Boa noite"

print (int(current_apre))
print (apre)