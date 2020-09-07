#include <iostream>
#include <fstream>
#include <string>  
#include <string.h>

using namespace std;

float stringToFloat (string str){
	float a = 0;
	float b = 1;
	
	bool dot = false;

	for(int i = 0; i < str.length(); i++){
		if (str[i]=='.' || str[i]==',') {
			dot = true;
			continue;
		}

		a *= 10;

		if(dot) b *= 10;

		a += (str[i] - 48);
	}

	a = a/b;

	return a;
}

int main(){
    ifstream data;
    ifstream dias;
    ofstream output;

    data.open("data.csv");
    dias.open("dias.csv");
    output.open("saida.csv");

	string linha;
	string sum;
	char aux[3] = {'0', '0', '\0'};

	int i = 0;
	float somar = 0;

	while(getline(dias, linha)){

		//for(int i = 0; i < strlen(linha); i++) {
		//	linha[i] = linha[i] == ';' ? ',' : linha[i];
		//}
		//output << linha << endl;

		if(aux[0] == '0' && aux[1] == '0') {
			aux[0] = linha[8];
			aux[1] = linha[9];
		}

		if(aux[0] != linha[8] || aux[1] != linha[9]) {
			somar = somar/i;
			output << somar << endl;
			cout << "Dia " << aux << " : " << somar << endl;
			somar = 0;
			i = 0;
		}
		
		getline(data,sum);

		somar += stringToFloat(sum);
		i++;


		aux[0] = linha[8];
		aux[1] = linha[9];
	}
	somar = somar/i;
	output << somar << endl;

    data.close();
    dias.close();
    output.close();
    return 0;
}
