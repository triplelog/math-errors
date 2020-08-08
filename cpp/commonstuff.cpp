bool checkAnswer(std::string answer);
std::string makeInt(std::string input);
flat_hash_map<char,int> prec;

flat_hash_map<std::string,std::vector<int>> constraintsMet;
//flat_hash_map<std::string,std::vector<std::string>> allListMapFull;
//flat_hash_map<std::string,std::vector<std::vector<std::string>>> allListMapBottom;
flat_hash_map<std::string,bool> constraintMap;

std::string jsonmessage;
int duration1;
int duration2;
int duration3;
int yesC;
int noC;
int mapSave;
int mapMake;
int overallScore;
bool answerIsFinished;
flat_hash_map<int,int> eloMap;


struct RawQuestion {
	std::string qH = "";
	std::string qC = "";
	flat_hash_map<char,std::string> rangeMap;
	std::vector<std::vector<std::string>> rawRules;
};
struct Dewey {
	std::string subject = ".";
	std::string topic = ".";
	std::string rule = ".";
	std::string id = ".";
};
struct Question {
	std::string text = "";
	std::string comp = "";
	std::vector<std::vector<std::string>> rawRules;
	Dewey dewey;
};

struct Rule {
	std::string operands = "";
	std::string out = "";
	std::string type = "";
	std::string explanation = "";
	std::vector<std::string> constraints;
	int score = 0;
	int k = 1000;
	int id;
};
struct Step {
	std::string next = "";
	int rule;
};
struct Answer {
	bool finished = false;
	bool correct = false;
	std::string next = "";
	std::string input = "";
	std::vector<Step> solution;
};
struct OperatorProxy
{
    int op = 0;
    Dewey dewey;
};


OperatorProxy operator<(const Dewey& a, const OperatorProxy& b){
	OperatorProxy c;
	c.dewey = a;
	c.op = b.op;
	return c;
}
OperatorProxy subjectEq;
OperatorProxy topicEq;
OperatorProxy ruleEq;
OperatorProxy idEq;
OperatorProxy minEq;
inline bool operator>(const OperatorProxy& a, const Dewey& b){
	if (a.op == 0){
		if (a.dewey.subject == b.subject && a.dewey.topic == b.topic && a.dewey.rule == b.rule && a.dewey.id == b.id){
			return true;
		}
		return false;
	}
	else if (a.op == 1){
		if (a.dewey.subject == b.subject){
			return true;
		}
		return false;
	}
	else if (a.op == 2){
		if (a.dewey.subject == b.subject && a.dewey.topic == b.topic){
			return true;
		}
		return false;
	}
	else if (a.op == 3){
		if (a.dewey.subject == b.subject && a.dewey.topic == b.topic && a.dewey.rule == b.rule){
			return true;
		}
		return false;
	}
	else if (a.op == 4){
		if (a.dewey.subject == "." || b.subject == "."){
			return true;
		}
		else if (a.dewey.topic == "." || b.topic == "."){
			return (a.dewey <subjectEq> b);
		}
		else if (a.dewey.rule == "." || b.rule == "."){
			return (a.dewey <topicEq> b);
		}
		else if (a.dewey.id == "." || b.id == "."){
			return (a.dewey <ruleEq> b);
		}
		else {
			return (a.dewey <idEq> b);
		}
		return false;
	}
	
	return false;
}
std::vector<Step> applyRulesVectorOnePart(std::string onePart,std::vector<int> oneIndex, std::string userFullString, bool isCorrect);
Question currentQuestion;

flat_hash_map<std::string,std::vector<Rule>> rules;
flat_hash_map<int,Rule> ruleIndex;
int ridx;
flat_hash_map<std::string,std::vector<Rule>> answerConstraints;

flat_hash_map<std::string,std::string> toLatex(std::vector<std::string> input){
	int i; int ii;
	flat_hash_map<std::string,std::string> latexMap;
	flat_hash_map<std::string,char> lastOpMap;
	flat_hash_map<std::string,std::vector<std::string>> childMap;
	childMap[""]={};
	for (i=0;i<input.size()/3;i++){
		//std::cout << input[i*3] << "\n";
		//std::cout << input[i*3+1] << "\n";
		//std::cout << input[i*3+2] << "\n";
		char lastOp = '#';
		bool foundAt = false;
		std::string firstOperand = "";
		for (ii=0;ii<input[i*3+2].size();ii++){
			if (input[i*3+2].at(ii) == '@'){
				foundAt = true;
			}
			else if (!foundAt){
				lastOp = input[i*3+2].at(ii);
			}
			else if (input[i*3+2].at(ii) == '_'){
				break;
			}
			else {
				firstOperand += input[i*3+2].at(ii);
			}
		}
		latexMap[input[i*3]]="";
		childMap[input[i*3]]={};
		childMap[input[i*3+1]].push_back(input[i*3]);
		if (lastOp == '#'){
			latexMap[input[i*3]]=firstOperand;
			lastOpMap[input[i*3]]='#';
			//std::cout << firstOperand << " is first s of: " << input[i*3] <<"\n";
		}
		else {
			lastOpMap[input[i*3]]=lastOp;
		}
	}
	int newLatex = 1;
	int count =0;
	while (newLatex>0 && count < 1000){
		newLatex = 0;
		for (i=0;i<input.size()/3;i++){
			bool allChildren = true;
			std::string s = "";
			for (ii=0;ii<childMap[input[i*3]].size();ii++){
				std::string child = childMap[input[i*3]][ii]; //is name of child
				//std::cout << "child: " << child << " latex of child: " << latexMap[child] << " and s: " << s << "\n";
				if (latexMap[child] == ""){
					allChildren = false;
					break;
				}
				else {
					switch (lastOpMap[input[i*3]]){
						case '^': {
							if (ii > 0){
								s += "^{";
								s += latexMap[child]+"}";
							}
							else {
								if (prec[lastOpMap[child]] < 100){
									s += "\\\\left("+latexMap[child]+"\\\\right)";
								}
								else {
									s += latexMap[child];
								}
							}
							break;
						}
						case -69: {
							if (ii > 0){
								s += latexMap[child]+"\\\\right]";
							}
							else {
								s += "\\\\frac{d}{d"+latexMap[child]+"}\\\\left[";
							}
							break;
						
						}
						case -85: {
							if (ii > 0){
								s.replace(6,0,latexMap[child]+" \\\\text{d");
							}
							else {
								s += "\\\\int "+latexMap[child]+"}";
							}
							break;
						
						}
						case -34:
							s += "|"+latexMap[child]+"|";
							break;
						case -64:
							s += "\\\\sin\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -63:
							s += "\\\\cos\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -62:
							s += "\\\\tan\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -61:
							s += "\\\\csc\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -60:
							s += "\\\\sec\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -59:
							s += "\\\\cot\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -32:
							s += "\\\\sin^{-1}\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -31:
							s += "\\\\cos^{-1}\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -30:
							s += "\\\\tan^{-1}\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -29:
							s += "\\\\csc^{-1}\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -28:
							s += "\\\\sec^{-1}\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -27:
							s += "\\\\cot^{-1}\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -16:
							s += "\\\\text{sinh}\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -15:
							s += "\\\\text{cosh}\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -14:
							s += "\\\\text{tanh}\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -13:
							s += "\\\\text{csch}\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -12:
							s += "\\\\text{sech}\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -11:
							s += "\\\\text{coth}\\\\left("+latexMap[child]+"\\\\right)";
							break;
						case -67:
							s += "\\\\sqrt{"+latexMap[child]+"}";
							break;
						case -84: {
							if (ii > 0){
								s += latexMap[child]+"}";
							}
							else {
								s += "\\\\sqrt["+latexMap[child]+"]{";
							}
							break;
						
						}
						case -93: {
							if (ii > 0){
								if (prec[lastOpMap[child]] < 100){
									s += "\\\\left("+latexMap[child]+"\\\\right)";
								}
								else {
									s += latexMap[child];
								}
								
							}
							else {
								if (latexMap[child] == "e"){
									s += "\\\\ln ";
								}
								else {
									s += "\\\\log_{"+latexMap[child]+"} ";
								}
							}
							break;
						
						}
						case '-': {
							if (prec[lastOpMap[input[i*3]]] >= prec[lastOpMap[child]]){
								s += "-("+latexMap[child]+")";
							}
							else {
								s += "-"+latexMap[child];
							}
							break;
						}
						case '/': {
							s += "\\\\frac{1}{"+latexMap[child]+"}";
							/*
							if (prec[lastOpMap[input[i*3]]] >= prec[lastOpMap[child]]){
								s += "/("+latexMap[child]+")";
							}
							else {
								s += "/"+latexMap[child];
							}*/
							break;
						}
						default: {
							if (prec[lastOpMap[input[i*3]]] > prec[lastOpMap[child]]){
								if (ii > 0){
									if (lastOpMap[input[i*3]] == '*'){
										s += "\\\\cdot ("+latexMap[child]+")";
									}
									else {
										s += lastOpMap[input[i*3]]+"("+latexMap[child]+")";
									}
								}
								else {
									s += "("+latexMap[child]+")";
								}
							}
							else if (prec[lastOpMap[input[i*3]]] == prec[lastOpMap[child]] && lastOpMap[input[i*3]] != lastOpMap[child]){
								if (ii > 0){
									if (lastOpMap[input[i*3]] == '*'){
										s += "\\\\cdot "+latexMap[child];//want to move this into numerator somehow
									}
									else if (lastOpMap[input[i*3]] == '+'){
										s += latexMap[child];
									}
									else {
										s += lastOpMap[input[i*3]]+"("+latexMap[child]+")";
									}
								}
								else {
									if (lastOpMap[input[i*3]] == '*'){
										s += latexMap[child];
									}
									else if (lastOpMap[input[i*3]] == '+'){
										s += latexMap[child];
									}
									else {
										s += "("+latexMap[child]+")";
									}
								}
							}
							else {
								if (ii > 0){
									if (lastOpMap[input[i*3]] == '*'){
										s += "\\\\cdot "+latexMap[child];
									}
									else {
										s += lastOpMap[input[i*3]]+latexMap[child];
									}
								}
								else {
									s += latexMap[child];
								}
							}
						}
					}
					
				}
			}
			if (allChildren && latexMap[input[i*3]]=="" && s != ""){
				newLatex++;
				latexMap[input[i*3]]=s;
				//std::cout << "\ns: "<< s << " is s for " << input[i*3] << "\n";
			}
		}
		count++;
	}

	
	return latexMap;
}

std::string removeBracketsOne(std::string input) {
	flat_hash_map<int,int> operandToIndex;
	int iii; int iiii;
	bool foundBracket = false;
	bool foundAt = false;
	int idx = 0;
	int iidx = 0;
	std::vector<std::string> bracketStrings;
	std::string tempString = "";
	int bracketLength = 0;
	int secondIndex;
	char mychar;
	int len = input.length();
	for (iii=0;iii<len;iii++){
		mychar = input.at(iii);
		if (mychar == '{'){
			foundBracket = true;
			bracketLength = 1;
			secondIndex = iii;
		}
		else if (mychar == '}') {
			bracketStrings.push_back(tempString);
			bracketLength++;
			break;
		}
		else if (mychar == '#' && !foundBracket) {
			operandToIndex[idx]=iii;
			idx++;
		}
		else if (mychar == '_' && !foundBracket) {
			iidx++;
		}
		else if (mychar == '@' && !foundBracket) {
			foundAt = true;
		}
		else if (mychar == '@' && foundBracket) {
			//tempString += input.at(iii);
			bracketStrings.push_back(tempString);
			tempString = "";
			bracketLength++;
		}
		else if (foundBracket){
			tempString += mychar;
			bracketLength++;
		}
	}
	if (!foundBracket){
		return input;
	}
	
	int firstIndex = operandToIndex[iidx];
	//std::cout << input << " --a\n";
	input.replace(secondIndex,bracketLength+1,bracketStrings[1]);
	//std::cout << input << " --b\n";
	input.replace(firstIndex,1,bracketStrings[0]);
	//std::cout << input << " --c\n";
	return removeBracketsOne(input);
	
	
	
}

std::string removeParOne(std::string input) {
	flat_hash_map<int,int> operandToIndex;
	int iii; int iiii;
	bool foundBracket = false;
	bool foundAt = false;
	int idx = 0;
	int iidx = 0;
	std::vector<std::string> bracketStrings;
	std::string tempString = "";
	int bracketLength = 0;
	int secondIndex;
	char mychar;
	int len = input.length();
	bool interiorBrackets = false;
	for (iii=0;iii<len;iii++){
		mychar = input.at(iii);
		if (mychar == '('){
			foundBracket = true;
			bracketLength = 1;
			secondIndex = iii;
		}
		else if (mychar == ')') {
			bracketStrings.push_back(tempString);
			bracketLength++;
			break;
		}
		else if (mychar == '{'){ //Must always be inside of a par
			interiorBrackets = true;
			tempString += mychar;
			bracketLength++;
		}
		else if (mychar == '}') {
			interiorBrackets = false;
			tempString += mychar;
			bracketLength++;
		}
		else if (mychar == '#' && !foundBracket && !interiorBrackets) {
			operandToIndex[idx]=iii;
			idx++;
		}
		else if (mychar == '_' && !foundBracket && !interiorBrackets) {
			iidx++;
		}
		else if (mychar == '@' && !foundBracket && !interiorBrackets) {
			foundAt = true;
		}
		else if (mychar == '@' && foundBracket && !interiorBrackets) {
			//tempString += input.at(iii);
			bracketStrings.push_back(tempString);
			tempString = "";
			bracketLength++;
		}
		else if (foundBracket){
			tempString += mychar;
			bracketLength++;
		}
	}
	if (!foundBracket){
		return input;
	}
	
	int firstIndex = operandToIndex[iidx];
	//std::cout << input << " --a\n";
	input.replace(secondIndex,bracketLength+1,bracketStrings[1]);
	//std::cout << input << " --b\n";
	input.replace(firstIndex,1,bracketStrings[0]);
	//std::cout << input << " --c\n";
	return removeParOne(input);
	
	
	
}

std::string fromOriginal(std::string input,flat_hash_map<int,std::string> originalMap) {
	int i;
	bool startOperands = false;
	std::vector<std::string> indexes;
	int currentOperator = 0;
	int startIndex = 0;
	for (i=0;i<input.length();i++){
		if (input.at(i) == '@'){
			startOperands = true;
			startIndex = i;
		}
		else if (startOperands){
			if (input.at(i) == '_'){
				indexes.push_back(std::to_string(startIndex+1));
				indexes.push_back(std::to_string(i - (startIndex+1)));
				indexes.push_back(originalMap[currentOperator]);
				currentOperator = 0;
				startIndex = i;
			}
			else {
				currentOperator = currentOperator*10 + (input.at(i) - '0');
			}
		}
	}
	for (i=indexes.size()/3-1;i>=0;i--){
		input.replace(std::stoi(indexes[i*3]),std::stoi(indexes[i*3+1]),indexes[i*3+2]);
	}
	return input;
}