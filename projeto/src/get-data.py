import requests
import json

#19 / 04 / 2017

#30 / 06 / 2019

finalDate = '20200630'

diaC = 19
mesC = 4
anoC = 2017


# ---------------------------------------------------------------------

def farenToCels(farenhit):
	return (farenhit - 32) / (1.8)

# ---------------------------------------------------------------------

def nextDay(ano, mes, dia):
	if(mes == 2):
		if(dia == 29 and ano % 4 != 0):
			dia = 1
			mes += 1
		elif(dia == 30):
			dia = 1
			mes += 1
	if(dia == 31 and (mes == 2 or mes == 4 or mes == 6 or mes == 9 or mes == 11)):
		dia = 1
		mes += 1		
	if(dia == 32):
		dia = 1
		mes += 1
	if(mes == 13):
		mes = 1
		ano += 1 
	
	return ano, mes, dia

# ---------------------------------------------------------------------

def Converte(ano, mes, dia):
	if mes < 10:
		if dia < 10:
			valor = str(ano) + '0' + str(mes) + '0' + str(dia)
		else:
			valor = str(ano) + '0' + str(mes) + str(dia)
	elif dia < 10:
		if mes < 10:
			valor = str(ano) + '0' + str(mes) + '0' + str(dia)		
		else:
			valor = str(ano) + str(mes) + '0' + str(dia)
	else:
		valor = str(ano) + str(mes) + str(dia)
	return valor

# ---------------------------------------------------------------------

calendary = Converte(anoC, mesC, diaC)

output = open("avarage.csv", "w")

while calendary != finalDate:
	# api URL
	url = 'https://api.weather.com/v1/location/SBSM:9:BR/observations/historical.json?apiKey=6532d6454b8aa370768e63d6ba5a832e&units=e&startDate=' + calendary + '&endDate=' + calendary
	request = requests.get(url) 

	f = open("file.txt", "w")
	f.write(request.text)
	f.close()

	with open("file.txt", "r") as texto:
		i = 0

		data = json.load(texto)

		output.write(str(diaC))
		output.write(str(mesC))
		output.write(",")

		for p in data['observations']:
			# gets only the data between 12 and 18 o'clock
			if(i > 3 and i < 10):
				if(p['temp']):
					temp = round(p['temp'])
					temp = round(farenToCels(temp), 2)
				
				output.write(str(temp))
					
				output.write(",")
			i += 1
		output.write('\n')

	diaC = diaC + 1

	anoC, mesC, diaC = nextDay(anoC, mesC, diaC)

	print(calendary)
	calendary = Converte(anoC, mesC, diaC)
	


output.close()
texto.close()