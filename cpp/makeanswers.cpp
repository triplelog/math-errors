std::string latexOne(std::string input) {

	int i; int ii; int iii; int idx = 0;
	bool startOperands = false;
	std::string currentOperator = "";
	flat_hash_map<int,std::string> originalMap;
	int iidx = 0;
	std::string pfstr = input;
	
	for (i=0;i<pfstr.length();i++){
		if (pfstr.at(i) == '@'){
			startOperands = true;
		}
		else if (startOperands){
			if (pfstr.at(i) == '_'){
				originalMap[iidx] = currentOperator;
				iidx++; 
				currentOperator = "";
			}
			else {
				currentOperator += pfstr.at(i);
			}
		}
	}
	
	flat_hash_map<std::string,std::string> listMap;
	flat_hash_map<std::string,char> lastOpMap;
	
	flat_hash_map<int,std::string> operandMap;
	std::string lastInput = "";
	for (i=0;i<pfstr.length();i++){
		if (pfstr.at(i) == '@'){
			break;
		}
		else if (pfstr.at(i) != '#'){
			std::string secondStr = "";
			std::string secondTtr = "";
			std::string secondChild = "";
			int maxi = i-1;
			
			for (ii=0;ii<i;ii++){
				std::string s = "";
				std::string t = "";
				for (iii=ii;iii<i;iii++){
					s += pfstr.at(iii);
					if (pfstr.at(iii) == '#'){
						t += operandMap[iii] + '_';
					}
				}
				if (listMap.find(s + '@' + t) != listMap.end()){
					secondStr = s;
					secondTtr = t;
					secondChild = s + '@' + t;
					maxi = ii;
					break;
				}
			}
			std::string firstStr = "";
			std::string firstTtr = "";
			std::string firstChild = "";
			std::vector<std::string> fullTrees;
			
			if (pfstr.at(i) != '-' && pfstr.at(i) != '/' && (pfstr.at(i) >= 0 || pfstr.at(i) <= -69 )){ // Is at least binary function
				
				for (ii=0;ii<maxi;ii++){
					std::string s = "";
					std::string t = "";
					for (iii=ii;iii<maxi;iii++){
						s += pfstr.at(iii);
						if (pfstr.at(iii) == '#'){
							t += operandMap[iii] + '_';
						}
					}
					if (listMap.find(s + '@' + t) != listMap.end()){
						firstStr = s;
						firstTtr = t;
						firstChild = s + '@' + t;
						break;
					}
				}
				
				
			}
			std::string fullStr = firstStr + secondStr + pfstr.at(i) + '@' + firstTtr + secondTtr;
			
			std::string s = "";
			for (ii=0;ii<2;ii++){
				std::string child = secondChild;
				if (ii==0 && firstChild != ""){
					child = firstChild;
				}
				else if (ii==1 && firstChild == ""){
					break;
				}
				switch (pfstr.at(i)){
					case '^': {
						if (ii > 0){
							s += "^{";
							s += listMap[child]+"}";
						}
						else {
							if (prec[lastOpMap[child]] < 100){
								s += "("+listMap[child]+")";
							}
							else {
								s += listMap[child];
							}
						}
						break;
					}
					case -69: {
						if (ii > 0){
							s += listMap[child]+"]";
						}
						else {
							s += "\\\\frac{d}{d"+listMap[child]+"}[";
						}
						break;
			
					}
					case -85: {
						if (ii > 0){
							s.replace(6,0,listMap[child]+" \\\\text{d");
						}
						else {
							s += "\\\\int "+listMap[child]+"}";
						}
						break;
			
					}
					case -34:
						s += "|"+listMap[child]+"|";
						break;
					case -64:
						s += "\\\\sin("+listMap[child]+")";
						break;
					case -63:
						s += "\\\\cos("+listMap[child]+")";
						break;
					case -62:
						s += "\\\\tan("+listMap[child]+")";
						break;
					case -61:
						s += "\\\\csc("+listMap[child]+")";
						break;
					case -60:
						s += "\\\\sec("+listMap[child]+")";
						break;
					case -59:
						s += "\\\\cot("+listMap[child]+")";
						break;
					case -32:
						s += "\\\\sin^{-1}("+listMap[child]+")";
						break;
					case -31:
						s += "\\\\cos^{-1}("+listMap[child]+")";
						break;
					case -30:
						s += "\\\\tan^{-1}("+listMap[child]+")";
						break;
					case -29:
						s += "\\\\csc^{-1}("+listMap[child]+")";
						break;
					case -28:
						s += "\\\\sec^{-1}("+listMap[child]+")";
						break;
					case -27:
						s += "\\\\cot^{-1}("+listMap[child]+")";
						break;
					case -16:
						s += "\\\\text{sinh}("+listMap[child]+")";
						break;
					case -15:
						s += "\\\\text{cosh}("+listMap[child]+")";
						break;
					case -14:
						s += "\\\\text{tanh}("+listMap[child]+")";
						break;
					case -13:
						s += "\\\\text{csch}("+listMap[child]+")";
						break;
					case -12:
						s += "\\\\text{sech}("+listMap[child]+")";
						break;
					case -11:
						s += "\\\\text{coth}("+listMap[child]+")";
						break;
					case -67:
						s += "\\\\sqrt{"+listMap[child]+"}";
						break;
					case -84: {
						if (ii > 0){
							s += listMap[child]+"}";
						}
						else {
							s += "\\\\sqrt["+listMap[child]+"]{";
						}
						break;
			
					}
					case -93: {
						if (ii > 0){
							if (prec[lastOpMap[child]] < 100){
								s += "("+listMap[child]+")";
							}
							else {
								s += listMap[child];
							}
					
						}
						else {
							if (listMap[child] == "e"){
								s += "\\\\ln ";
							}
							else {
								s += "\\\\log_{"+listMap[child]+"} ";
							}
						}
						break;
			
					}
					case '-': {
						if (prec[pfstr.at(i)] >= prec[lastOpMap[child]]){
							s += "-("+listMap[child]+")";
						}
						else {
							s += "-"+listMap[child];
						}
						break;
					}
					case '/': {
						s += "\\\\frac{1}{"+listMap[child]+"}";
						/*
						if (prec[pfstr.at(i)] >= prec[lastOpMap[child]]){
							s += "/("+listMap[child]+")";
						}
						else {
							s += "/"+listMap[child];
						}*/
						break;
					}
					default: {
						if (prec[pfstr.at(i)] > prec[lastOpMap[child]]){
							if (ii > 0){
								if (pfstr.at(i) == '*'){
									s += "\\\\cdot ("+listMap[child]+")";
								}
								else {
									s += pfstr.at(i)+"("+listMap[child]+")";
								}
							}
							else {
								s += "("+listMap[child]+")";
							}
						}
						else if (prec[pfstr.at(i)] == prec[lastOpMap[child]] && pfstr.at(i) != lastOpMap[child]){
							if (ii > 0){
								if (pfstr.at(i) == '*'){
									s += "\\\\cdot "+listMap[child];//want to move this into numerator somehow
								}
								else if (pfstr.at(i) == '+'){
									s += listMap[child];
								}
								else {
									s += pfstr.at(i)+"("+listMap[child]+")";
								}
							}
							else {
								if (pfstr.at(i) == '*'){
									s += listMap[child];
								}
								else if (pfstr.at(i) == '+'){
									s += listMap[child];
								}
								else {
									s += "("+listMap[child]+")";
								}
							}
						}
						else {
							if (ii > 0){
								if (pfstr.at(i) == '*'){
									s += "\\\\cdot "+listMap[child];
								}
								else {
									s += pfstr.at(i)+listMap[child];
								}
							}
							else {
								s += listMap[child];
							}
						}
					}
				}
			}
			
			listMap[fullStr]=s;
			lastOpMap[fullStr]=pfstr.at(i);
			lastInput = s;
			
		}
		else {
			listMap["#@" + std::to_string(idx) + "_"]=originalMap[idx];
			lastOpMap["#@" + std::to_string(idx) + "_"]='#';
			operandMap[i]=std::to_string(idx);
			lastInput = originalMap[idx];
			idx++;
		}
		
	}
	
	std::cout << lastInput << "\n";
	return lastInput;


}

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
	//std::cout << postfixed;
	return postfixed;
	//return makeTree(postfixed)[0];
}



Question chooseQuestion(std::string dewey, std::vector<Question> questions){
	Question q = questions[0];
	std::vector<std::string> fullPost;
	std::string key;
	std::string val1;
	std::string out;
	answerConstraints.clear();
	int i;
	for (i=0;i<q.rawRules.size();i++){
		std::vector<std::string> rule;

		fullPost = makeAnswer(q.rawRules[i][1]);
		key = fullPost[0];
		val1 = fullPost[1];
		rule = {val1,q.rawRules[i][2],q.rawRules[i][3]};
		

		//TODO: add more constraint options
	
		if (q.rawRules[i].size()>4){
			std::string constraint = constraintify(q.rawRules[i][5]);
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
	return q;
}


Question makeQuestion(std::string qRow, std::string qText,flat_hash_map<char,std::string> varMap){
	Question question;
	std::string q = postfixify(qRow);
	int i;
	std::string newQ = replaceVars(q,varMap);
	std::cout << "question for computer: " << newQ << "\n\n";
	question.comp = newQ;

	bool isMath = false;
	std::string newText = "";
	std::string currentMath = "";
	for (i=0;i<qText.length();i++){
		if (qText.at(i)== '$'){
			if (isMath){
				isMath = false;
				std::cout << "cm: " << currentMath << "\n";
				std::string pf = postfixify(currentMath);
				std::cout << "pf: " << pf << "\n";
				pf = replaceVars(pf,varMap);
				std::cout << "pf: " << pf << "\n";
				pf = latexOne(pf);
				std::cout << "pf: " << pf << "\n";
				
				newText += pf;
			}
			else {
				isMath = true;
			}
		}
		else if (isMath) {
			currentMath += qText.at(i);
		}
		else {
			newText += qText.at(i);
		}
	}

	question.text = newText;
	return question;
}

std::vector<Question> makeQuestions(std::string fileName){
	
	std::vector<Question> questions;
	rapidcsv::Document doc("cpp/rules/"+fileName, rapidcsv::LabelParams(-1, -1));
	
	int nRows = doc.GetRowCount();
	
	int startIdx = 0;
	int idx = 0;
	int oldIdx = 0;
	auto a0 = std::chrono::high_resolution_clock::now();
	for (idx=0;idx<nRows;idx++){
		int i; int ii;
		bool makeThis = true;
		std::vector<std::string> dewey;
		std::vector<std::string> firstRow = doc.GetRow<std::string>(startIdx);
		
		if (firstRow.size() < 1){
			continue;
		}
		std::string rawDewey = firstRow[0]:
		std::string current = "";
		for (i=0;i<rawDewey.length();i++){
			if (rawDewey.at(i)=='.'){
				dewey.push_back(current);
				current = "";
			}
			else {
				current += rawDewey.at(i);
			}
		}
		if (current.length()>0){
			dewey.push_back(current);
		}
		if (dewey[0] != "algebra"){
			makeThis = false;
		}
		std::vector<std::vector<std::string>> rawRules;

		
	
		if (nRows<startIdx+5){
			break;
		}
		oldIdx = startIdx;

		flat_hash_map<char,std::string> varMap;
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
		
		}
		
		if (!makeThis){
			continue;
		}
		auto a1 = std::chrono::high_resolution_clock::now();
		Question q = makeQuestion(doc.GetRow<std::string>(oldIdx+2)[0], doc.GetRow<std::string>(oldIdx+1)[0], varMap);
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