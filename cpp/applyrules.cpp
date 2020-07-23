std::vector<std::string> applyRulesVectorOnePart(std::string onePart,std::vector<int> oneIndex, std::string userFullString, bool isCorrect) {
	auto a1 = std::chrono::high_resolution_clock::now();
	int iii; int iiii;

	auto a3 = std::chrono::high_resolution_clock::now();
	std::vector<std::vector<std::string>> allOptions;
	std::vector<std::string> allStrings;
	std::string newPostfix = "";
	bool midBracket = false;
	bool foundAt = false;

	std::string userString = onePart;
	std::string key = "";
	
	newPostfix = "";
	
	int startAt =0;
	
	for (iiii=0;iiii<userString.length();iiii++){
		if (userString.at(iiii) == '@'){
			startAt = iiii+1;
			break;
		}
		else{
			key += userString.at(iiii);
		}
	}
	std::vector<std::string> newStrings;
	if (rules.find(key) != rules.end()){
		//std::cout << "Key Match: " << key << " and " << rules[key][0][0] << "\n";
		//std::cout << "userFullString @ keyMatch: "<< userFullString << "\n";
		int ruleIdx;
		for (ruleIdx=0;ruleIdx<rules[key].size();ruleIdx++){
			//std::cout << "Key sub-Match: " << key << " and " << rules[key][ruleIdx][0] << "\n";
			
			std::vector<std::string> rule = rules[key][ruleIdx];
			
			
			if (rule[2] != "c" && isCorrect){continue;}
			
			
			
			std::string currentOperand = "";
			flat_hash_map<char,std::string> partMap;
			std::vector<std::string> userOperands;
			std::vector<std::string> ruleOperands;
			newPostfix = "";
			for (iii=0;iii<rule[0].length();iii++){
				if (rule[0].at(iii) == '_'){
					ruleOperands.push_back(currentOperand);
					currentOperand = "";
				}
				else {
					currentOperand += rule[0].at(iii);
				}
			}
			currentOperand = "";
			midBracket = false;
			for (iii=startAt;iii<userString.length();iii++){
				if (userString.at(iii) == '_' && !midBracket){
					userOperands.push_back(currentOperand);
					currentOperand = "";
				}
				else if (userString.at(iii) == '{') {
					currentOperand += userString.at(iii);
					midBracket = true;
				}
				else if (userString.at(iii) == '}') {
					currentOperand += userString.at(iii);
					midBracket = false;
				}
				else {
					currentOperand += userString.at(iii);
				}
			}
			bool ignoreThis = false;
			if (ruleOperands.size() != userOperands.size()){
				//TODO: move to next rule
				ignoreThis = true;
			}
			for (iii=0;iii<ruleOperands.size();iii++){
				if (ruleOperands[iii].length()==1){
					if (ruleOperands[iii].at(0) <= 'Z' && ruleOperands[iii].at(0) >= 'A'){
						if (partMap.find(ruleOperands[iii].at(0)) != partMap.end()){
							if (partMap[ruleOperands[iii].at(0)] != userOperands[iii]){
								ignoreThis = true;
								break;
							}
						}
						partMap[ruleOperands[iii].at(0)] = userOperands[iii];
					}
					else if (ruleOperands[iii] != userOperands[iii]){
						//TODO: skip this rule
						ignoreThis = true;
						break;
					}
				}
				else if (ruleOperands[iii] != userOperands[iii]){
					//TODO: skip this rule
					ignoreThis = true;
					break;
				}
			}
			
			
			
		
			newPostfix = "";
			if (ignoreThis){
				continue;
			}
			bool pastKey = false;
			/*
			if (rule[1].at(0)=='='){
				
				std::string inside = rule[1];
				inside.replace(inside.length()-1,1,"");
				inside.replace(0,2,"");
				
				std::string opResult = solvePostfix(inside,partMap);
				
				if (opResult == "false"){
					newPostfix = "";
					continue;
				}
				
				newPostfix = "#@"+opResult+"_";
				
				
			}*/
			if (2 ==2) {
				bool openBrackets = false;
				std::string insidePostfix = "";
				bool pastInsideKey = false;
				bool hasBrackets = false;
				std::cout << "the rule: "<< rule[1] << "\n";
				for (iii=0;iii<rule[1].length();iii++){
					if (openBrackets){
						hasBrackets = true;
						if (pastInsideKey){
							if (rule[1].at(iii) == '}'){
								std::cout << "insidePF: "<< insidePostfix << "\n";
								std::string opResult = solvePostfix(insidePostfix);
								std::cout << "opR: "<< opResult << "\n";
								if (opResult == "false"){
									currentOperand = "{"+insidePostfix+"}";
								}
								else {
									currentOperand = "{#@"+opResult+"_}";
								}
								openBrackets = false;
								pastInsideKey = false;
							}
							else if (rule[1].at(iii) == '_'){
								std::cout << "co: "<< currentOperand << "\n";
								if (currentOperand.length()==1 && currentOperand.at(0) <='Z' && currentOperand.at(0) >= 'A'){
									insidePostfix += partMap[currentOperand.at(0)] + '_';
									std::cout << "ipf: "<< insidePostfix << "\n";
								}
								else {
									insidePostfix += currentOperand + '_';
									std::cout << "us: "<< userString << "\n";
								}
								currentOperand = "";
							}
							else {
								currentOperand += rule[1].at(iii);
							}
						}
						else {
							if (rule[1].at(iii) == '@'){
								pastInsideKey = true;
								currentOperand = "";
							}
							insidePostfix += rule[1].at(iii);
						}
					}
					else {
						if (pastKey){
							if (rule[1].at(iii) == '{'){
								openBrackets = true;
								currentOperand = "";
								insidePostfix = "";
								pastInsideKey = false;
							}
							else if (rule[1].at(iii) == '_'){
								if (currentOperand.length()==1 && currentOperand.at(0) <='Z' && currentOperand.at(0) >= 'A'){
									newPostfix += partMap[currentOperand.at(0)] + '_';
								}
								else {
									newPostfix += currentOperand + '_';
								}
								currentOperand = "";
							}
							else {
								currentOperand += rule[1].at(iii);
							}
						}
						else {
							if (rule[1].at(iii) == '@'){
								pastKey = true;
							}
							newPostfix += rule[1].at(iii);
						}
					}
						
				}
				std::cout << "post rule: "<< newPostfix << "\n";
				if (hasBrackets){
					newPostfix = removeBracketsOne(newPostfix);
				}
				
				if (newPostfix.length()>0){
					//Constraints go here
					for (iiii=4;iiii<rule.size();iiii++){
						pastKey = false;
						std::string constraintFix = "";
						currentOperand = "";
						
						for (iii=0;iii<rule[iiii].length();iii++){
							if (pastKey){
								if (rule[iiii].at(iii) == '_'){
									if (currentOperand.length()==1 && currentOperand.at(0) <='Z' && currentOperand.at(0) >= 'A'){
										constraintFix += partMap[currentOperand.at(0)] + '_';
									}
									else {
										constraintFix += currentOperand + '_';
									}
									currentOperand = "";
								}
								else {
									currentOperand += rule[iiii].at(iii);
								}
							}
							else {
								if (rule[iiii].at(iii) == '@'){
									pastKey = true;
								}
								constraintFix += rule[iiii].at(iii);
							}
						}
						bool isAllowed = true;
						if (constraintMap.find(constraintFix) != constraintMap.end()){
							isAllowed = constraintMap[constraintFix];
						}
						else {
							isAllowed = solveConstraintFix(constraintFix);
							constraintMap[constraintFix]=isAllowed;
						}
						if (!isAllowed){
							newPostfix = "";
							break;
						}
					}
				}
			}
		
			if (newPostfix.length()>0){
				//std::cout << userFullString << " anand " << fullStr << " anand " << newPostfix << "\n\n";
				std::string newPostfixFirst = "";
				std::string newPostfixSecond = "";
				foundAt = false;
				for (iiii=0;iiii<newPostfix.length();iiii++){
					if (newPostfix.at(iiii) == '@' && !foundAt){
						foundAt = true;
					}
					else if (foundAt){
						newPostfixSecond += newPostfix.at(iiii);
					}
					else {
						newPostfixFirst += newPostfix.at(iiii);
					}
				}
				
				
				std::string tempTemp = userFullString;
				//std::cout << bottomTrees[ii][1] << " b " << bottomTrees[ii][2] << " c " << bottomTrees[ii][3] << " d " << bottomTrees[ii][4] << "\n";
				tempTemp.replace(oneIndex[2],oneIndex[3]+1,newPostfixSecond);
				//std::cout << "userFullString: "<< userFullString << "\n";
				tempTemp.replace(oneIndex[0],oneIndex[1],newPostfixFirst);
				//std::cout << bottomTrees[ii][1] << " bb " << bottomTrees[ii][2] << " c " << bottomTrees[ii][3] << " d " << bottomTrees[ii][4] << "\n";
				
				if (tempTemp != userFullString){
					tempTemp = removeBracketsOne(tempTemp);
					newStrings.push_back(tempTemp);
					allStrings.push_back(tempTemp);
					allStrings.push_back(key+","+std::to_string(ruleIdx));
				}
				
				
			}
		}
		
	}
	if (newStrings.size()>0){
		allOptions.push_back(newStrings);
		
	}

	
	auto a4 = std::chrono::high_resolution_clock::now();
	//duration1 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	//duration2 += std::chrono::duration_cast<std::chrono::microseconds>( a3 - a2 ).count();
	//duration3 += std::chrono::duration_cast<std::chrono::microseconds>( a4 - a3 ).count();

	return allStrings;
	
}
