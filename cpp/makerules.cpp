std::vector<std::string> makeRule(std::string input){
	char infixexpr[input.length() + 1]; 
    strcpy(infixexpr, input.c_str()); 

	infixexpr[input.length()] = '\0';
	std::vector<std::string> postfixed = postfixifyVector(infixexpr);
	//std::cout << postfixed;
	return postfixed;
	//return makeTree(postfixed)[0];
}

flat_hash_map<std::string,std::vector<std::vector<std::string>>> makeRules(){
	flat_hash_map<std::string,std::vector<std::vector<std::string>>> finalRules;
	std::vector<std::vector<std::string>> rawRules;
	
	rapidcsv::Document doc("cpp/rules/main.csv", rapidcsv::LabelParams(-1, -1));
	
	int nRows = doc.GetRowCount();
	int i; int ii;
	
	std::cout << "Rows: " << nRows << "\n";
	
	for (i=0;i<nRows;i++){
		std::vector<std::string> rawRule = doc.GetRow<std::string>(i);
		rawRules.push_back(rawRule);
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
			if (finalRules.find(key) != finalRules.end()){
				finalRules[key].push_back({val1,rawRules[i][1],rawRules[i][2]});
			}
			else {
				finalRules[key] = {{val1,rawRules[i][1],rawRules[i][2]}};
			}
			
		}
		else {
			fullPost = makeRule(rawRules[i][0]);
			key = fullPost[0];
			val1 = fullPost[1];
			fullPost = makeRule(rawRules[i][1]);
			out = fullPost[0] + '@' + fullPost[1];
			if (finalRules.find(key) != finalRules.end()){
				finalRules[key].push_back({val1,out,rawRules[i][2]});
			}
			else {
				finalRules[key] = {{val1,out,rawRules[i][2]}};
			}
			// TODO: add possibility of appending to existing key, and adding all constraints
		}
		
	}
	return finalRules;
}