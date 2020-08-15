Number mulTwo(const Number numA, const Number numB);
std::vector<int> factorList(Number n){
	std::vector<int> list;
	if (n.type != 1 && n.type != 1){
		return list;
	}
	long nn = std::stoi(n.top);
	int p = 2;
	while (p <= nn){
		if (nn%p == 0){
			nn /= p;
			list.push_back(p);
		}
		p++;
	}
	return list;
}
std::string numberType(std::string input){
	Number n;
	//TODO: add strings to numbers map with type==0
	if (input.length()==0){
		numbers[""]=n;
		return "string";
	}
	if (input == "pi"){
		n.type = 11;
		n.top = "1";
		n.bottom = "pi";
		numbers[input]=n;
		std::cout << "n1: " << outputNumber(n) << "\n";
		return "num";
	}
	else if (input.length()>2 && input.at(input.length()-2) == 'p' && input.at(input.length()-1) == 'i'){
		n.type = 11;
		if (numbers.find(input.substr(0,input.length()-2)) == numbers.end()){
			numberType(input.substr(0,input.length()-2));
		}
		n.top = outputNumber(numbers[input.substr(0,input.length()-2)]);
		n.bottom = "pi";
		numbers[input]=n;
		std::cout << "n2: " << outputNumber(n) << "\n";
		return "num";
	}
	
	
	if (input.at(0) == '-'){
		input.replace(0,1,"");
		std::string rest = "";
		if (numbers.find(input) != numbers.end()){
			if (numbers[input].type == 0){
				rest = "string";
			}
		}
		else {
			rest = numberType(input);
		}
		 
		if (rest == "string" || numbers[input].type <= 0){
			numbers[input]=n; return "string";
		}
		else {
			n.type = numbers[input].type*-1;
			n.top = numbers[input].top;
			n.bottom = numbers[input].bottom;
			numbers["-"+input] = n;
			return "num";
		}
	}
	int ii;
	std::string currentType = "int";
	int idx = -1;
	for(ii=0;ii<input.length();ii++){
		switch(input.at(ii)){
			case '.': {
				if (currentType == "int"){currentType = "dec";}
				else if (currentType == "dec"){numbers[input]=n; return "string";}
				else if (currentType == "red"){numbers[input]=n; return "string";}
				else if (currentType == "rep"){numbers[input]=n; return "string";}
				else if (currentType == "fra"){numbers[input]=n; return "string";}
				else if (currentType == "sci" || currentType == "scn"){numbers[input]=n; return "string";}
				n.top = input.substr(0,ii);
				n.bottom = input.substr(ii+1,input.length()-ii-1);
				idx = ii;
				break;
			}
			case '_': {
				if (currentType == "int"){
					//currentType = "rep";
					//n.top = input.substr(0,ii);
					//n.bottom = input.substr(ii+1,input.length()-ii-1);
					numbers[input]=n; return "string";
				}
				else if (currentType == "dec"){currentType = "red"; idx = ii - idx;}
				else if (currentType == "red"){numbers[input]=n; return "string";}
				else if (currentType == "rep"){numbers[input]=n; return "string";}
				else if (currentType == "fra"){numbers[input]=n; return "string";}
				else if (currentType == "sci" || currentType == "scn"){numbers[input]=n; return "string";}
				break;
			}
			case 'e': {
				if (currentType == "int"){currentType = "sci";}
				else if (currentType == "dec"){currentType = "sci";}
				else if (currentType == "red"){currentType = "sci";}
				else if (currentType == "rep"){currentType = "sci";}
				else if (currentType == "fra"){numbers[input]=n; return "string";}
				else if (currentType == "sci" || currentType == "scn"){numbers[input]=n; return "string";}
				n.top = input.substr(0,ii);
				n.bottom = input.substr(ii+1,input.length()-ii-1);
				break;
			}
			case '-': {
				if (currentType == "int"){numbers[input]=n; return "string";}
				else if (currentType == "dec"){numbers[input]=n; return "string";}
				else if (currentType == "red"){numbers[input]=n; return "string";}
				else if (currentType == "rep"){numbers[input]=n; return "string";}
				else if (currentType == "fra"){numbers[input]=n; return "string";}
				else if (currentType == "sci"){currentType = "scn";}
				else if (currentType == "scn"){numbers[input]=n; return "string";}
				break;
			}
			case '/': {
				if (currentType == "int"){currentType = "fra";
					n.top = input.substr(0,ii);
					n.bottom = input.substr(ii+1,input.length()-ii-1);
					idx = ii;
				}
				else if (currentType == "dec"){numbers[input]=n; return "string";}
				else if (currentType == "red"){numbers[input]=n; return "string";}
				else if (currentType == "rep"){numbers[input]=n; return "string";}
				else if (currentType == "fra"){numbers[input]=n; return "string";}
				else if (currentType == "sci"){numbers[input]=n; return "string";}
				else if (currentType == "scn"){numbers[input]=n; return "string";}
				break;
			}
			case '0': break;
			case '1': break;
			case '2': break;
			case '3': break;
			case '4': break;
			case '5': break;
			case '6': break;
			case '7': break;
			case '8': break;
			case '9': break;
			default: numbers[input]=n; return "string";

		}
	}
	
	if (currentType == "int"){
		n.type = 1;
		n.top = input;
		n.bottom = "1";
		numbers[input]=n;
		return "int";
	}
	else if (currentType == "dec"){
		n.type = 2;
		std::string nb = n.bottom;
		n.top = n.top+n.bottom;
		int nbl = n.bottom.length();
		n.bottom = "1";
		int lastZero = -1;
		for (ii=0;ii<nbl;ii++){
			n.bottom += "0";
			if (nb.at(ii) != '0'){
				lastZero = ii;
			}
		}
		if (lastZero < nbl-1){
			n.top = n.top.substr(0,n.top.length()-(nbl-1-lastZero));
			n.bottom = n.bottom.substr(0,n.bottom.length()-(nbl-1-lastZero));
		}
		if (n.bottom == "1"){
			n.type = 1;
		}
		numbers[input]=n;
		return "dec";
	}
	else if (currentType == "fra"){
		n.type = 3;
		numbers[input]=n;
		if (n.bottom == "1"){
			n.type = 1;
		}
		return "fra";
	}
	else if (currentType == "red"){
		/*
		n.type = 5;
		//TODO: make correct top and bottom
		int repLen = n.bottom.length()-idx;
		int repTop = std::stoi(n.bottom.substr(idx,n.bottom.length()-idx));
		std::string repBot = "";
		for (ii=0;ii<repLen;ii++){
			repBot += "9";
		}
		if (numbers.find(repBot) == numbers.end()){
			numberType(repBot);
		}
		std::vector<int> fList = factorList(numbers[repBot]);
		numbers[input]=n;
		return "rep";
		*/
		numbers[input]=n;
		return "string";
	}
	else if (currentType == "sci" || currentType == "scn"){
		n.type = 4;
		numbers[input]=n;
		return "sci";
	}
	else {numbers[input]=n; return "string";}
	numbers[input]=n;
	return "string";
}

Number negateOne(const Number numA){
	Number n;
	n.type = -1*numA.type;
	n.top = numA.top;
	n.bottom = numA.bottom;
	return n;
}
Number invertOne(const Number numA){
	Number n;
	if (numA.type == 0){
		n.type = 0; return n;
	}
	else if (numA.type == 1 || numA.type == -1){//integer
		if (numA.top == "1"){n = numA; return n;}
		if (numA.top == "0"){n.type = 0; return n;}
		n.type = 3*numA.type;
		n.top = "1";
		n.bottom = numA.top;
		return n;
	}
	else if (numA.type == 2 || numA.type == -2){//decimal
		//TODO: create decimal unless == 0
		if (numA.top == "0"){n.type = 0; return n;}
		if (numA.top == "1"){n.type = 1*numA.type/2; n.top = numA.bottom; n.bottom = "1"; return n;}
		n.type = numA.type;
		n.top = numA.bottom;
		n.bottom = numA.top;
		return n;
	}
	else if (numA.type == 3 || numA.type == -3){//fraction
		//TODO: create decimal unless == 0
		if (numA.top == "0"){n.type = 0; return n;}
		if (numA.top == "1"){n.type = 1*numA.type/3; n.top = numA.bottom; n.bottom = "1"; return n;}
		n.type = numA.type;
		n.top = numA.bottom;
		n.bottom = numA.top;
		return n;
	}
	else if (numA.type == 4 || numA.type == -4){//sci not
		//TODO: create sci not unless == 0
	}
	else if (numA.type == 5 || numA.type == -5){//rep decimal
		//TODO: do rep decimal inversion
	}
	//TODO: create number type for division by zero
	return n;
}
bool isDecimal(Number n){
	int i;
	if (n.bottom.length()<1){
		return false;
	}
	if (n.bottom.at(0) != '1'){
		return false;
	}
	for (i=1;i<n.bottom.length();i++){
		if (n.bottom.at(i) != '0'){
			return false;
		}
	}
	return true;
}


std::string outputNumber(Number n){
	if (n.type == 1){
		return n.top;
	}
	else if (n.type == -1){
		return "-"+n.top;
	}
	else if (n.type == 2){
		double d = std::stoi(n.top);
		d /= std::stoi(n.bottom);
		return std::to_string(d);
	}
	else if (n.type == -2){
		double d = std::stoi(n.top);
		d /= std::stoi(n.bottom);
		return "-"+std::to_string(d);
	}
	else if (n.type == 3){
		return n.top + "/"+n.bottom;
	}
	else if (n.type == -3){
		return "-"+n.top + "/"+n.bottom;
	}
	else if (n.type == 11){
		return n.top + n.bottom;
	}
	return "";
}
Number reduceFraction(const Number numA){
	int a = std::stoi(numA.top);
	int b = std::stoi(numA.bottom);
	std::vector<int> primes = {2,3,5,7,11,13,17,19,23,29};
	int i;
	for (i=0;i<10;i++){
		while (a%primes[i] == 0 && b%primes[i] == 0){
			a = a/primes[i];
			b = b/primes[i];
		}
		if (b == 1){
			Number n;
			if (numA.type < 0){
				n.type = -1;
			}
			else {
				n.type = 1;
			}
			n.top = std::to_string(a);
			n.bottom = "1";
			return n;
		}
	}
	Number n;
	n.type = numA.type;
	n.top = std::to_string(a);
	n.bottom = std::to_string(b);
	return n;
	
}
Number addTwo(const Number numA, const Number numB){
	std::string revsum = "";
	Number n;
	int base = 10;
	if (numA.type == 1){
		if (numB.type == 1){
			std::string a = numA.top;
			std::string b = numB.top;
			if (b.length() > a.length()){
				std::string c = a;
				a = b;
				b = c;
			}
			int len = a.length();
			while (len > b.length()){
				b = "0"+b;
			}
			int i;
			int charSum =0;
			int carry = 0;
			for (i=0;i<a.length();i++){
				int aa = a.at(len-1-i) - '0';
				int bb = b.at(len-1-i) - '0';
				charSum = aa + bb + carry;
				carry = 0;
				while (charSum >= base){
					charSum -= base;
					carry++;
				}
				revsum += std::to_string(charSum);
			}
			while (carry > 0){
				charSum = carry;
				carry = 0;
				while (charSum >= base){
					charSum -= base;
					carry++;
				}
				revsum += std::to_string(charSum);
			}
			std::string sum = "";
			for (i=revsum.length()-1;i>=0;i--){
				sum += revsum.at(i);
			}
			if (numbers.find(sum) == numbers.end()){
				numberType(sum);
			}
			return numbers[sum];
		}
		else if (numB.type == -1){
			n.type = 1;
			n.top = numB.top;
			if (n > numA){
				return negateOne(addTwo(n,negateOne(numA)));
			}
			
			std::string a = numA.top;
			std::string b = numB.top;

			int len = a.length();
			while (len > b.length()){
				b = "0"+b;
			}
			int i;
			int charSum =0;
			int carry = 0;
			for (i=0;i<a.length();i++){
				int aa = a.at(len-1-i) - '0';
				int bb = b.at(len-1-i) - '0';
				charSum = aa - bb + carry;
				carry = 0;
				while (charSum < 0){
					charSum += base;
					carry--;
				}
				revsum += std::to_string(charSum);
			}
			while (carry < 0){
				charSum = carry;
				carry = 0;
				while (charSum < 0){
					charSum += base;
					carry--;
				}
				revsum += std::to_string(charSum);
			}
			std::string sum = "";
			bool pastZero = false;
			for (i=revsum.length()-1;i>=0;i--){
				if (!pastZero){
					if (revsum.at(i) == '0'){continue;}
					else {pastZero = true;}
				}
				sum += revsum.at(i);
			}
			if (numbers.find(sum) == numbers.end()){
				numberType(sum);
			}
			return numbers[sum];
		}
		else if (numB.type == 2 || numB.type == -2){
			n.type = 2; n.top = numA.top; n.bottom = "1";
			return addTwo(n,numB);
		}
		else if (numB.type == 3 || numB.type == -3){
			n.type = 3; n.top = numA.top; n.bottom = "1";
			return addTwo(n,numB);
		}
	}
	else if (numA.type == 2){
		if (numB.type == 2){
			Number nb;
			nb.type = 1;
			if (isDecimal(numA) && isDecimal(numB)){
				int blenDiff = numB.bottom.length() - numA.bottom.length();
				int i;
				if (blenDiff > 0){
					nb.top = numB.top;
					n.type = 1;
					n.top = numA.top;
					for (i=0;i<blenDiff;i++){
						n.top += "0";
					}
					n = addTwo(n,nb);
					n.bottom = numB.bottom;
					n.type = 2;
				}
				else if (blenDiff < 0){
					nb.top = numB.top;
					n.type = 1;
					n.top = numA.top;
					for (i=0;i<-1*blenDiff;i++){
						nb.top += "0";
					}
					n = addTwo(n,nb);
					n.bottom = numA.bottom;
					n.type = 2;
				}
				else {
					nb.top = numB.top;
					n.type = 1;
					n.top = numA.top;
					n = addTwo(n,nb);
					n.bottom = numA.bottom;
					n.type = 2;
					while (n.top.at(n.top.length()-1)=='0' && n.bottom.length()>1){
						n.top = n.top.substr(0,n.top.length()-1);
						n.bottom = n.bottom.substr(0,n.bottom.length()-1);
					}
					if (n.bottom == "1"){
						n.type = 1;
					}
				}
			}
			else {
				if (numbers.find(numA.top) == numbers.end()){
					numberType(numA.top);
				}
				if (numbers.find(numB.top) == numbers.end()){
					numberType(numB.top);
				}
				if (numbers.find(numA.bottom) == numbers.end()){
					numberType(numA.bottom);
				}
				if (numbers.find(numB.bottom) == numbers.end()){
					numberType(numB.bottom);
				}
				
				n = addTwo(mulTwo(numbers[numA.top],numbers[numB.bottom]),mulTwo(numbers[numB.top],numbers[numA.bottom]));
				
				nb = mulTwo(numbers[numA.bottom],numbers[numB.bottom]);
				n.type = 2;
				n.top = n.top;
				n.bottom = nb.top;
				n = reduceFraction(n);
			}
		}
		else if (numB.type == -2){
			Number nb;
			nb.type = -1;
			if (isDecimal(numA) && isDecimal(numB)){
				int blenDiff = numB.bottom.length() - numA.bottom.length();
				int i;
				if (blenDiff > 0){
					nb.top = numB.top;
					n.type = 1;
					n.top = numA.top;
					for (i=0;i<blenDiff;i++){
						n.top += "0";
					}
					n = addTwo(n,nb);
					n.bottom = numB.bottom;
					n.type = 2 * n.type;
				}
				else if (blenDiff < 0){
					nb.top = numB.top;
					n.type = 1;
					n.top = numA.top;
					for (i=0;i<-1*blenDiff;i++){
						nb.top += "0";
					}
					n = addTwo(n,nb);
					n.bottom = numA.bottom;
					n.type = 2 * n.type;
				}
				else {
					nb.top = numB.top;
					n.type = 1;
					n.top = numA.top;
					n = addTwo(n,nb);
					n.bottom = numA.bottom;
				
					while (n.top.at(n.top.length()-1)=='0' && n.bottom.length()>1){
						n.top = n.top.substr(0,n.top.length()-1);
						n.bottom = n.bottom.substr(0,n.bottom.length()-1);
					}
					if (n.bottom != "1"){
						n.type = 2 * n.type;
					}
				}
			}
			else {
				if (numbers.find(numA.top) == numbers.end()){
					numberType(numA.top);
				}
				if (numbers.find(numB.top) == numbers.end()){
					numberType(numB.top);
				}
				if (numbers.find(numA.bottom) == numbers.end()){
					numberType(numA.bottom);
				}
				if (numbers.find(numB.bottom) == numbers.end()){
					numberType(numB.bottom);
				}
				
				n = addTwo(mulTwo(numbers[numA.top],numbers[numB.bottom]),mulTwo(negateOne(numbers[numB.top]),numbers[numA.bottom]));
				
				nb = mulTwo(numbers[numA.bottom],numbers[numB.bottom]);
				n.type = 2 * n.type;
				n.top = n.top;
				n.bottom = nb.top;
				n = reduceFraction(n);
			}
		}
		else if (numB.type == 1 || numB.type == -1){
			n.type = 2 * numB.type; n.top = numB.top; n.bottom = "1";
			return addTwo(numA,n);
		}
		else if (numB.type == 3 || numB.type == -3){
			n.type = 2 * numB.type / 3; n.top = numB.top; n.bottom = numB.bottom;
			return addTwo(numA,n);
		}
	}
	else if (numA.type == 3){
		if (numB.type == 3){
			Number nb;
			nb.type = 2;
			nb.top = numB.top;
			nb.bottom = numB.bottom;
			n.type = 2;
			n.top = numA.top;
			n.bottom = numA.bottom;
			n = addTwo(n,nb);
			n.type = 3;
		}
		else if (numB.type == -3){
			Number nb;
			nb.type = -2;
			nb.top = numB.top;
			nb.bottom = numB.bottom;
			n.type = 2;
			n.top = numA.top;
			n.bottom = numA.bottom;
			n = addTwo(n,nb);
			n.type = 3 * n.type/2;
		}
		else if (numB.type == 1 || numB.type == -1){
			n.type = 3 * numB.type; n.top = numB.top; n.bottom = "1";
			return addTwo(n,numA);
		}
		else if (numB.type == 2 || numB.type == -2){
			n.type = 2; n.top = numA.top; n.bottom = numA.bottom;
			return addTwo(n,numB);
		}
	}
	else if (numA.type < 0){
		if (numB.type > 0){
			return addTwo(numB,numA);
		}
		else if (numB.type < 0){
			return negateOne(addTwo(negateOne(numA),negateOne(numB)));
		}
	}
	return n;

}

Number mulTwo(const Number numA, const Number numB){
	int base = 10;
	int neg = 1;
	Number n;
			
	if (numA.type == 1){
		if (numB.type == 1){
			n.type = 1;
			int prod = std::stoi(numA.top);
			prod *= std::stoi(numB.top);
			n.top = std::to_string(prod);
			return n;
		}
		else if (numB.type == -1){
			n.type = -1;
			int prod = std::stoi(numA.top);
			prod *= std::stoi(numB.top);
			n.top = std::to_string(prod);
			return n;
		}
		else if (numB.type == 2 || numB.type == -2 || numB.type == 3 || numB.type == -3){
			n.type = numB.type;
			int prod = std::stoi(numA.top);
			prod *= std::stoi(numB.top);
			n.top = std::to_string(prod);
			n.bottom = numB.bottom;
			n = reduceFraction(n);
			return n;
		}
		else if (numB.type == 11){
			Number nn;
			nn = mulTwo(numA,numbers[numB.top]);
			n.type = 11;
			n.top = outputNumber(nn);
			n.bottom = numB.bottom;
			return n;
		}
	}
	else if (numA.type == 2){
		if (numB.type == 1 || numB.type == -1){
			n.type = 2 * numB.type;
			int prod = std::stoi(numA.top);
			prod *= std::stoi(numB.top);
			n.top = std::to_string(prod);
			n.bottom = numA.bottom;
			n = reduceFraction(n);
			return n;
		}
		else if (numB.type == 2 || numB.type == -2 || numB.type == 3 || numB.type == -3){
			n.type = 2;
			if (numB.type < 0){
				n.type = -2;
			}
			int prod = std::stoi(numA.top);
			prod *= std::stoi(numB.top);
			n.top = std::to_string(prod);
			prod = std::stoi(numA.bottom);
			prod *= std::stoi(numB.bottom);
			n.bottom = std::to_string(prod);
			n = reduceFraction(n);
			return n;
		}
	}
	else if (numA.type == 3){
		if (numB.type == 1 || numB.type == -1){
			n.type = 3 * numB.type;
			int prod = std::stoi(numA.top);
			prod *= std::stoi(numB.top);
			n.top = std::to_string(prod);
			n.bottom = numA.bottom;
			n = reduceFraction(n);
			return n;
		}
		else if (numB.type == 2 || numB.type == -2 || numB.type == 3 || numB.type == -3){
			n.type = numB.type;
			int prod = std::stoi(numA.top);
			prod *= std::stoi(numB.top);
			n.top = std::to_string(prod);
			prod = std::stoi(numA.bottom);
			prod *= std::stoi(numB.bottom);
			n.bottom = std::to_string(prod);
			n = reduceFraction(n);
			return n;
		}
	}
	else if (numA.type < 0){
		if (numB.type > 0){
			return mulTwo(numB,numA);
		}
		else if (numB.type < 0){
			return mulTwo(negateOne(numA),negateOne(numB));
		}
	}
	return n;
}

Number expTwo(const Number numA, const Number numB){
	int base = 10;
	int neg = 1;
	Number n;
	if (numB.type < 0){
		n.type = -1*numB.type;
		n.top = numB.top;
		n.bottom = numB.bottom;
		return invertOne(expTwo(numA,n));
	}
	if (numA.type == 1){
		if (numB.type == 1){
			n.type = 1;
			double a = std::stoi(numA.top);
			double b = std::stoi(numB.top);
			std::string prod = std::to_string(pow(a,b));
			if (numbers.find(prod) == numbers.end()){
				numberType(prod);
			}
			n = numbers[prod];
			return n;
		}
		else if (numB.type == 2){
			n.type = 2;
			double a = std::stoi(numA.top);
			double b = std::stod(numB.top) / std::stod(numB.bottom);
			std::string prod = std::to_string(pow(a,b));
			if (numbers.find(prod) == numbers.end()){
				numberType(prod);
			}
			n = numbers[prod];
			return n;
		}
	}
	else if (numA.type == 2){
		if (numB.type == 1){
			n.type = 1;
			double a = std::stod(numA.top) / std::stod(numA.bottom);
			double b = std::stoi(numB.top);
			std::string prod = std::to_string(pow(a,b));
			if (numbers.find(prod) == numbers.end()){
				numberType(prod);
			}
			n = numbers[prod];
			return n;
		}
		else if (numB.type == 2){
			n.type = 2;
			double a = std::stod(numA.top) / std::stod(numA.bottom);
			double b = std::stod(numB.top) / std::stod(numB.bottom);
			std::string prod = std::to_string(pow(a,b));
			if (numbers.find(prod) == numbers.end()){
				numberType(prod);
			}
			n = numbers[prod];
			return n;
		}
	}
	else if (numA.type < 0){
		if (numB.type == 1){
			char lastDigit = numB.top.at(numB.top.length()-1);
			if (lastDigit == '0' || lastDigit == '2' || lastDigit == '4' || lastDigit == '6' || lastDigit == '8'){
				n.type = -1*numA.type;
				n.top = numA.top;
				n.bottom = numA.bottom;
				return expTwo(n,numB);
			}
			else {
				n.type = -1*numA.type;
				n.top = numA.top;
				n.bottom = numA.bottom;
				return negateOne(expTwo(n,numB));
			}
		}
		else if (numB.type == 2){
			return n;
		}
		else if (numB.type == 3){
			char lastDigitB = numB.bottom.at(numB.bottom.length()-1);
			if (lastDigitB == '0' || lastDigitB == '2' || lastDigitB == '4' || lastDigitB == '6' || lastDigitB == '8'){
				return n;
			}
			else {
				char lastDigit = numB.top.at(numB.top.length()-1);
				if (lastDigit == '0' || lastDigit == '2' || lastDigit == '4' || lastDigit == '6' || lastDigit == '8'){
					n.type = -1*numA.type;
					n.top = numA.top;
					n.bottom = numA.bottom;
					return expTwo(n,numB);
				}
				else {
					n.type = -1*numA.type;
					n.top = numA.top;
					n.bottom = numA.bottom;
					return negateOne(expTwo(n,numB));
				}
			}
		}
		

	}
	return n;
}

Number logTwo(const Number numA, const Number numB){ //numA is base and numB is inside part, of course
	int base = 10;
	int neg = 1;
	Number n;
	if (numB.type <= 0 || numA.type <= 0){
		return n;
	}
	if (numB.top == "0"){
		return n;
	}

	if (numA.type == 1){
		if (numB.type == 1){
			double a = std::stoi(numA.top);
			double b = std::stoi(numB.top);
			std::string prod = std::to_string(log(b)/log(a));
			if (numbers.find(prod) == numbers.end()){
				numberType(prod);
			}
			n = numbers[prod];
			return n;
		}
		else if (numB.type == 2){
			double a = std::stoi(numA.top);
			double b = std::stod(numB.top) / std::stod(numB.bottom);
			std::string prod = std::to_string(log(b)/log(a));
			if (numbers.find(prod) == numbers.end()){
				numberType(prod);
			}
			n = numbers[prod];
			return n;
		}
		else if (numB.type == 3){
			n.type = 1;
			n.top = numB.top;
			Number nb;
			nb.type = 1;
			nb.top = numB.bottom;
			return addTwo(logTwo(numA,n),negateOne(logTwo(numA,nb)));
		}
	}
	else if (numA.type == 2){
		if (numB.type == 1){
			double a = std::stod(numA.top) / std::stod(numA.bottom);
			double b = std::stoi(numB.top);
			std::string prod = std::to_string(log(b)/log(a));
			if (numbers.find(prod) == numbers.end()){
				numberType(prod);
			}
			n = numbers[prod];
			return n;
		}
		else if (numB.type == 2){
			double a = std::stod(numA.top) / std::stod(numA.bottom);
			double b = std::stod(numB.top) / std::stod(numB.bottom);
			std::string prod = std::to_string(log(b)/log(a));
			if (numbers.find(prod) == numbers.end()){
				numberType(prod);
			}
			n = numbers[prod];
			return n;
		}
		else if (numB.type == 3){
			double a = std::stod(numA.top) / std::stod(numA.bottom);
			double b = std::stod(numB.top) / std::stod(numB.bottom);
			std::string prod = std::to_string(log(b)/log(a));
			if (numbers.find(prod) == numbers.end()){
				numberType(prod);
			}
			n = numbers[prod];
			return n;
		}
	}
	else if (numA.type == 3){
		if (numB.type == 1){
			double a = std::stoi(numA.top);
			double aa = std::stoi(numA.bottom);
			double b = std::stoi(numB.top);
			std::string prod = std::to_string(log(b)/(log(a)-log(aa)));
			if (numbers.find(prod) == numbers.end()){
				numberType(prod);
			}
			n = numbers[prod];
			return n;
		}
		else if (numB.type == 2){
			double a = std::stod(numA.top) / std::stod(numA.bottom);
			double b = std::stod(numB.top) / std::stod(numB.bottom);
			std::string prod = std::to_string(log(b)/log(a));
			if (numbers.find(prod) == numbers.end()){
				numberType(prod);
			}
			n = numbers[prod];
			return n;
		}
		else if (numB.type == 3){
			double a = std::stoi(numA.top);
			double aa = std::stoi(numA.bottom);
			double b = std::stoi(numB.top);
			double bb = std::stoi(numB.bottom);
			std::string prod = std::to_string((log(b)-log(bb))/(log(a)-log(aa)));
			if (numbers.find(prod) == numbers.end()){
				numberType(prod);
			}
			n = numbers[prod];
			return n;
		}
	}
	return n;
}

Number trigTwo(char fn, const Number numA){ //numA is base and numB is inside part, of course
	int base = 10;
	int neg = 1;
	Number n;
	if (numA.type == 0){
		return n;
	}
	double a;
	if (numA.type == 1 || numA.type == -1){
		a = std::stoi(numA.top);
	}
	else if (numA.type == 2 || numA.type == 3 || numA.type == -2 || numA.type == -3){
		a = std::stod(numA.top) / std::stod(numA.bottom);
	}
	else if (numA.type == 11){
		std::cout << "n3: " << outputNumber(numA) << " and " << numA.top << " and " << numA.bottom << "\n";
		if (numA.bottom == "pi"){
			n = numbers[numA.top];
			if (n.type == 1 || n.type == -1){
				if (fn == -64){
					std::cout << "n4: " << outputNumber(numbers["0"]) << "\n";
					return numbers["0"];
				}
			}
			else {
				return n;
			}
			//TODO: compute exact value of trig functions of multiples of pi
		}
		else {
			return n;
		}
	}
	else {
		return n;
	}

	std::string prod = "";
	if (fn == -64){prod = std::to_string(sin(a));}
	else if (fn == -63){prod = std::to_string(cos(a));} 
	else if (fn == -62){double ca = cos(a); if (ca != 0){prod = std::to_string(sin(a)/ca);}} 
	else if (fn == -61){double sa = sin(a); if (sa != 0){prod = std::to_string(1.0/sa);}} 
	else if (fn == -60){double ca = cos(a); if (ca != 0){prod = std::to_string(1.0/ca);}} 
	else if (fn == -59){double sa = sin(a); if (sa != 0){prod = std::to_string(cos(a)/sa);}} 
	
	if (numbers.find(prod) == numbers.end()){
		numberType(prod);
	}
	n = numbers[prod];
	return n;

}

Number invTrigTwo(char fn, const Number numA){ //numA is base and numB is inside part, of course
	int base = 10;
	int neg = 1;
	Number n;
	if (numA.type == 0){
		return n;
	}
	double a;
	if (numA.type == 1 || numA.type == -1){
		a = std::stoi(numA.top);
	}
	else if (numA.type == 2 || numA.type == 3 || numA.type == -2 || numA.type == -3){
		a = std::stod(numA.top) / std::stod(numA.bottom);
	}
	else {
		return n;
	}

	std::string prod = "";
	if (fn == -32){
		if (a > 1 || a < -1) {return n;}
		prod = std::to_string(asin(a));
	}
	else if (fn == -31){
		if (a > 1 || a < -1) {return n;}
		prod = std::to_string(acos(a));
	}
	else if (fn == -30){
		prod = std::to_string(atan(a));
	}
	else if (fn == -29){
		if (a < 1 && a > -1) {return n;}
		prod = std::to_string(asin(1.0/a));
	}
	else if (fn == -28){
		if (a < 1 && a > -1) {return n;}
		prod = std::to_string(acos(1.0/a));
	}
	else if (fn == -27){
		if (a == 0) {return n;}
		prod = std::to_string(atan(1.0/a));
	}
	
	if (numbers.find(prod) == numbers.end()){
		numberType(prod);
	}
	n = numbers[prod];
	return n;

}

Number hypTrigTwo(char fn, const Number numA){ //numA is base and numB is inside part, of course
	int base = 10;
	int neg = 1;
	Number n;
	if (numA.type == 0){
		return n;
	}
	double a;
	if (numA.type == 1 || numA.type == -1){
		a = std::stoi(numA.top);
	}
	else if (numA.type == 2 || numA.type == 3 || numA.type == -2 || numA.type == -3){
		a = std::stod(numA.top) / std::stod(numA.bottom);
	}
	else {
		return n;
	}

	std::string prod = "";
	if (fn == -16){prod = std::to_string(sinh(a));}
	else if (fn == -15){prod = std::to_string(cosh(a));} 
	else if (fn == -14){double ca = cosh(a); if (ca != 0){prod = std::to_string(sinh(a)/ca);}} 
	else if (fn == -13){double sa = sinh(a); if (sa != 0){prod = std::to_string(1.0/sa);}} 
	else if (fn == -12){double ca = cosh(a); if (ca != 0){prod = std::to_string(1.0/ca);}} 
	else if (fn == -11){double sa = sinh(a); if (sa != 0){prod = std::to_string(cosh(a)/sa);}} 
	
	if (numbers.find(prod) == numbers.end()){
		numberType(prod);
	}
	n = numbers[prod];
	return n;

}

Number roundOne(const Number numA){
	int base = 10;
	int neg = 1;
	Number n;
	if (numA.type == 0){
		return n;
	}
	if (numA.type == 1 || numA.type == -1){
		n = numA;
		return n;
	}
	else if (numA.type == 2 || numA.type == -2 || numA.type == 3 || numA.type == -3){
		double a = std::stod(numA.top) / std::stod(numA.bottom);
		int aa = round(a);
		Number n;
		if (aa < 0){
			n.type = -1;
			n.top = std::to_string(aa*-1);
			n.bottom = "1";
		}
		else {
			n.type = 1;
			n.top = std::to_string(aa);
			n.bottom = "1";
		}
		return n;
	}
	
	
	return n;
}

Number rootNth(const Number numA, const Number numB){
	int base = 10;
	int neg = 1;
	Number n;

	if (numA.type == 1){
		int a = std::stoi(numA.top);
		double b;
		if (numB.type == 1){
			b = std::stoi(numB.top);
		}
		else if (numB.type == 2 || numB.type == 3){
			b = std::stod(numB.top) / std::stod(numB.bottom);
		}
		else if (numB.type < 0){
			if (a%2 == 0){n.type = 0; return n;}
			else {
				return negateOne(rootNth(numA,negateOne(numB)));
			}
		}
		double aa = 1.0;
		aa /= a;
		std::string prod = std::to_string(pow(b,aa));
		if (numbers.find(prod) == numbers.end()){
			numberType(prod);
		}
		n = numbers[prod];
		return n;
	}

	return n;
	
}

Number sqrtOne(const Number numA){
	if (numbers.find("2") == numbers.end()){
		numberType("2");
	}
	return rootNth(numbers["2"],numA);
}

flat_hash_map<std::string,Number> solvedPostfixMap;
Number solvePostfix(std::string postfix) {
	if (solvedPostfixMap.find(postfix) != solvedPostfixMap.end()){
		return solvedPostfixMap[postfix];
	}
	int i;
  	int currentIndex = 0;
  	int arrayIndex = 0;
  	std::vector<Number> stack;
  	std::vector<Number> intArray;
  	std::string currentOperand = "";
  	Number n;
  	//std::cout << "pf: " << postfix << "\n";
  	if (numbers.find("") == numbers.end()){
		numberType("");
	}
	if (numbers.find("-1") == numbers.end()){
		numberType("-1");
	}
	if (numbers.find("1") == numbers.end()){
		numberType("1");
	}
	if (numbers.find("0") == numbers.end()){
		numberType("0");
	}
  	for (i=0; i<postfix.length(); i++) 
    {
    	if (postfix.at(i) == '{'){
    		solvedPostfixMap[postfix] = n;
    		return n;
    	}
    	else if (postfix.at(i) == '@') {
        	currentOperand = "";
        }
        else if (postfix.at(i) == '_') {
			//TODO: convert to number here
			if (numbers.find(currentOperand) == numbers.end()){
				numberType(currentOperand);
			}
			intArray.push_back(numbers[currentOperand]);
			stack.push_back(numbers[""]);

        	currentOperand = "";
        }
        else {
        	currentOperand += postfix.at(i);
        }
    }

    for (i=0; i<postfix.length(); i++) 
    { 
    	//std::cout << "pfi: " << i << "\n";
        if (postfix.at(i) == '#') {
        	stack[currentIndex] = intArray[arrayIndex];
        	currentIndex++;
        	arrayIndex++;
  
        } 
        else if (postfix.at(i) == '@') {
        	break;
        }
        else 
        { 
            switch (postfix.at(i)) 
            { 
	            //case '>': stack[currentIndex - 2].w = (stack[currentIndex - 2] > stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break; 
	            //case '<': stack[currentIndex - 2].w = (stack[currentIndex - 2] < stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break;
	            //case ']': stack[currentIndex - 2].w = (stack[currentIndex - 2] >= stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break; 
	            //case '[': stack[currentIndex - 2].w = (stack[currentIndex - 2] <= stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break;
	            case '+': stack[currentIndex - 2] = addTwo(stack[currentIndex - 2],stack[currentIndex - 1]); break;
	            case '-': stack[currentIndex - 1] = negateOne(stack[currentIndex - 1]); currentIndex++; break; 
	            case '*': stack[currentIndex - 2] = mulTwo(stack[currentIndex - 2],stack[currentIndex - 1]); break; 
	            case '/': stack[currentIndex - 1] = invertOne(stack[currentIndex - 1]); currentIndex++; break;
	            case '^': stack[currentIndex - 2] = expTwo(stack[currentIndex - 2],stack[currentIndex - 1]); break;
	            case -93: stack[currentIndex - 2] = logTwo(stack[currentIndex - 2],stack[currentIndex - 1]); break;
	            case -84: stack[currentIndex - 2] = rootNth(stack[currentIndex - 2],stack[currentIndex - 1]); break;
	            case -82: stack[currentIndex - 1] = roundOne(stack[currentIndex - 1]); currentIndex++; break;
	            case -67: stack[currentIndex - 1] = sqrtOne(stack[currentIndex - 1]); currentIndex++; break;
	            case -64: stack[currentIndex - 1] = trigTwo(-64,stack[currentIndex - 1]); currentIndex++; break;
	            case -63: stack[currentIndex - 1] = trigTwo(-63,stack[currentIndex - 1]); currentIndex++; break;
	            case -62: stack[currentIndex - 1] = trigTwo(-62,stack[currentIndex - 1]); currentIndex++; break;
	            case -61: stack[currentIndex - 1] = trigTwo(-61,stack[currentIndex - 1]); currentIndex++; break;
	            case -60: stack[currentIndex - 1] = trigTwo(-60,stack[currentIndex - 1]); currentIndex++; break;
	            case -59: stack[currentIndex - 1] = trigTwo(-59,stack[currentIndex - 1]); currentIndex++; break;
	            case -32: stack[currentIndex - 1] = invTrigTwo(-32,stack[currentIndex - 1]); currentIndex++; break;
	            case -31: stack[currentIndex - 1] = invTrigTwo(-31,stack[currentIndex - 1]); currentIndex++; break;
	            case -30: stack[currentIndex - 1] = invTrigTwo(-30,stack[currentIndex - 1]); currentIndex++; break;
	            case -29: stack[currentIndex - 1] = invTrigTwo(-29,stack[currentIndex - 1]); currentIndex++; break;
	            case -28: stack[currentIndex - 1] = invTrigTwo(-28,stack[currentIndex - 1]); currentIndex++; break;
	            case -27: stack[currentIndex - 1] = invTrigTwo(-27,stack[currentIndex - 1]); currentIndex++; break;
	            case -16: stack[currentIndex - 1] = hypTrigTwo(-16,stack[currentIndex - 1]); currentIndex++; break;
	            case -15: stack[currentIndex - 1] = hypTrigTwo(-15,stack[currentIndex - 1]); currentIndex++; break;
	            case -14: stack[currentIndex - 1] = hypTrigTwo(-14,stack[currentIndex - 1]); currentIndex++; break;
	            case -13: stack[currentIndex - 1] = hypTrigTwo(-13,stack[currentIndex - 1]); currentIndex++; break;
	            case -12: stack[currentIndex - 1] = hypTrigTwo(-12,stack[currentIndex - 1]); currentIndex++; break;
	            case -11: stack[currentIndex - 1] = hypTrigTwo(-11,stack[currentIndex - 1]); currentIndex++; break;
	            case '=': {
	            	if (stack[currentIndex - 2] == stack[currentIndex - 1]){
	            		Number nn;
	            		nn.type = 1;
	            		nn.top = "1";
	            		stack[currentIndex - 2] = nn;
	            		break;
	            	}
	            	else {
	            		Number nn;
	            		nn.type = 1;
	            		nn.top = "0";
	            		stack[currentIndex - 2] = nn;
	            		break;
	            	}
	            }
	            case '>': {
	            	if (stack[currentIndex - 2] > stack[currentIndex - 1]){
	            		Number nn;
	            		nn.type = 1;
	            		nn.top = "1";
	            		stack[currentIndex - 2] = nn;
	            		break;
	            	}
	            	else {
	            		Number nn;
	            		nn.type = 1;
	            		nn.top = "0";
	            		stack[currentIndex - 2] = nn;
	            		break;
	            	}
	            }
	            case '<': {
	            	if (stack[currentIndex - 2] > stack[currentIndex - 1]){
	            		Number nn;
	            		nn.type = 1;
	            		nn.top = "1";
	            		stack[currentIndex - 2] = nn;
	            		break;
	            	}
	            	else {
	            		Number nn;
	            		nn.type = 1;
	            		nn.top = "0";
	            		stack[currentIndex - 2] = nn;
	            		break;
	            	}
	            }
	            case ']': {
	            	if (stack[currentIndex - 2] < stack[currentIndex - 1]){
	            		Number nn;
	            		nn.type = 1;
	            		nn.top = "0";
	            		stack[currentIndex - 2] = nn;
	            		break;
	            	}
	            	else {
	            		Number nn;
	            		nn.type = 1;
	            		nn.top = "1";
	            		stack[currentIndex - 2] = nn;
	            		break;
	            	}
	            }
	            case '[': {
	            	if (stack[currentIndex - 2] > stack[currentIndex - 1]){
	            		Number nn;
	            		nn.type = 1;
	            		nn.top = "0";
	            		stack[currentIndex - 2] = nn;
	            		break;
	            	}
	            	else {
	            		Number nn;
	            		nn.type = 1;
	            		nn.top = "1";
	            		stack[currentIndex - 2] = nn;
	            		break;
	            	}
	            }
	            case '!': {
	            	if (stack[currentIndex - 2] == stack[currentIndex - 1]){
	            		Number nn;
	            		nn.type = 1;
	            		nn.top = "0";
	            		stack[currentIndex - 2] = nn;
	            		break;
	            	}
	            	else {
	            		Number nn;
	            		nn.type = 1;
	            		nn.top = "1";
	            		stack[currentIndex - 2] = nn;
	            		break;
	            	}
	            }
	            default: n.type = 0; solvedPostfixMap[postfix] = n; return n;
	            //case '!': stack[currentIndex - 2] = stack[currentIndex - 2] != stack[currentIndex - 1]; break;
	            //case '%': stack[currentIndex - 2] = stack[currentIndex - 2] % stack[currentIndex - 1]; break; 
	            //case '&': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w > 1) ? 1 : 0; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            //case '|': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w == 0) ? 0 : 1; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            //multiandcase '&': if (stack[currentIndex - 5] > 0 && stack[currentIndex - 4] > 0 && stack[currentIndex - 3] > 0 && stack[currentIndex - 2] > 0 && stack[currentIndex - 1] > 0) {stack[currentIndex - 5] = 1;} else {stack[currentIndex - 5] = -1;}; currentIndex--; currentIndex--; currentIndex--; currentIndex--; break; 
            
            } 
            currentIndex--;
        } 
    } 
	
	//std::cout << "pfb: " << postfix << " and " << stack[0].type << " and " << outputNumber(stack[0]) << "\n";
	solvedPostfixMap[postfix] = stack[0];
	return stack[0];
}

std::vector<std::string> factorList(std::string input) {

	int i;
	int n = std::stoi(input);
	if (n<1){
		return {};
	}
	std::vector<std::string> list;
	list.push_back("1");
	for (i=2;i<n;i++){
		if (n%i == 0){
			list.push_back(std::to_string(i));
		}
	}
	list.push_back(input);
	return list;
}
flat_hash_map<std::string,std::string> conditionalPostfixList;

std::string solveConditionalPostfix(std::string var){
	if (conditionalPostfixList.find(var) != conditionalPostfixList.end()){
		return conditionalPostfixList[var];
	}
	std::vector<Number> possibleValues;
	std::string x = "";
	std::string xxl = "";
	std::string xxr = "";
	std::string expressionl = "";
	std::string expressionr = "";
	bool pastKey = false;
	bool pastFirst = false;
	int idx = 1;
	int i;
	std::string currentOperand = "";
	for (i=1;i<var.length();i++){
		if (var.at(i) == '@'){
			pastKey = true;
			pastFirst = false;
		}
		else if (var.at(i) == -95){
			pastFirst = true;
		}
		else if (var.at(i) == '&'){
		
		}
		else if (!pastFirst && !pastKey){
			xxl += var.at(i);
			if (var.at(i)=='#'){
				idx++;
			}
		}
		else if (pastFirst && !pastKey){
			expressionl += var.at(i);
		}
		else if (!pastFirst && pastKey){
			if (var.at(i) == '_'){
				pastFirst = true;
				idx--;
			}
			else {
				x += var.at(i);
			}
		}
		else {
			if (idx > 0){
				xxr += var.at(i);
			}
			else {
				expressionr += var.at(i);
			}
			if (var.at(i) == '_'){
				idx--;
			}
		}
	}
	std::string xxrp = xxr.substr(0,xxr.length()-1);
	if (numbers.find(xxrp) == numbers.end()){
		numberType(xxrp);
	}
	if (numbers[xxrp].type != 1 && numbers[xxrp].type != -1){
		conditionalPostfixList[var]="##@";
		return "##@";
	}

		
		std::vector<std::string> list = factorList(xxrp);
		int ii;
		for (ii=0;ii<list.size();ii++){
			std::string currentOperand = "";
			std::string newPostfix = expressionl+"@";
			for (i=0;i<expressionr.length();i++){
				if (expressionr.at(i) == '_'){
					if (currentOperand == x){
						newPostfix += list[ii]+"_";
					}
					else {
						if (numbers.find(currentOperand) == numbers.end()){
							numberType(currentOperand);
						}
						if (numbers[currentOperand].type != 1 && numbers[currentOperand].type != -1){
							conditionalPostfixList[var]="##@";
							return "##@";
						}
						newPostfix += currentOperand+"_";
					}
					currentOperand = "";
				}
				else {
					currentOperand += expressionr.at(i);
				}
			}
			Number n = solvePostfix(newPostfix);
			if (n.type == 1 && n.top == "1"){
				//std::cout << "npf: " << newPostfix << " and " << "true"<< "\n";
				conditionalPostfixList[var]="##=@C_"+list[ii]+"_";
				return "##=@C_"+list[ii]+"_";
			}
			
		}
		//std::cout << "var: " << var << " and " << x << " and " << xxl << " and " << xxr << " and " << expressionl << " and " << expressionr << "\n";
	
	conditionalPostfixList[var]="##@";
	return "##@";
}

std::vector<std::string> varToX(std::string var) {
	std::string x = "";
	std::string xxl = "";
	std::string xxr = "";
	bool pastKey = false;
	int idx = 0;
	int i;
	for (i=1;i<var.length();i++){
		if (var.at(i) == '@'){
			if (i>0 && var.at(i-1) == '&'){
				var = solveConditionalPostfix(var);
				return varToX(var);
			}
			if (i>0 && var.at(i-1) != '='){
				return {};
			}
			pastKey = true;
		}
		else if (var.at(i) == '_'){
			if (idx == 0){
				
			}
			else {
				xxr += var.at(i);
			}
			idx++;
		}
		else if (var.at(i) == '=' && !pastKey){
			if (i+1<var.length() && var.at(i+1) == '@'){
			
			}
			else {
				xxl += var.at(i);
			}
		}
		else {
			if (pastKey && idx>0){
				xxr += var.at(i);
			}
			else if (pastKey){
				x += var.at(i);
			}
			else {
				xxl += var.at(i);
			}
		}
	}
	return {x,xxl,xxr};
}

std::string substitute(std::string input){
	std::string returnStr = "("+input+")";
	if (input.length() < 4){
		return returnStr;
	}
	std::string var = "";
	int i;
	if (input.at(0) != '#' || input.at(1) != '#' || input.at(2) != -102 || input.at(3) != '@'){
		//TODO: grab the part up to & and convert to format
		std::string left = "";
		std::string right = "";
		std::string left2 = "";
		std::string right2 = "";
		bool pastKey= false;
		bool pastAnd= false;
		int idx = 0;
		for (i=0;i<input.length();i++){
			if (input.at(i)=='{'){
				return returnStr;
			}
			
			
			if (input.at(i)=='&'){
				pastAnd = true;
				left += input.at(i);
			}
			else if (input.at(i)=='@'){
				pastKey = true;
			}
			else if (!pastAnd){
				left += input.at(i);
				if (input.at(i)=='#'){
					idx++;
				}
			}
			else if (pastAnd && !pastKey){
				if (input.at(i) != -102){
					left2 += input.at(i);
				}
			}
			else if (pastKey && input.at(i)=='_'){
				if (idx >0){
					right += input.at(i);
				}
				else {
					right2 += input.at(i);
				}
				idx--;
				
			}
			else if (pastKey && idx > 0){
				right += input.at(i);
			}
			else if (pastKey){
				right2 += input.at(i);
			}
		}
		std::cout << "l: " << left << " and " << right << "\n";
		std::cout << "l2: " << left2 << " and " << right2 << "\n";
		var = solveConditionalPostfix(left + "@" + right);
		if (var == "##@"){
			std::cout << "fin: nothing" << "\n";
			return returnStr;
		}
		char sub{-102};
		std::string substr = "";
		substr += sub;
		input = "##"+substr+"@{"+var+"}_{"+left2+"@"+right2+"}_";
		std::cout << "fin: "<< input << "\n";
	}
	var = "";
	std::string expression = "";
	bool isExpression = false;
	bool inBrackets = false;
	for (i=4;i<input.length();i++){
		if (input.at(i)=='{'){
			inBrackets = true;
		}
		else if (input.at(i)=='}'){
			inBrackets = false;
		}
		else if (input.at(i)=='_'){
			if (inBrackets){
				if (isExpression){
					expression += input.at(i);
				}
				else {
					var += input.at(i);
				}
			}
			else {
				isExpression = true;
			}
		}
		else {
			if (isExpression){
				expression += input.at(i);
			}
			else {
				var += input.at(i);
			}
		}
	}
	//std::cout << "var: " << var << " and " << expression << "\n";
	std::string x = "";
	std::string xxl = "";
	std::string xxr = "";
	bool pastKey = false;
	int idx = 0;
	std::vector<std::string> xv = varToX(var);
	if (xv.size() < 3){
		return returnStr;
	}
	x = xv[0]; xxl = xv[1]; xxr = xv[2];

	std::string currentOperand = "";
	pastKey = false;
	idx=0;
	std::string newPostfix = "";
	//std::cout << "x: " << x << " and " << xxl << " and " << xxr << "\n";
	for (i=0;i<expression.length();i++){
		if (expression.at(i) == '@'){
			pastKey = true;
			newPostfix += "@";
		}
		else if (expression.at(i) == '_'){
			if (currentOperand == x){
				newPostfix += "{"+xxl+"@"+xxr+"}_";
			}
			else {
				newPostfix += currentOperand+"_";
			}
			currentOperand = "";
		}
		else if (pastKey){
			currentOperand += expression.at(i);
		}
		else {
			newPostfix += expression.at(i);
		}
	}
	//std::cout << "newPostfix: " << newPostfix << "\n";
	if (newPostfix != input){
		std::cout << input << " andand " << newPostfix << "\n";
	}
	return "("+newPostfix+")";
}