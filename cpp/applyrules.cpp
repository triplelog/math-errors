std::vector<Step> applyRulesVectorOnePart(std::string onePart,std::vector<int> oneIndex, std::string userFullString, bool isCorrect) {
	auto a1 = std::chrono::high_resolution_clock::now();
	int iii; int iiii;

	auto a3 = std::chrono::high_resolution_clock::now();
	std::vector<Step> allStrings;
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

	if (rules.find(key) != rules.end()){
		//std::cout << "Key Match: " << key << " and " << rules[key][0][0] << "\n";
		//std::cout << "userFullString @ keyMatch: "<< userFullString << "\n";
		int ruleIdx;
		for (ruleIdx=0;ruleIdx<rules[key].size();ruleIdx++){
			//std::cout << "Key sub-Match: " << key << " and " << rules[key][ruleIdx].out << "\n";
			
			Rule rule = rules[key][ruleIdx];
			
			
			if (rule.type != "c" && isCorrect){continue;}
			else if (rule.type != "e" && rule.type != "i" && !isCorrect){continue;}
			//else if (!isCorrect){continue;}
			
			
			
			std::string currentOperand = "";
			flat_hash_map<char,std::string> partMap;
			std::vector<std::string> userOperands;
			std::vector<std::string> ruleOperands;
			newPostfix = "";
			for (iii=0;iii<rule.operands.length();iii++){
				if (rule.operands.at(iii) == '_'){
					ruleOperands.push_back(currentOperand);
					currentOperand = "";
				}
				else {
					currentOperand += rule.operands.at(iii);
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

			bool hasPar = false;

			int openPar = 0;
			std::string insidePostfix = "";
			bool pastInsideKey = false;
			bool isArithmetic = true;
			//std::cout << userString << " and " << rule.operands << " and " << key << " and " << rule.out << " was userString\n";
			for (iii=0;iii<rule.out.length();iii++){
				//std::cout << iii << "\n";
				if (openPar > 0){
					hasPar = true;
					if (pastInsideKey){
						if (rule.out.at(iii) == ')' && openPar == 1){
							int bi;
							isArithmetic = true;
							//std::cout << "ipf: " << insidePostfix << "\n";
							for (bi=0;bi<insidePostfix.length();bi++){
								if (insidePostfix.at(bi) == -89 && bi+1<insidePostfix.length() && insidePostfix.at(bi+1) == '@'){
									
									currentOperand = substitute(insidePostfix);
									if (currentOperand != "("+insidePostfix+")" && currentOperand.at(4) == -95){
										std::cout << "substitute: " << insidePostfix << "\n";
										std::cout << "substituted: " << currentOperand << "\n";
									}
									
									isArithmetic = false;
									break;
								}
							}
							openPar--;
							pastInsideKey = false;
							if (!isArithmetic){continue;}
							Number opResult = solvePostfix(insidePostfix);

							if (opResult.type == 0){
								currentOperand = "("+insidePostfix+")";
							}
							else if (opResult.type == 1){
								currentOperand = "(#@"+opResult.top+"_)";
							}
							else if (opResult.type == -1){
								currentOperand = "(#@-"+opResult.top+"_)";
							}
							else {
								currentOperand = "("+insidePostfix+")";
							}
							
							
						}
						else if (rule.out.at(iii) == '_'){
							if (currentOperand.length()==1 && currentOperand.at(0) <='Z' && currentOperand.at(0) >= 'A'){
								if (partMap.find(currentOperand.at(0)) != partMap.end()){
									insidePostfix += partMap[currentOperand.at(0)] + '_';
								}
								else {
									insidePostfix += currentOperand + '_';
								}
								
							}
							else {
								insidePostfix += currentOperand + '_';
								
							}
							currentOperand = "";
						}
						else if (rule.out.at(iii) == ')') {
							openPar--;
							currentOperand += rule.out.at(iii);
						}
						else {
							currentOperand += rule.out.at(iii);
						}
					}
					else {
						if (rule.out.at(iii) == '@'){
							pastInsideKey = true;
							currentOperand = "";
						}
						insidePostfix += rule.out.at(iii);
					}
				}
				else {
					if (pastKey){
						if (rule.out.at(iii) == '('){
							openPar = 1;
							currentOperand = "";
							insidePostfix = "";
							pastInsideKey = false;
						}
						else if (rule.out.at(iii) == '_'){
							if (currentOperand.length()==1 && currentOperand.at(0) <='Z' && currentOperand.at(0) >= 'A'){
								if (partMap.find(currentOperand.at(0)) != partMap.end()){
									newPostfix += partMap[currentOperand.at(0)] + '_';
								}
								else {
									newPostfix += currentOperand + '_';
								}
								
							}
							else {
								newPostfix += currentOperand + '_';
							}
							currentOperand = "";
						}
						else {
							currentOperand += rule.out.at(iii);
						}
					}
					else {
						if (rule.out.at(iii) == '@'){
							pastKey = true;
						}
						newPostfix += rule.out.at(iii);
					}
				}
					
			}

			
			if (hasPar && newPostfix.length() >0){
				//std::cout << newPostfix << " was newPostfix\n";
				newPostfix = removeParOne(newPostfix);
				//std::cout << newPostfix << " was newPostfix after removal\n";
				//newPostfix = removeBracketsOne(newPostfix);
			}
			if (newPostfix == userString){
				newPostfix = "";
			}
			//std::cout << newPostfix << " was npf\n";
			
			if (newPostfix.length()>0){
				//Constraints go here
				for (iiii=0;iiii<rule.constraints.size();iiii++){
					pastKey = false;
					std::string constraintFix = "";
					currentOperand = "";
					
					for (iii=0;iii<rule.constraints[iiii].length();iii++){
						if (pastKey){
							if (rule.constraints[iiii].at(iii) == '_'){
								if (currentOperand.length()==1 && currentOperand.at(0) <='Z' && currentOperand.at(0) >= 'A'){
									if (partMap.find(currentOperand.at(0)) != partMap.end()){
										constraintFix += partMap[currentOperand.at(0)] + '_';
									}
									else {
										constraintFix += currentOperand + '_';
									}
								}
								else {
									constraintFix += currentOperand + '_';
								}
								currentOperand = "";
							}
							else {
								currentOperand += rule.constraints[iiii].at(iii);
							}
						}
						else {
							if (rule.constraints[iiii].at(iii) == '@'){
								pastKey = true;
							}
							constraintFix += rule.constraints[iiii].at(iii);
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

					Step step;
					step.next = tempTemp;
					step.rule = rule.id;
					
					allStrings.push_back(step);
				}
				
				
			}
		}
		
	}


	
	auto a4 = std::chrono::high_resolution_clock::now();
	//duration1 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	//duration2 += std::chrono::duration_cast<std::chrono::microseconds>( a3 - a2 ).count();
	//duration3 += std::chrono::duration_cast<std::chrono::microseconds>( a4 - a3 ).count();

	return allStrings;
	
}
