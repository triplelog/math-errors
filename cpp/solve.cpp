
struct Number {
	int type = 0;
	std::string top = "";
	std::string bottom = "";
}
flat_hash_map<std::string,Number> numbers;

std::string numberType(std::string input){
	if (input.length()==0){
		return "string";
	}
	
	Number n;
	if (input.at(0) == '-'){
		input.replace(0,1,"");
		std::string rest = "";
		if (numbers.find(input) != numbers.end){
			rest = numbers[input].type;
		}
		else {
			rest = numberType(input);
		}
		 
		if (rest == "string" || rest.at(0) == 'n'){
			return "string";
		}
		else {
			n.type = numbers[input].type*-1;
			n.top = numbers[input].top;
			n.bottom = numbers[input].bottom;
			numbers["-"+input] = n;
			return "n"+rest;
		}
	}
	int ii;
	std::string currentType = "int";
	for(ii=0;ii<input.length();ii++){
		switch(input.at(ii)){
			case '.': {
				if (currentType == "int"){currentType = "dec";}
				else if (currentType == "dec"){return "string";}
				else if (currentType == "red"){return "string";}
				else if (currentType == "rep"){currentType = "red";}
				else if (currentType == "sci" || currentType == "scn"){return "string";}
				n.top = input.substr(0,ii);
				n.bottom = input.substr(ii+1,input.length()-ii-1);
				break;
			}
			case '_': {
				if (currentType == "int"){currentType = "rep";}
				else if (currentType == "dec"){currentType = "red";}
				else if (currentType == "red"){return "string";}
				else if (currentType == "rep"){return "string";}
				else if (currentType == "sci" || currentType == "scn"){return "string";}
				break;
			}
			case 'e': {
				if (currentType == "int"){currentType = "sci";}
				else if (currentType == "dec"){currentType = "sci";}
				else if (currentType == "red"){currentType = "sci";}
				else if (currentType == "rep"){currentType = "sci";}
				else if (currentType == "sci" || currentType == "scn"){return "string";}
				n.top = input.substr(0,ii);
				n.bottom = input.substr(ii+1,input.length()-ii-1);
				break;
			}
			case '-': {
				if (currentType == "int"){return "string";}
				else if (currentType == "dec"){return "string";}
				else if (currentType == "red"){return "string";}
				else if (currentType == "rep"){return "string";}
				else if (currentType == "sci"){currentType = "scn";}
				else if (currentType == "scn"){return "string";}
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
			default: return "string";

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
		n.top = n.top+n.bottom;
		int nbl = n.bottom.length();
		n.bottom = "1":
		for (ii=0;ii<nbl;ii++){
			n.bottom += "0";
		}
		numbers[input]=n;
		return "dec";
	}
	else if (currentType == "red"){
		n.type = 3;
		//TODO: make correct top and bottom
		numbers[input]=n;
		return "rep";
	}
	else if (currentType == "sci" || currentType == "scn"){
		n.type = 4;
		numbers[input]=n;
		return "sci";
	}
	else {return "string";}
	return "string";
}

std::string addTwo(std::string a, std::string b){
	std::string revsum = "";
	int base = 10;
	Number numA;
	Number numB;
	if (numbers.find(a) != numbers.end()){
		if (numberType(a) == "string"){
			return "false";
		}
		else{
			numA = numbers[a];
		}
	}
	if (numbers.find(b) != numbers.end()){
		if (numberType(b) == "string"){
			return "false";
		}
		else{
			numB = numbers[b];
		}
	}
	
	if (numA.type == 1 && numB.type == 1){
		a = numA.top;
		b = numB.top;
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
			if (aa<0 || aa>9){
				return "false";
			}
			int bb = b.at(len-1-i) - '0';
			if (bb<0 || bb>9){
				return "false";
			}
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
		return sum;
		}
	}
	return "false";

}

std::string mulTwoInts(std::string a, std::string b){
	int base = 10;
	int neg = 1;
	if (a.at(0) == '-'){
		a.replace(0,1,"");
		neg *= -1;
	}
	if (b.at(0) == '-'){
		b.replace(0,1,"");
		neg *= -1;
	}
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
	for (i=0;i<a.length();i++){
		int aa = a.at(len-1-i) - '0';
		if (aa<0 || aa>9){
			return "false";
		}
		int bb = b.at(len-1-i) - '0';
		if (bb<0 || bb>9){
			return "false";
		}
	}
	int prod = std::stoi(a);
	prod *= std::stoi(b);
	prod *= neg;
	return std::to_string(prod);
}

std::string divTwoInts(std::string a, std::string b){
	int base = 10;
	int i;
	int len = a.length();
	for (i=0;i<len;i++){
		int aa = a.at(len-1-i) - '0';
		if (aa<0 || aa>9){
			return "false";
		}
	}
	len = b.length();
	for (i=0;i<len;i++){
		int bb = b.at(len-1-i) - '0';
		if (bb<0 || bb>9){
			return "false";
		}
	}
	int div = std::stoi(a);
	int divb = std::stoi(b);
	if (divb == 0){return "false";}
	if (div % divb == 0){
		div /= divb;
	}
	else {
		return "false";
	}
	return std::to_string(div);
}

std::string subTwoInts(std::string a, std::string b){
	int base = 10;
	int i;
	int len = a.length();
	for (i=0;i<len;i++){
		int aa = a.at(len-1-i) - '0';
		if (aa<0 || aa>9){
			return "false";
		}
	}
	len = b.length();
	for (i=0;i<len;i++){
		int bb = b.at(len-1-i) - '0';
		if (bb<0 || bb>9){
			return "false";
		}
	}
	int div = std::stoi(a);
	div -= std::stoi(b);
	return std::to_string(div);
}

std::string solvePostfix(std::string postfix) {
	int i;
  	int currentIndex = 0;
  	int arrayIndex = 0;
  	std::vector<std::string> stack;
  	std::vector<std::string> intArray;
  	std::string currentOperand = "";
  	for (i=0; i<postfix.length(); i++) 
    {
    	if (postfix.at(i) == '{'){
    		return "false";
    	}
    	else if (postfix.at(i) == '@') {
        	currentOperand = "";
        }
        else if (postfix.at(i) == '_') {

			intArray.push_back(currentOperand);
			stack.push_back("");

        	currentOperand = "";
        }
        else {
        	currentOperand += postfix.at(i);
        }
    }

    for (i=0; i<postfix.length(); i++) 
    { 
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
	            case '-': stack[currentIndex - 2] = subTwoInts(stack[currentIndex - 2],stack[currentIndex - 1]); i++; break; 
	            case '*': stack[currentIndex - 2] = mulTwoInts(stack[currentIndex - 2],stack[currentIndex - 1]); break; 
	            case '/': stack[currentIndex - 1] = divTwoInts("1",stack[currentIndex - 1]); currentIndex++; break;
	            //case '=': stack[currentIndex - 2] = stack[currentIndex - 2] == stack[currentIndex - 1]; break;
	            //case '!': stack[currentIndex - 2] = stack[currentIndex - 2] != stack[currentIndex - 1]; break;
	            //case '%': stack[currentIndex - 2] = stack[currentIndex - 2] % stack[currentIndex - 1]; break; 
	            //case '&': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w > 1) ? 1 : 0; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            //case '|': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w == 0) ? 0 : 1; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            //multiandcase '&': if (stack[currentIndex - 5] > 0 && stack[currentIndex - 4] > 0 && stack[currentIndex - 3] > 0 && stack[currentIndex - 2] > 0 && stack[currentIndex - 1] > 0) {stack[currentIndex - 5] = 1;} else {stack[currentIndex - 5] = -1;}; currentIndex--; currentIndex--; currentIndex--; currentIndex--; break; 
            
            } 
            currentIndex--;
        } 
    } 



	return stack[0];
}
/*
inline Cppdata solvePostfixVV(char expstr[], std::vector<Cppdata> const intArray, std::vector<Cppdata> stack)
{

	int i;
  	int currentIndex = 0;
  	int arrayIndex = 0;

    for (i = 0; expstr[i]; i++) 
    { 
        if (expstr[i] == '#') {
        	stack[currentIndex] = intArray[arrayIndex];
        	currentIndex++;
        	arrayIndex++;
  
        } else 
        { 
            switch (expstr[i]) 
            { 
	            case '>': stack[currentIndex - 2].w = (stack[currentIndex - 2] > stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break; 
	            case '<': stack[currentIndex - 2].w = (stack[currentIndex - 2] < stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break;
	            case ']': stack[currentIndex - 2].w = (stack[currentIndex - 2] >= stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break; 
	            case '[': stack[currentIndex - 2].w = (stack[currentIndex - 2] <= stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break;
	            case '+': stack[currentIndex - 2] = stack[currentIndex - 2] + stack[currentIndex - 1]; break; 
	            case '-': stack[currentIndex - 2] = stack[currentIndex - 2] - stack[currentIndex - 1]; break; 
	            case '*': stack[currentIndex - 2] = stack[currentIndex - 2] * stack[currentIndex - 1]; break; 
	            case '/': stack[currentIndex - 2] = stack[currentIndex - 2] / stack[currentIndex - 1]; break;
	            case '=': stack[currentIndex - 2] = stack[currentIndex - 2] == stack[currentIndex - 1]; break;
	            case '!': stack[currentIndex - 2] = stack[currentIndex - 2] != stack[currentIndex - 1]; break;
	            //case '%': stack[currentIndex - 2] = stack[currentIndex - 2] % stack[currentIndex - 1]; break; 
	            case '&': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w > 1) ? 1 : 0; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            case '|': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w == 0) ? 0 : 1; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            //multiandcase '&': if (stack[currentIndex - 5] > 0 && stack[currentIndex - 4] > 0 && stack[currentIndex - 3] > 0 && stack[currentIndex - 2] > 0 && stack[currentIndex - 1] > 0) {stack[currentIndex - 5] = 1;} else {stack[currentIndex - 5] = -1;}; currentIndex--; currentIndex--; currentIndex--; currentIndex--; break; 
            
            } 
            currentIndex--;
        } 
    } 



	return stack[0];

}
*/