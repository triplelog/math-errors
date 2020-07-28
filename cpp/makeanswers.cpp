
std::vector<std::string> makeAnswer(std::string input){
	char infixexpr[input.length() + 1]; 
    strcpy(infixexpr, input.c_str()); 

	infixexpr[input.length()] = '\0';
	std::vector<std::string> postfixed = postfixifyVector(infixexpr,true);
	//std::cout << postfixed;
	return postfixed;
	//return makeTree(postfixed)[0];
}

std::vector<std::string> makeQuestion(std::string fileName){
	std::vector<std::vector<std::string>> rawRules;
	std::vector<std::string> question = {"",""};
	
	rapidcsv::Document doc("cpp/rules/"+fileName, rapidcsv::LabelParams(-1, -1));
	
	int nRows = doc.GetRowCount();
	int i; int ii;
	
	std::cout << "Rows: " << nRows << "\n";
	if (nRows<6){
		return question;
	}
	std::string qText = "";
	std::string q = "";
	
	std::vector<std::string> qTextRow = doc.GetRow<std::string>(2);
	
	if (qTextRow.size() > 0){
		qText = qTextRow[0];
		std::cout << "question: " << qText << "\n\n";
		question[0] = qText;
	}
	
	
	flat_hash_map<char,std::string> varMap;
	for (i=6;i<nRows;i++){
		std::vector<std::string> rawRule = doc.GetRow<std::string>(i);
		if (rawRule.size() < 3 || rawRule[0] == "t"){
			continue;			
		}
		else if (rawRule[0] != "a" && rawRule[0] != "q"){
			continue;			
		}
		else if (rawRule[0] == "q" && rawRule[1].length == 1){
			std::string range = "";
			char var = rawRule[1].at(0);
			for (ii=3;ii<rawRule.size();ii++){
				if (ii >3){
					range += ",";
				}
				range += rawRule[ii];
			}
			std::cout << "range: "<< range << "\n";		
			varMap[var]=makeInt(range);
		}
		else if (rawRule[2] == "e"){
			//jsonmessage += "rule.examples.push(\""+rawRule[0]+"\");\n";
		}
		else if (rawRule[2] == "c"){
			rawRules.push_back(rawRule);
			//jsonmessage += "rule.correct.push(\""+rawRule[0]+"\");\n";
		}
		else if (rawRule[2] == "i"){
			rawRules.push_back(rawRule);
			//jsonmessage += "rule.incorrect.push(\""+rawRule[0]+"\");\n";
		}
		
	}
	
	std::vector<std::string> qRow = doc.GetRow<std::string>(3);
	if (qRow.size() > 0){
		q = postfixify(qRow[0]);
		bool pastKey = false;
		std::string newQ = "";
		std::string currentOperand = "";
		for (ii=0;ii<q.length();ii++){

			if (pastKey){
				if (q.at(ii) == '_'){
					if (currentOperand.length()==1 && currentOperand.at(0) <='Z' && currentOperand.at(0) >= 'A'){
						if (varMap.find(currentOperand.at(0)) != varMap.end()){
							newQ += varMap[currentOperand.at(0)] + '_';
						}
						else {
							newQ += currentOperand + '_';
						}
						
					}
					else {
						
					}
					currentOperand = "";
				}
				else {
					currentOperand += q.at(ii);
				}
			}
			else {
				if (q.at(ii) == '@'){
					pastKey = true;
				}
				newQ += q.at(ii);
			}
				
		}
		std::cout << "question for computer: " << newQ << "\n\n";
		question[1] = newQ;
		
	}
	//jsonmessage += "rules.push(rule);\n";
	
	
	std::vector<std::string> fullPost;
	std::string key;
	std::string val1;
	std::string out;
	for (i=0;i<rawRules.size();i++){
		std::vector<std::string> rule;

		fullPost = makeAnswer(rawRules[i][1]);
		key = fullPost[0];
		val1 = fullPost[1];
		rule = {val1,rawRules[i][2],rawRules[i][3]};
			

		//TODO: add more constraint options
		
		if (rawRules[i].size()>4){
			std::string constraint = constraintify(rawRules[i][5]);
			std::string postfixed = postfixify(constraint);
			std::cout <<" postfixed " << postfixed << "\n";
			rule.push_back(postfixed);
		}
		
		
		if (rules.find(key) != rules.end()){
			answerConstraints[key].push_back(rule);
		}
		else {
			answerConstraints[key] = {rule};
		}
		
		
		
	}
	return question;
}