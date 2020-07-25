
std::vector<std::string> makeAnswer(std::string input){
	char infixexpr[input.length() + 1]; 
    strcpy(infixexpr, input.c_str()); 

	infixexpr[input.length()] = '\0';
	std::vector<std::string> postfixed = postfixifyVector(infixexpr,true);
	//std::cout << postfixed;
	return postfixed;
	//return makeTree(postfixed)[0];
}

void makeAnswers(std::string fileName){
	std::vector<std::vector<std::string>> rawRules;
	
	rapidcsv::Document doc("cpp/rules/"+fileName, rapidcsv::LabelParams(-1, -1));
	
	int nRows = doc.GetRowCount();
	int i; int ii;
	
	std::cout << "Rows: " << nRows << "\n";
	
	for (i=0;i<nRows;i++){
		std::vector<std::string> rawRule = doc.GetRow<std::string>(i);
		if (rawRule[0] == "Rule"){
			if (i>0){
				//jsonmessage += "rules.push(rule);";
			}
			//jsonmessage += "rule = {name:\""+rawRule[1]+"\",explanation:\""+rawRule[2]+"\",correct:[],incorrect:[],examples:[]}; rule['id'] = rules.length; \n";
			
		}
		else if (rawRule[1] == "e"){
			//jsonmessage += "rule.examples.push(\""+rawRule[0]+"\");\n";
		}
		else if (rawRule[1] == "c"){
			rawRules.push_back(rawRule);
			//jsonmessage += "rule.correct.push(\""+rawRule[0]+"\");\n";
		}
		else if (rawRule[1] == "i"){
			rawRules.push_back(rawRule);
			//jsonmessage += "rule.incorrect.push(\""+rawRule[0]+"\");\n";
		}
		
	}
	//jsonmessage += "rules.push(rule);\n";
	
	
	std::vector<std::string> fullPost;
	std::string key;
	std::string val1;
	std::string out;
	for (i=0;i<rawRules.size();i++){
		std::vector<std::string> rule;

		fullPost = makeAnswer(rawRules[i][0]);
		key = fullPost[0];
		val1 = fullPost[1];
		rule = {val1,rawRules[i][1],rawRules[i][2]};
			

		//TODO: add more constraint options
		
		if (rawRules[i].size()>3){
			std::string constraint = constraintify(rawRules[i][4]);
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
}