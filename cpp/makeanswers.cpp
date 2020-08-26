std::string replaceVars(std::string q, flat_hash_map<char,std::string> varMap){
	bool pastKey = false;
	std::string newQ = "";
	std::string currentOperand = "";
	int ii;
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
					newQ += currentOperand + '_';
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
	return newQ;
}

std::vector<std::string> makeAnswer(std::string input){
	char infixexpr[input.length() + 1]; 
    strcpy(infixexpr, input.c_str()); 

	infixexpr[input.length()] = '\0';
	std::vector<std::string> postfixed = postfixifyVector(infixexpr,true);
	return postfixed;
	//return makeTree(postfixed)[0];
}
std::string solveInsideQuestion(std::string input) {
	int iii; bool openPar = false; bool pastInsideKey = false; bool pastKey = false;
	std::string currentOperand = "";
	std::string insidePostfix = "";
	bool hasPar = false;
	std::string newPostfix = "";
	for (iii=0;iii<input.length();iii++){
		if (openPar){
			hasPar = true;
			if (pastInsideKey){
				if (input.at(iii) == ')'){
					
					Number opResult = solvePostfix(insidePostfix);

					if (opResult.type == 0){
						currentOperand = "{"+insidePostfix+"}";
					}
					else {
						currentOperand = "{#@"+outputNumber(opResult)+"_}";
					}
					openPar = false;
					pastInsideKey = false;
					
				}
				else if (input.at(iii) == '_'){
					insidePostfix += currentOperand + '_';
					currentOperand = "";
				}
				else {
					currentOperand += input.at(iii);
				}
			}
			else {
				if (input.at(iii) == '@'){
					pastInsideKey = true;
					currentOperand = "";
				}
				insidePostfix += input.at(iii);
			}
		}
		else {
			if (pastKey){
				if (input.at(iii) == '('){
					openPar = true;
					currentOperand = "";
					insidePostfix = "";
					pastInsideKey = false;
				}
				else if (input.at(iii) == '_'){
					newPostfix += currentOperand + '_';
					currentOperand = "";
				}
				else {
					currentOperand += input.at(iii);
				}
			}
			else {
				if (input.at(iii) == '@'){
					pastKey = true;
				}
				newPostfix += input.at(iii);
			}
		}
			
	}
	return removeBracketsOne(newPostfix);
}
Question makeQuestion(std::string qRow, std::string qText,flat_hash_map<char,std::string> rangeMap){
	Question question;
	flat_hash_map<char,std::string> varMap;
	for (flat_hash_map<char,std::string>::iterator iter = rangeMap.begin(); iter != rangeMap.end(); ++iter){
		varMap[iter->first]=makeInt(iter->second);	
		//std::cout << "if: " << iter->first << " is: " << iter->second << " and " << makeInt(iter->second) << "\n";
	}
	//std::string q = postfixify(qRow);
	int i;
	//std::string newQ = replaceVars(q,varMap);
	std::vector<std::string> qv = postfixifyVector(qRow,true);
	//std::cout << "qv: " << qv[0] << " and " << qv[1] << "\n";
	std::string q = replaceVars(qv[0] + "@"+qv[1],varMap);
	//std::cout << "q: " << q << "\n";
	std::string newQ = solveInsideQuestion(q);
	//std::cout << "nq: " << newQ << "\n";
	std::cout << "question for computer: " << newQ << "\n\n";
	std::cout << "question for human: " << qText << "\n\n";
	question.comp = newQ;

	bool isMath = false;
	std::string newText = "";
	std::string currentMath = "";
	for (i=0;i<qText.length();i++){
		if (qText.at(i)== '$'){
			if (isMath){
				isMath = false;
				std::cout << "cm: " << currentMath << "\n";
				//std::string pf = postfixify(currentMath);
				std::vector<std::string> pv = postfixifyVector(currentMath,true);
				std::string pvv = replaceVars(pv[0] + "@"+pv[1],varMap);
				std::string pf = solveInsideQuestion(pvv);
				//std::cout << "pf: " << pf << "\n";
				//std::cout << "pvv: " << pvv << "\n";
				std::cout << "pf: " << pf << "\n";
				//pf = replaceVars(pf,varMap);
				//std::cout << "pf: " << pf << "\n";
				pf = latexOne(pf);
				std::cout << "pf: " << pf << "\n";
				
				newText += "$" + pf + "$";
				currentMath = "";
			}
			else {
				isMath = true;
				currentMath = "";
			}
		}
		else if (isMath) {
			currentMath += qText.at(i);
		}
		else {
			newText += qText.at(i);
		}
	}
	std::cout << "question for human: " << newText << "\n\n";
	question.text = newText;
	return question;
}

Question chooseQuestion(std::vector<RawQuestion> questions){
	Question q = makeQuestion(questions[0].qC, questions[0].qH, questions[0].rangeMap);
	q.rawRules = questions[0].rawRules;
	q.dewey = questions[0].dewey;
	std::vector<std::string> fullPost;
	std::string key;
	std::string val1;
	std::string out;
	answerConstraints.clear();
	int i; int ii;
	for (i=0;i<q.rawRules.size();i++){
		Rule rule;

		fullPost = makeAnswer(q.rawRules[i][1]);
		key = fullPost[0];
		val1 = fullPost[1];
		rule.key = key;
		rule.operands = val1;
		rule.type = q.rawRules[i][2];
		rule.explanation = q.rawRules[i][3];
		rule.id = -1;

		//TODO: add more constraint options
	
		if (q.rawRules[i].size()>4){
			for (ii=4;ii<q.rawRules[i].size();ii++){
				std::string constraint = constraintify(q.rawRules[i][ii]);
				std::string postfixed = postfixify(constraint);
				//std::cout <<" postfixed " << postfixed << "\n";
				rule.constraints.push_back(postfixed);
			}
		}
	
	
		if (rules.find(key) != rules.end()){
			answerConstraints[key].push_back(rule);
		}
		else {
			answerConstraints[key] = {rule};
		}
	
	
	
	}
	return q;
}




std::vector<RawQuestion> makeQuestions(Dewey qDewey, std::string fileName){
	
	std::vector<RawQuestion> questions;
	rapidcsv::Document doc("cpp/rules/"+fileName, rapidcsv::LabelParams(-1, -1));
	
	int nRows = doc.GetRowCount();
	
	int startIdx = 0;
	int idx = 0;
	int oldIdx = 0;
	auto a0 = std::chrono::high_resolution_clock::now();
	for (idx=0;idx<nRows;idx++){
		int i; int ii;
		bool makeThis = true;
		Dewey dewey;
		std::vector<std::string> firstRow = doc.GetRow<std::string>(startIdx);
		
		if (firstRow.size() < 1){
			continue;
		}
		std::string rawDewey = firstRow[0];
		std::string current = "";
		for (i=0;i<rawDewey.length();i++){
			if (rawDewey.at(i)=='.'){
				if (dewey.subject == "."){
					dewey.subject = current;
				}
				else if (dewey.topic == "."){
					dewey.topic = current;
				}
				else if (dewey.lesson == "."){
					dewey.lesson = current;
				}
				else {
					dewey.id = current;
				}
				current = "";
			}
			else {
				current += rawDewey.at(i);
			}
		}
		if (current.length()>0){
			if (dewey.subject == "."){
				dewey.subject = current;
			}
			else if (dewey.topic == "."){
				dewey.topic = current;
			}
			else if (dewey.lesson == "."){
				dewey.lesson = current;
			}
			else {
				dewey.id = current;
			}
		}

		if (dewey <minEq> qDewey){
		}
		else {
			makeThis = false;
		}
		std::vector<std::vector<std::string>> rawRules;

		
	
		if (nRows<startIdx+5){
			break;
		}
		oldIdx = startIdx;

		flat_hash_map<char,std::string> rangeMap;
		for (i=startIdx+5;i<nRows;i++){
			std::vector<std::string> rawRule = doc.GetRow<std::string>(i);
			if (rawRule.size() == 1 && rawRule[0] == ""){
				startIdx = i+1;
				break;
			}
			if (makeThis){
				if (rawRule.size() < 3 || rawRule[0] == "t"){
					continue;			
				}
				else if (rawRule[0] != "a" && rawRule[0] != "q"){
					continue;			
				}
				else if (rawRule[0] == "q" && rawRule[1].length() == 1){
					std::string range = "";
					char var = rawRule[1].at(0);
					for (ii=3;ii<rawRule.size();ii++){
						if (ii >3){
							range += ",";
						}
						range += rawRule[ii];
					}
					//std::cout << "range: "<< range << "\n";		
					//varMap[var]=makeInt(range);
					rangeMap[var]=range;
				}
				else if (rawRule[2] == "x"){
					//jsonmessage += "rule.examples.push(\""+rawRule[0]+"\");\n";
				}
				else if (rawRule[2] == "c"){
					
					if (rawRule.size()>5){
						std::vector<std::string> tempV;
						std::string currentCon = "";
						int openPar = 0;
						int iii;
						for (ii=0;ii<rawRule.size();ii++){
							if (ii<4){tempV.push_back(rawRule[ii]);}
							else {
								for (iii=0;iii<rawRule[ii].length();iii++){
									if (rawRule[ii].at(iii) == '['){
										openPar++;
									}
									else if (rawRule[ii].at(iii) == '{'){
										openPar++;
									}
									else if (rawRule[ii].at(iii) == '('){
										openPar++;
									}
									else if (rawRule[ii].at(iii) == '}'){
										openPar--;
									}
									else if (rawRule[ii].at(iii) == ')'){
										openPar--;
									}
									else if (rawRule[ii].at(iii) == ']'){
										openPar--;
									}
									
									if (rawRule[ii].at(iii) == ',' && openPar == 0){
										tempV.push_back(currentCon);
										currentCon = "";
									}
									else {
										currentCon += rawRule[ii].at(iii);
									}
								}
							}
							
						}
						if (currentCon.length()>0){
							tempV.push_back(currentCon);
						}
						rawRules.push_back(tempV);
					}
					else {
						rawRules.push_back(rawRule);
					}
					
					//jsonmessage += "rule.correct.push(\""+rawRule[0]+"\");\n";
				}
				else if (rawRule[2] == "i" || rawRule[2] == "e"){
					if (rawRule.size()>5){
						std::vector<std::string> tempV;
						std::string currentCon = "";
						int openPar = 0;
						int iii;
						for (ii=0;ii<rawRule.size();ii++){
							if (ii<4){tempV.push_back(rawRule[ii]);}
							else {
								for (iii=0;iii<rawRule[ii].length();iii++){
									if (rawRule[ii].at(iii) == '['){
										openPar++;
									}
									else if (rawRule[ii].at(iii) == '{'){
										openPar++;
									}
									else if (rawRule[ii].at(iii) == '('){
										openPar++;
									}
									else if (rawRule[ii].at(iii) == '}'){
										openPar--;
									}
									else if (rawRule[ii].at(iii) == ')'){
										openPar--;
									}
									else if (rawRule[ii].at(iii) == ']'){
										openPar--;
									}
									
									if (rawRule[ii].at(iii) == ',' && openPar == 0){
										tempV.push_back(currentCon);
										currentCon = "";
									}
									else {
										currentCon += rawRule[ii].at(iii);
									}
								}
								
								if (openPar > 0){
									currentCon += ",";
								}
								
								
							}
							
						}
						if (currentCon.length()>0){
							tempV.push_back(currentCon);
						}
						rawRules.push_back(tempV);
					}
					else {
						rawRules.push_back(rawRule);
					}
					//jsonmessage += "rule.incorrect.push(\""+rawRule[0]+"\");\n";
				}
			}
		
		}
		
		if (!makeThis){
			continue;
		}
		auto a1 = std::chrono::high_resolution_clock::now();
		RawQuestion q;
		q.qH = doc.GetRow<std::string>(oldIdx+1)[0];
		q.qC = doc.GetRow<std::string>(oldIdx+2)[0];
		q.rangeMap = rangeMap;
		q.rawRules = rawRules;
		questions.push_back(q);
		auto a2 = std::chrono::high_resolution_clock::now();
		int dd1 = std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
		std::cout << "time to makeQuestion(): " << dd1 << "\n";
		int dd2 = std::chrono::duration_cast<std::chrono::microseconds>( a2 - a0 ).count();
		std::cout << "time after rapidcsv: " << dd2 << "\n";
		if (startIdx == oldIdx){
			break;
		}
		
		

	}
	
	return questions;
}

std::vector<RawQuestion> makeQuestionsNew(Dewey qDewey, std::string input){
	

	int i; int ii;
	std::vector<std::string> rows;
	std::string currentRow = "";
	for (i=0;i<input.length();i++){
		if (input.at(i) == '\n'){
			rows.push_back(currentRow);
			currentRow = "";
		}
		else {
			currentRow += input.at(i);
		}
	}
	if (currentRow.length()>0){
		rows.push_back(currentRow);
	}
	
	int nRows = rows.size();


		
	std::vector<RawQuestion> questions;

	
	int startIdx = 0;
	int idx = 0;
	int oldIdx = 0;
	auto a0 = std::chrono::high_resolution_clock::now();
	for (idx=0;idx<nRows;idx++){
		bool makeThis = true;
		Dewey dewey;
		std::string firstRow = rows[startIdx];
		
		if (firstRow.substr(0,10) != ":subtople:"){
			continue;
		}
		std::string rawDewey = firstRow.substr(10,firstRow.length()-10);
		std::string current = "";
		for (i=0;i<rawDewey.length();i++){
			if (rawDewey.at(i)=='.'){
				if (dewey.subject == "."){
					dewey.subject = current;
				}
				else if (dewey.topic == "."){
					dewey.topic = current;
				}
				else if (dewey.lesson == "."){
					dewey.lesson = current;
				}
				else {
					dewey.id = current;
				}
				current = "";
			}
			else {
				current += rawDewey.at(i);
			}
		}
		
		if (current.length()>0){
			if (dewey.subject == "."){
				dewey.subject = current;
			}
			else if (dewey.topic == "."){
				dewey.topic = current;
			}
			else if (dewey.lesson == "."){
				dewey.lesson = current;
			}
			else {
				dewey.id = current;
			}
		}
		std::cout << "dewey: " << dewey.topic << "\n";
		if (dewey <minEq> qDewey){
		}
		else {
			makeThis = false;
		}
		std::vector<std::vector<std::string>> rawRules;

		
	
		if (nRows<startIdx+5){
			break;
		}
		oldIdx = startIdx;

		flat_hash_map<char,std::string> rangeMap;
		RawQuestion q;
		
		std::vector<std::string> currentRawRule;
		currentRawRule.resize(0);
		bool inRule = false;
		for (i=startIdx+1;i<nRows;i++){
			std::string rawRule = rows[i];
			if (rawRule == ""){
				currentRawRule.push_back(rawRule);
				continue;
			}
			if (rawRule.substr(0,10) == ":subtople:"){
				idx--;
				break;
			}
			if (rawRule.substr(0,6) == ":name:"){
				continue;
			}
			
			if (makeThis){
				if (rawRule == "::: layout"){
					if (inRule){
						inRule = false;
					}
					currentRawRule.resize(3);
					currentRawRule[2] = "l";
					currentRawRule[0] = "";
					currentRawRule[1] = "";
					inRule = true;
				}
				else if (rawRule == "::: question"){
					if (inRule){
						inRule = false;
					}
					if (i+2 < nRows){
						q.qC = rows[i+1];
					}
					for (ii=i+3;ii<nRows;ii++){
						if (rows[ii].substr(0,3) == ":::"){
							break;
						}
						if (rows[ii] == ""){continue;}
						std::string range = "";
						char var = rows[ii].at(0);
						range = rows[ii].substr(2,rows[ii].length()-2);
						rangeMap[var]=range;
					}
					i = ii;
					currentRawRule.resize(0);
					inRule = false;
				}
				else if (rawRule == "::: answery"){
					if (inRule){
						inRule = false;
					}
					currentRawRule.resize(4);
					currentRawRule[3] = "";
					currentRawRule[2] = "c";
					if (i+1 < nRows){
						currentRawRule[1] = rows[i+1];
						i++;
					}
					currentRawRule[0] = "a";
					inRule = true;
				}
				else if (rawRule == "::: answern"){
					if (inRule){
						inRule = false;
					}
					currentRawRule.resize(4);
					currentRawRule[3] = "";
					currentRawRule[2] = "i";
					if (i+1 < nRows){
						currentRawRule[1] = rows[i+1];
						i++;
					}
					currentRawRule[0] = "a";
					inRule = true;
				}
				else if (rawRule.substr(0,3) == ":::"){
					if (inRule){
						inRule = false;
						if (currentRawRule[2] == "l"){
							q.qH = "";
							for (ii=3;ii<currentRawRule.size();ii++){
								q.qH += currentRawRule[ii]+"\n";
							}
						}
						else if (currentRawRule[2] == "c" || currentRawRule[2] == "i" || currentRawRule[2] == "e"){
							rawRules.push_back(currentRawRule);
						}
						currentRawRule.resize(0);
					}
				}
				else if (inRule){
					currentRawRule.push_back(rawRule);
				}
		
				/*
				if (rawRule.size() < 3 || rawRule[0] == "t"){
					continue;			
				}
				else if (rawRule[0] != "a" && rawRule[0] != "q"){
					continue;			
				}
				else if (rawRule[0] == "q" && rawRule[1].length() == 1){
					std::string range = "";
					char var = rawRule[1].at(0);
					for (ii=3;ii<rawRule.size();ii++){
						if (ii >3){
							range += ",";
						}
						range += rawRule[ii];
					}
					//std::cout << "range: "<< range << "\n";		
					//varMap[var]=makeInt(range);
					rangeMap[var]=range;
				}
				else if (rawRule[2] == "x"){
					//jsonmessage += "rule.examples.push(\""+rawRule[0]+"\");\n";
				}
				else if (rawRule[2] == "c"){
					
					if (rawRule.size()>5){
						std::vector<std::string> tempV;
						std::string currentCon = "";
						int openPar = 0;
						int iii;
						for (ii=0;ii<rawRule.size();ii++){
							if (ii<4){tempV.push_back(rawRule[ii]);}
							else {
								for (iii=0;iii<rawRule[ii].length();iii++){
									if (rawRule[ii].at(iii) == '['){
										openPar++;
									}
									else if (rawRule[ii].at(iii) == '{'){
										openPar++;
									}
									else if (rawRule[ii].at(iii) == '('){
										openPar++;
									}
									else if (rawRule[ii].at(iii) == '}'){
										openPar--;
									}
									else if (rawRule[ii].at(iii) == ')'){
										openPar--;
									}
									else if (rawRule[ii].at(iii) == ']'){
										openPar--;
									}
									
									if (rawRule[ii].at(iii) == ',' && openPar == 0){
										tempV.push_back(currentCon);
										currentCon = "";
									}
									else {
										currentCon += rawRule[ii].at(iii);
									}
								}
							}
							
						}
						if (currentCon.length()>0){
							tempV.push_back(currentCon);
						}
						rawRules.push_back(tempV);
					}
					else {
						rawRules.push_back(rawRule);
					}
					
					//jsonmessage += "rule.correct.push(\""+rawRule[0]+"\");\n";
				}
				else if (rawRule[2] == "i" || rawRule[2] == "e"){
					if (rawRule.size()>5){
						std::vector<std::string> tempV;
						std::string currentCon = "";
						int openPar = 0;
						int iii;
						for (ii=0;ii<rawRule.size();ii++){
							if (ii<4){tempV.push_back(rawRule[ii]);}
							else {
								for (iii=0;iii<rawRule[ii].length();iii++){
									if (rawRule[ii].at(iii) == '['){
										openPar++;
									}
									else if (rawRule[ii].at(iii) == '{'){
										openPar++;
									}
									else if (rawRule[ii].at(iii) == '('){
										openPar++;
									}
									else if (rawRule[ii].at(iii) == '}'){
										openPar--;
									}
									else if (rawRule[ii].at(iii) == ')'){
										openPar--;
									}
									else if (rawRule[ii].at(iii) == ']'){
										openPar--;
									}
									
									if (rawRule[ii].at(iii) == ',' && openPar == 0){
										tempV.push_back(currentCon);
										currentCon = "";
									}
									else {
										currentCon += rawRule[ii].at(iii);
									}
								}
								
								if (openPar > 0){
									currentCon += ",";
								}
								
								
							}
							
						}
						if (currentCon.length()>0){
							tempV.push_back(currentCon);
						}
						rawRules.push_back(tempV);
					}
					else {
						rawRules.push_back(rawRule);
					}
					//jsonmessage += "rule.incorrect.push(\""+rawRule[0]+"\");\n";
				}
				*/
			}
			
		
		}
		
		if (!makeThis){
			continue;
		}
		auto a1 = std::chrono::high_resolution_clock::now();
		
		q.rangeMap = rangeMap;
		q.rawRules = rawRules;
		q.dewey = dewey;
		questions.push_back(q);
		auto a2 = std::chrono::high_resolution_clock::now();
		int dd1 = std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
		std::cout << "time to makeQuestion(): " << dd1 << "\n";
		int dd2 = std::chrono::duration_cast<std::chrono::microseconds>( a2 - a0 ).count();
		std::cout << "time after rapidcsv: " << dd2 << "\n";
		if (startIdx == oldIdx){
			break;
		}
		
		

	}
	
	return questions;
}

Question previewQuestion(std::string input){
	
	RawQuestion q;
	Question qq;
	const std::string& csv = input;

    std::stringstream sstream(csv);
	rapidcsv::Document doc(sstream, rapidcsv::LabelParams(-1, -1));
	
	int nRows = doc.GetRowCount();
	
	int startIdx = 0;
	int idx = 0;
	int oldIdx = 0;
	auto a0 = std::chrono::high_resolution_clock::now();

	int i; int ii;
	bool makeThis = true;
	Dewey dewey;
	std::vector<std::string> firstRow = doc.GetRow<std::string>(startIdx);
	
	if (firstRow.size() < 1){
		return qq;
	}
	std::string rawDewey = firstRow[0];
	std::string current = "";
	for (i=0;i<rawDewey.length();i++){
		if (rawDewey.at(i)=='.'){
			if (dewey.subject == "."){
				dewey.subject = current;
			}
			else if (dewey.topic == "."){
				dewey.topic = current;
			}
			else if (dewey.lesson == "."){
				dewey.lesson = current;
			}
			else {
				dewey.id = current;
			}
			current = "";
		}
		else {
			current += rawDewey.at(i);
		}
	}
	if (current.length()>0){
		if (dewey.subject == "."){
			dewey.subject = current;
		}
		else if (dewey.topic == "."){
			dewey.topic = current;
		}
		else if (dewey.lesson == "."){
			dewey.lesson = current;
		}
		else {
			dewey.id = current;
		}
	}
	std::cout << dewey.subject << " -- " << dewey.topic << " -- " << dewey.lesson << " -- " << dewey.id << "\n";
	std::vector<std::vector<std::string>> rawRules;

	

	if (nRows<startIdx+5){
		return qq;
	}
	oldIdx = startIdx;

	flat_hash_map<char,std::string> rangeMap;
	for (i=startIdx+5;i<nRows;i++){
		std::vector<std::string> rawRule = doc.GetRow<std::string>(i);
		if (rawRule.size() == 1 && rawRule[0] == ""){
			startIdx = i+1;
			break;
		}
		if (makeThis){
			if (rawRule.size() < 3 || rawRule[0] == "t"){
				continue;			
			}
			else if (rawRule[0] != "a" && rawRule[0] != "q"){
				continue;			
			}
			else if (rawRule[0] == "q" && rawRule[1].length() == 1){
				std::string range = "";
				char var = rawRule[1].at(0);
				for (ii=3;ii<rawRule.size();ii++){
					if (ii >3){
						range += ",";
					}
					range += rawRule[ii];
				}
				//std::cout << "range: "<< range << "\n";		
				//varMap[var]=makeInt(range);
				rangeMap[var]=range;
			}
			else if (rawRule[2] == "x"){
				//jsonmessage += "rule.examples.push(\""+rawRule[0]+"\");\n";
			}
			else if (rawRule[2] == "c"){
				rawRules.push_back(rawRule);
				//jsonmessage += "rule.correct.push(\""+rawRule[0]+"\");\n";
			}
			else if (rawRule[2] == "i" || rawRule[2] == "e"){
				rawRules.push_back(rawRule);
				//jsonmessage += "rule.incorrect.push(\""+rawRule[0]+"\");\n";
			}
		}
	
	}
	
	if (!makeThis){
		return qq;
	}
	auto a1 = std::chrono::high_resolution_clock::now();
	
	q.qH = doc.GetRow<std::string>(oldIdx+1)[0];
	q.qC = doc.GetRow<std::string>(oldIdx+2)[0];
	q.rangeMap = rangeMap;
	q.rawRules = rawRules;
	qq = makeQuestion(q.qC, q.qH, q.rangeMap);
	qq.rawRules = q.rawRules;
	auto a2 = std::chrono::high_resolution_clock::now();
	int dd1 = std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	std::cout << "time to makeQuestion(): " << dd1 << "\n";
	int dd2 = std::chrono::duration_cast<std::chrono::microseconds>( a2 - a0 ).count();
	std::cout << "time after rapidcsv: " << dd2 << "\n";
	
	
	std::vector<std::string> fullPost;
	std::string key;
	std::string val1;
	std::string out;
	answerConstraints.clear();

	for (i=0;i<qq.rawRules.size();i++){
		Rule rule;

		fullPost = makeAnswer(qq.rawRules[i][1]);
		key = fullPost[0];
		val1 = fullPost[1];
		rule.operands = val1;
		rule.type = qq.rawRules[i][2];
		rule.explanation = qq.rawRules[i][3];
		

		//TODO: add more constraint options
	
		if (qq.rawRules[i].size()>4){
			std::string constraint = constraintify(qq.rawRules[i][4]);
			std::string postfixed = postfixify(constraint);
			//std::cout <<" postfixed " << postfixed << "\n";
			rule.constraints.push_back(postfixed);
		}
	
	
		if (rules.find(key) != rules.end()){
			answerConstraints[key].push_back(rule);
		}
		else {
			answerConstraints[key] = {rule};
		}
	
	
	
	}
		

	
	return qq;
}

