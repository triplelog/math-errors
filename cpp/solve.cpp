
struct Number {
	int type = 0;
	std::string top = "";
	std::string bottom = "";
};
inline bool operator>(const Number& a, const Number& b){
	if (a.type == 1){
		if (b.type == 1){
			if (a.top.length()>b.top.length()){
				return true;
			}
			else if (a.top.length()<b.top.length()){
				return false;
			}
			else {
				int ii;
				for (ii=0;ii<a.top.length();ii++){
					if (a.top.at(ii) > b.top.at(ii)){
						return true;
					}
					else if (a.top.at(ii) < b.top.at(ii)){
						return false;
					}
				}
				return false;
			}
		}
		else if (b.type == -1){
			return true;
		}
	}
	return true;
}
inline bool operator<(const Number& a, const Number& b){
	if (a.type == 1){
		if (b.type == 1){
			if (a.top.length()<b.top.length()){
				return true;
			}
			else if (a.top.length()>b.top.length()){
				return false;
			}
			else {
				int ii;
				for (ii=0;ii<a.top.length();ii++){
					if (a.top.at(ii) < b.top.at(ii)){
						return true;
					}
					else if (a.top.at(ii) > b.top.at(ii)){
						return false;
					}
				}
				return false;
			}
		}
		else if (b.type == -1){
			return false;
		}
	}
	return true;
}
inline bool operator==(const Number& a, const Number& b){
	if (a<b || a>b){
		return false;
	}
	return true;
}
flat_hash_map<std::string,Number> numbers;

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
			return "string";
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
				else if (currentType == "dec"){return "string";}
				else if (currentType == "red"){return "string";}
				else if (currentType == "rep"){return "string";}
				else if (currentType == "sci" || currentType == "scn"){return "string";}
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
					return "string";
				}
				else if (currentType == "dec"){currentType = "red"; idx = ii - idx;}
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
		n.bottom = "1";
		for (ii=0;ii<nbl;ii++){
			n.bottom += "0";
		}
		numbers[input]=n;
		return "dec";
	}
	else if (currentType == "red"){
		n.type = 3;
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
	}
	else if (currentType == "sci" || currentType == "scn"){
		n.type = 4;
		numbers[input]=n;
		return "sci";
	}
	else {return "string";}
	return "string";
}

Number negateOne(Number numA){
	Number n;
	n.type = -1*numA.type;
	n.top = numA.top;
	n.bottom = numA.bottom;
	return n;
}
Number invertOne(Number numA){
	Number n;
	return n;
	if (numA.type == 0){
		n.type = 0; return n;
	}
	else if (numA.type == 1 || numA.type == -1){
		if (numA.top == "1"){n = numA; return n;}
		if (numA.top == "0"){n.type = 0; return n;}
		n.type = 5*numA.type;
		n.top = "1";
		n.bottom = numA.top;
		return n;
	}
	else if (numA.type == 2 || numA.type == -2){
		//TODO: create decimal unless == 0
	}
	else if (numA.type == 3 || numA.type == -3){
		//TODO: create decimal unless == 0
	}
	else if (numA.type == 4 || numA.type == -4){
		//TODO: create sci not unless == 0
	}
	else if (numA.type == 5 || numA.type == -5){
		if (numA.top == "0"){n.type = 0; return n;}
		if (numA.top == "1"){n.type = 1*numA.type/5; n.top = numA.bottom; return n;}
		n.type = numA.type;
		n.top = numA.bottom;
		n.bottom = numA.top;
		return n;
	}
	//TODO: create number type for division by zero
	return n;
}

Number addTwo(Number numA, Number numB){
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
			for (i=revsum.length()-1;i>=0;i--){
				sum += revsum.at(i);
			}
			if (numbers.find(sum) == numbers.end()){
				numberType(sum);
			}
			return numbers[sum];
		}
		else if (numB.type == 2 || numB.type == -2){
			n.type = 2; n.top = numA.top; n.bottom = "0";
			return addTwo(n,numB);
		}
	}
	else if (numA.type == 2){
		if (numB.type == 2){
			
		}
	}
	else if (numA.type < 0){
		if (numB.type > 0){
			return addTwo(numB,numA);
		}
		else if (numB.type < 0){
			return negateOne(addTwo(negateOne(numA),negateOne(numA)));
		}
	}
	return n;

}

Number mulTwoInts(Number numA, Number numB){
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
	}
	else if (numA.type == -1){
		if (numB.type == 1){
			n.type = -1;
			int prod = std::stoi(numA.top);
			prod *= std::stoi(numB.top);
			n.top = std::to_string(prod);
			return n;
		}
		else if (numB.type == -1){
			n.type = 1;
			int prod = std::stoi(numA.top);
			prod *= std::stoi(numB.top);
			n.top = std::to_string(prod);
			return n;
		}
	}
	return n;
}

Number expTwo(Number numA, Number numB){
	int base = 10;
	int neg = 1;
	Number n;
	//TODO: implement exponentiation instead of multiplication
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
	}
	else if (numA.type == -1){
		if (numB.type == 1){
			n.type = -1;
			int prod = std::stoi(numA.top);
			prod *= std::stoi(numB.top);
			n.top = std::to_string(prod);
			return n;
		}
		else if (numB.type == -1){
			n.type = 1;
			int prod = std::stoi(numA.top);
			prod *= std::stoi(numB.top);
			n.top = std::to_string(prod);
			return n;
		}
	}
	return n;
}

Number divTwoInts(Number numA, Number numB){
	int base = 10;
	int neg = 1;
	Number n;
	if (numA.type == 1){
		if (numB.type == 1 || numB.type == -1){
			if (numB.top == "0"){
				return n;
			}
			n.type = numB.type;
			int div = std::stoi(numA.top);
			div /= std::stoi(numB.top);
			n.top = std::to_string(div);
			return n;
		}
	}
	else if (numA.type == -1){
		if (numB.type == 1 || numB.type == -1){
			if (numB.top == "0"){
				return n;
			}
			n.type = -1 * numB.type;
			int div = std::stoi(numA.top);
			div /= std::stoi(numB.top);
			n.top = std::to_string(div);
			return n;
		}
	}
	return n;
}

Number solvePostfix(std::string postfix) {
	int i;
  	int currentIndex = 0;
  	int arrayIndex = 0;
  	std::vector<Number> stack;
  	std::vector<Number> intArray;
  	std::string currentOperand = "";
  	Number n;
  	if (numbers.find("") != numbers.end()){
		numberType("");
	}
	if (numbers.find("-1") != numbers.end()){
		numberType("-1");
	}
	if (numbers.find("1") != numbers.end()){
		numberType("1");
	}
  	for (i=0; i<postfix.length(); i++) 
    {
    	if (postfix.at(i) == '{'){
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
	            case '*': stack[currentIndex - 2] = mulTwoInts(stack[currentIndex - 2],stack[currentIndex - 1]); break; 
	            case '/': {
	            	if (currentIndex > 1){
	            		stack[currentIndex - 2] = divTwoInts(stack[currentIndex - 2],stack[currentIndex - 1]); i++; break;
	            	}
	            	else {
	            		stack[currentIndex - 1] = invertOne(stack[currentIndex - 1]); currentIndex++; break;
	            	}
	            }
	            case '^': stack[currentIndex - 2] = expTwo(stack[currentIndex - 2],stack[currentIndex - 1]); break;
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
	            //case '!': stack[currentIndex - 2] = stack[currentIndex - 2] != stack[currentIndex - 1]; break;
	            //case '%': stack[currentIndex - 2] = stack[currentIndex - 2] % stack[currentIndex - 1]; break; 
	            //case '&': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w > 1) ? 1 : 0; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            //case '|': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w == 0) ? 0 : 1; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            //multiandcase '&': if (stack[currentIndex - 5] > 0 && stack[currentIndex - 4] > 0 && stack[currentIndex - 3] > 0 && stack[currentIndex - 2] > 0 && stack[currentIndex - 1] > 0) {stack[currentIndex - 5] = 1;} else {stack[currentIndex - 5] = -1;}; currentIndex--; currentIndex--; currentIndex--; currentIndex--; break; 
            
            } 
            currentIndex--;
        } 
    } 

	//std::cout << "pf: " << postfix << " and " << stack[0].type << " and " << stack[0].top << "\n";
	return stack[0];
}

std::vector<std::string> factorList(std::string input) {
	int i;
	int n = std::stoi(input);
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
	if (expressionr == "C_12_C_7_" && expressionl == "###/*+#="){
		
		std::vector<std::string> list = factorList(xxr.substr(0,xxr.length()-1));
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
				std::cout << "npf: " << newPostfix << " and " << "true"<< "\n";
				conditionalPostfixList[var]="##=@C_"+list[ii]+"_";
				return "##=@C_"+list[ii]+"_";
			}
			
		}
		std::cout << "var: " << var << " and " << x << " and " << xxl << " and " << xxr << " and " << expressionl << " and " << expressionr << "\n";
	}
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
	if (input.at(0) != '#' || input.at(1) != '#' || input.at(2) != -89 || input.at(3) != '@'){
		//TODO: grab the part up to & and convert to format
		std::string left = "";
		std::string right = "";
		std::string left2 = "";
		std::string right2 = "";
		bool pastKey= false;
		bool pastAnd= false;
		int idx = 0;
		for (i=0;i<input.length();i++){
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
				if (input.at(i) != -89){
					left2 += input.at(i);
				}
			}
			else if (pastKey && input.at(i)=='_'){
				if (idx >0){
					right += input.at(i);
				}
				idx--;
				
			}
			else if (pastKey && idx > 0){
				right += input.at(i);
			}
			else if (pastKey){
				right2 + input.at(i);
			}
		}
		std::cout << "l: " << left << " and " << right << "\n";
		std::cout << "l2: " << left2 << " and " << right2 << "\n";
		var = solveConditionalPostfix(left + "@" + right);
		char sub{-89};
		std::string substr = "";
		substr += sub;
		input = "##"+substr+"@{"+var+"}_{"+left2+"@"+right2+"}_";
		std::cout << input << "\n";
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
	std::cout << "var: " << var << " and " << expression << "\n";
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
	std::cout << "x: " << x << " and " << xxl << " and " << xxr << "\n";
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
	std::cout << "newPostfix: " << newPostfix << "\n";
	return "("+newPostfix+")";
}