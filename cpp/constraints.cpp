bool solveConstraintFix(std::string input){
	int i; int ii; int iii;
	bool postKey = false;\
	
	std::string firstPart = "";
	std::string secondPart = "";
	std::string firstExp = "";
	std::string secondExp = "";
	char lastOp = '=';
	bool inBrackets = false;
	flat_hash_map<std::string,bool> expressionMap;
	std::vector<std::string> operandList;
	std::string currentOperand ="";
	expressionMap["#"]=true;
	for (i=0;i<input.length();i++){
	
		if (postKey){
			if (input.at(i) == '{'){
				inBrackets = true;
				currentOperand = "{";
			}
			else if (input.at(i) == '}'){
				inBrackets = false;
				currentOperand += "}";
			}
			else if (inBrackets){
				currentOperand += input.at(i);
			}
			else if (input.at(i) == '_'){
				operandList.push_back(currentOperand);
				currentOperand ="";
			}
			else {
				currentOperand += input.at(i);
			}
		}
		else if (input.at(i) == '@'){
			postKey = true;
			
		}
		else if (input.at(i) != '#'){
			std::string tempExp = "";
			int maxi = 0;
			for (ii=0;ii<i;ii++){
				tempExp = "";
				for (iii=ii;iii<i;iii++){
					tempExp += input.at(iii);
				}
				if (expressionMap.find(tempExp) != expressionMap.end()){
					maxi = ii;
					secondPart = tempExp;
					break;
				}
			}
			if (input.at(i) != '-' && input.at(i) != '/' && (input.at(i) >= 0 || input.at(i) <= -69)){
				for (ii=0;ii<maxi;ii++){
					tempExp = "";
					for (iii=ii;iii<maxi;iii++){
						tempExp += input.at(iii);
					}
					if (expressionMap.find(tempExp) != expressionMap.end()){
						maxi = ii;
						firstPart = tempExp;
						break;
					}
				}
			}
			tempExp = "";
			for (ii=maxi;ii<i+1;ii++){
				tempExp += input.at(iii);
			}
			expressionMap[tempExp]=true;
			lastOp= input.at(i);
		}

	}
	firstExp = firstPart + "@";
	int idx = 0;
	for (i=0;i<firstPart.length();i++){
		if (firstPart.at(i) =='#'){
			firstExp += operandList[idx]+"_";
			idx++;
		}
	}
	int firstIdx = idx;
	secondExp = secondPart + "@";
	for (i=0;i<secondPart.length();i++){
		if (secondPart.at(i) =='#'){
			secondExp += operandList[idx]+"_";
			idx++;
		}
	}
	firstExp = removeBracketsOne(firstExp);
	secondExp = removeBracketsOne(secondExp);
	
	std::cout << "constraint: "<< input << " and " << firstExp << " and " << secondExp << " and " << lastOp << "\n";
	
	if (lastOp == -94){ //does not contain--secondExp must be single operand
		currentOperand = "";
		postKey = false;
		if (operandList.size()>firstIdx+1){
			return false;
		}
		for (i=0;i<firstExp.length();i++){
	
			if (postKey){
				if (firstExp.at(i) == '_'){
					if (currentOperand==operandList[firstIdx]){
						return false;
					}
					currentOperand ="";
				}
				else {
					currentOperand += firstExp.at(i);
				}
			}
			else if (firstExp.at(i) == '@'){
				postKey = true;
			
			}
		}
		std::cout << "was true" << "\n";
		return true;
	}
	else if (lastOp == -87){ //contains--secondExp must be single operand
		currentOperand = "";
		postKey = false;
		if (operandList.size()>firstIdx+1){
			return false;
		}
		for (i=0;i<firstExp.length();i++){
	
			if (postKey){
				if (firstExp.at(i) == '_'){
					if (currentOperand==operandList[firstIdx]){
						return true;
					}
					currentOperand ="";
				}
				else {
					currentOperand += firstExp.at(i);
				}
			}
			else if (firstExp.at(i) == '@'){
				postKey = true;
			
			}
		}
		return false;
	}
	else if (lastOp == '>'){
		Number a = solvePostfix(firstExp);
		Number b = solvePostfix(secondExp);
		if (a.type == 0 || b.type == 0){
			return false;
		}
		if (a > b){
			return true;
		}
		else {
			return false;
		}
	}
	else if (lastOp == '<'){
		Number a = solvePostfix(firstExp);
		Number b = solvePostfix(secondExp);
		if (a.type == 0 || b.type == 0){
			return false;
		}
		if (a < b){
			return true;
		}
		else {
			return false;
		}
	}
	
	
	return false;
}
std::string constraintify(std::string input){
	int i;
	std::string tempStr = "..................";
	char dncc{-94};
	std::string dnc = "";
	dnc += dncc;
	std::cout << "contraintify: "<< input << "\n";
	for (i=0;i<input.length();i++){
		tempStr += input.at(i);
		tempStr.replace(0,1,"");
		if (tempStr == " does not contain "){
			input.replace(i-17,18,dnc);
			i -= 17;
			tempStr = "..................";
		}
	}
	tempStr = "..........";
	char dcc{-87};
	std::string dc = "";
	dc += dcc;
	std::cout << "contraintify: "<< input << "\n";
	for (i=0;i<input.length();i++){
		tempStr += input.at(i);
		tempStr.replace(0,1,"");
		if (tempStr == " contains "){
			input.replace(i-9,10,dc);
			i -= 9;
			tempStr = "..........";
		}
	}
	std::cout << "contraintified: " << input << "\n";
	return input;
}