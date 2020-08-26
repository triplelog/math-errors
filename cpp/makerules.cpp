#include "constraints.cpp"

std::vector<std::string> makeRule(std::string input){
	char infixexpr[input.length() + 1]; 
    strcpy(infixexpr, input.c_str()); 

	infixexpr[input.length()] = '\0';
	std::vector<std::string> postfixed = postfixifyVector(infixexpr,true);
	//std::cout << postfixed;
	return postfixed;
	//return makeTree(postfixed)[0];
}

void makeRules(std::string fileName){
	std::vector<std::vector<std::string>> rawRules;
	
	rapidcsv::Document doc("cpp/"+fileName, rapidcsv::LabelParams(-1, -1));
	
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
		else if (rawRule[2] == "x"){
			jsonmessage += "rule.examples.push(\""+rawRule[0]+"\");\n";
		}
		else if (rawRule[2] == "c"){
			rawRules.push_back(rawRule);
			jsonmessage += "rule.correct.push(\""+rawRule[0]+"\");\n";
		}
		else if (rawRule[2] == "i" || rawRule[2] == "e"){
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
		Rule rule;
		
		fullPost = makeRule(rawRules[i][0]);
		key = fullPost[0];
		val1 = fullPost[1];
		rule.key = key;
		//std::cout << "key: "<< key << "\n";
		//std::cout << "val1: "<< val1 << "\n";
		fullPost = makeRule(rawRules[i][1]);
		//std::cout << "raw: "<< rawRules[i][1] << "\n";
		out = fullPost[0] + '@' + fullPost[1];
		//std::cout << "out: "<< out << "\n";
		rule.operands = val1;
		rule.out = out;
		
		if (rawRules[i][2] == "e" || rawRules[i][2] == "i"){
			rule.type = "e";
		}
		else {
			rule.type = rawRules[i][2];
		}
		if (rawRules[i].size()>3){
			rule.explanation = rawRules[i][3];
		}
		

		//TODO: add more constraint options
		
		if (rawRules[i].size()>4){
			for (ii=4;ii<rawRules[i].size();ii++){
				std::string constraint = constraintify(rawRules[i][ii]);
				std::string postfixed = postfixify(constraint);
				//std::cout <<" constraint postfixed " << postfixed << "\n";
				rule.constraints.push_back(postfixed);
			}
		}
		
		rule.id = ridx;
		if (rules.find(key) != rules.end()){
			rules[key].push_back(rule);
		}
		else {
			rules[key] = {rule};
		}
		
		
		ruleIndex[ridx]=rule;
		ridx++;
		
		
		
	}
}

void makeRulesNew(std::vector<std::string> rows){
	std::vector<std::vector<std::string>> rawRules;
	int i; int ii;
	
	int nRows = rows.size();
	
	
	std::cout << "RowsNew: " << nRows << "\n";
	
	std::vector<std::string> currentRawRule;
	currentRawRule.resize(0);
	bool inRule = false;
	for (i=0;i<nRows;i++){
		std::string rawRule = rows[i];
		if (rawRule == "::: rule"){
			if (inRule){
				inRule = false;
				rawRules.push_back(currentRawRule);
				currentRawRule.resize(0);
			}
			currentRawRule.resize(4);
			currentRawRule[2] = "c";
			currentRawRule[3] = "";
			inRule = true;
		}
		else if (rawRule == "::: error"){
			if (inRule){
				inRule = false;
				rawRules.push_back(currentRawRule);
				currentRawRule.resize(0);
			}
			currentRawRule.resize(4);
			currentRawRule[2] = "i";
			currentRawRule[3] = "";
			inRule = true;
		}
		else if (rawRule.substr(0,11) == "::: example"){
			if (inRule){
				inRule = false;
				rawRules.push_back(currentRawRule);
				currentRawRule.resize(0);
			}
			for (ii=i+1;ii<nRows;ii++){
				if (rows[ii].substr(0,3) == ":::"){
					break;
				}
				if (rows[ii] == ""){continue;}
				currentRawRule.resize(4);
				currentRawRule[2] = "x";
				currentRawRule[3] = "";
				currentRawRule[0] = rows[ii];
				currentRawRule[1] = rows[ii];
				rawRules.push_back(currentRawRule);
				currentRawRule.resize(0);
			}
			i = ii;
			inRule = false;
			
		}
		else if (rawRule.length() == 0 || rawRule.substr(0,3) == ":::"){
			if (inRule){
				inRule = false;
				rawRules.push_back(currentRawRule);
				currentRawRule.resize(0);
			}
		}
		else if (rawRule.substr(0,2) == "ee"){
			if (inRule){
				inRule = false;
				rawRules.push_back(currentRawRule);
				currentRawRule.resize(0);
			}
		}
		else if (rawRule.substr(0,4) == "in: " || rawRule.substr(0,4) == "IN: " || rawRule.substr(0,4) == "In: "){
			currentRawRule[0] = rawRule.substr(4,rawRule.length()-4);
		}
		else if (rawRule.substr(0,5) == "out: " || rawRule.substr(0,5) == "OUT: " || rawRule.substr(0,5) == "Out: "){
			currentRawRule[1] = rawRule.substr(5,rawRule.length()-5);
		}
		else if (inRule){
			currentRawRule.push_back(rawRule);
		}
	}
	if (inRule){
		inRule = false;
		rawRules.push_back(currentRawRule);
		currentRawRule.resize(0);
	}
	//jsonmessage += "rules.push(rule);\n";
	
	
	std::vector<std::string> fullPost;
	std::string key;
	std::string val1;
	std::string out;
	for (i=0;i<rawRules.size();i++){
		Rule rule;
		fullPost = makeRule(rawRules[i][0]);
		key = fullPost[0];
		val1 = fullPost[1];
		rule.key = key;
		fullPost = makeRule(rawRules[i][1]);
		out = fullPost[0] + '@' + fullPost[1];
		rule.operands = val1;
		rule.out = out;
		
		if (rawRules[i][2] == "e" || rawRules[i][2] == "i"){
			rule.type = "e";
		}
		else {
			rule.type = rawRules[i][2];
		}
		if (rawRules[i].size()>3){
			rule.explanation = rawRules[i][3];
		}
		

		//TODO: add more constraint options
		
		if (rawRules[i].size()>4){
			for (ii=4;ii<rawRules[i].size();ii++){
				std::string constraint = constraintify(rawRules[i][ii]);
				std::string postfixed = postfixify(constraint);
				//std::cout <<" constraint postfixed " << postfixed << "\n";
				rule.constraints.push_back(postfixed);
			}
		}
		
		rule.id = ridx;
		if (rules.find(key) != rules.end()){
			rules[key].push_back(rule);
		}
		else {
			rules[key] = {rule};
		}
		
		
		ruleIndex[ridx]=rule;
		ridx++;
		
		
		
	}
}