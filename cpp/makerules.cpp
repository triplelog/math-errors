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
		for (i=0;i<firstPart.length();i++){
	
			if (postKey){
				if (firstPart.at(i) == '_'){
					if (currentOperand==operandList[firstIdx]){
						return false;
					}
					currentOperand ="";
				}
				else {
					currentOperand += firstPart.at(i);
				}
			}
			else if (firstPart.at(i) == '@'){
				postKey = true;
			
			}
		}
		std::cout << "was true" << "\n";
		return true;
	}
	if (lastOp == -87){ //contains--secondExp must be single operand
		currentOperand = "";
		postKey = false;
		for (i=0;i<firstPart.length();i++){
	
			if (postKey){
				if (firstPart.at(i) == '_'){
					if (currentOperand==operandList[firstIdx]){
						return true;
					}
					currentOperand ="";
				}
				else {
					currentOperand += firstPart.at(i);
				}
			}
			else if (firstPart.at(i) == '@'){
				postKey = true;
			
			}
		}
		return false;
	}
	
	
	return false;
}
std::string constraintify(std::string input){
	int i;
	std::string tempStr = "................";
	char dncc{-94};
	std::string dnc = "";
	dnc += dncc;
	std::cout << input << "\n";
	for (i=0;i<input.length();i++){
		tempStr += input.at(i);
		tempStr.replace(0,1,"");
		if (tempStr == "does not contain"){
			input.replace(i-15,16,dnc);
			i -= 15;
			tempStr = "................";
		}
	}
	std::cout << input << "\n";
	return input;
}

std::vector<std::string> makeRule(std::string input){
	char infixexpr[input.length() + 1]; 
    strcpy(infixexpr, input.c_str()); 

	infixexpr[input.length()] = '\0';
	std::vector<std::string> postfixed = postfixifyVector(infixexpr);
	//std::cout << postfixed;
	return postfixed;
	//return makeTree(postfixed)[0];
}

void makeRules(std::string fileName){
	std::vector<std::vector<std::string>> rawRules;
	
	rapidcsv::Document doc("cpp/rules/"+fileName, rapidcsv::LabelParams(-1, -1));
	
	int nRows = doc.GetRowCount();
	int i; int ii;
	
	std::cout << "Rows: " << nRows << "\n";
	
	for (i=0;i<nRows;i++){
		std::vector<std::string> rawRule = doc.GetRow<std::string>(i);
		if (rawRule[0] == "Rule"){
			if (i>0){
				jsonmessage += "rules.push(rule);";
			}
			jsonmessage += "rule = {name:\""+rawRule[1]+"\",explanation:\""+rawRule[2]+"\",correct:[],incorrect:[],examples:[]}; rule['id'] = rules.length; \n";
			
		}
		else if (rawRule[2] == "e"){
			jsonmessage += "rule.examples.push(\""+rawRule[0]+"\");\n";
		}
		else if (rawRule[2] == "c"){
			rawRules.push_back(rawRule);
			jsonmessage += "rule.correct.push(\""+rawRule[0]+"\");\n";
		}
		else if (rawRule[2] == "i"){
			rawRules.push_back(rawRule);
			jsonmessage += "rule.incorrect.push(\""+rawRule[0]+"\");\n";
		}
		
	}
	jsonmessage += "rules.push(rule);\n";
	
	
	std::vector<std::string> fullPost;
	std::string key;
	std::string val1;
	std::string out;
	for (i=0;i<rawRules.size();i++){
		std::vector<std::string> rule;
		if (rawRules[i][1].at(0)=='='){
			fullPost = makeRule(rawRules[i][0]);
			key = fullPost[0];
			val1 = fullPost[1];
			rule = {val1,rawRules[i][1],rawRules[i][2]};
			
		}
		else {
			fullPost = makeRule(rawRules[i][0]);
			key = fullPost[0];
			val1 = fullPost[1];
			fullPost = makeRule(rawRules[i][1]);
			out = fullPost[0] + '@' + fullPost[1];
			rule = {val1,out,rawRules[i][2]};
			
		}
		//TODO: add more constraint options
		
		if (rawRules[i].size()>4){
			std::string constraint = constraintify(rawRules[i][4]);
			std::string postfixed = postfixify(constraint);
			std::cout <<" postfixed " << postfixed << "\n";
			rule.push_back(postfixed);
		}
		
		
		if (rules.find(key) != rules.end()){
			rules[key].push_back(rule);
		}
		else {
			rules[key] = {rule};
		}
		
		
		
	}
}