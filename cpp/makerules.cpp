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
		if (rawRule[0] != "Rule"){
			rawRules.push_back(rawRule);
			std::cout << rawRule[0] << "\n";
		}
		else {
			std::cout << "skipped: " << rawRule[0] << "\n";
		}
		
	}
	
	
	std::vector<std::string> fullPost;
	std::string key;
	std::string val1;
	std::string out;
	for (i=0;i<rawRules.size();i++){
		if (rawRules[i][1].at(0)=='='){
			fullPost = makeRule(rawRules[i][0]);
			key = fullPost[0];
			val1 = fullPost[1];
			if (rules.find(key) != rules.end()){
				rules[key].push_back({val1,rawRules[i][1],rawRules[i][2]});
			}
			else {
				rules[key] = {{val1,rawRules[i][1],rawRules[i][2]}};
			}
			
		}
		else {
			fullPost = makeRule(rawRules[i][0]);
			key = fullPost[0];
			val1 = fullPost[1];
			fullPost = makeRule(rawRules[i][1]);
			out = fullPost[0] + '@' + fullPost[1];
			if (rules.find(key) != rules.end()){
				rules[key].push_back({val1,out,rawRules[i][2]});
			}
			else {
				rules[key] = {{val1,out,rawRules[i][2]}};
			}
			// TODO: add possibility of appending to existing key, and adding all constraints
		}
		
	}
}