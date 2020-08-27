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



struct Dewey {
	std::string subject = ".";
	std::string topic = ".";
	std::string lesson = ".";
	std::string id = ".";
};
struct RawQuestion {
	std::string qH = "";
	std::string qC = "";
	flat_hash_map<char,std::string> rangeMap;
	std::vector<std::vector<std::string>> rawRules;
	Dewey dewey;
};
struct Question {
	std::string text = "";
	std::string comp = "";
	std::vector<std::vector<std::string>> rawRules;
	Dewey dewey;
};

struct Rule {
	std::string key = "";
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
	int startNode;
	int endNode;
	std::vector<int> endNodes;
	std::vector<int> startNodes;
	flat_hash_map<char,std::string> partMap;
	
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

struct Number {
	int type = 0;
	std::string top = "";
	std::string bottom = "";
};
struct Range {
	std::vector<Number> left;
	std::vector<Number> right;
	std::vector<char> incexc;
};
Range makeRange(std::string input);
Number solvePostfix(std::string postfix);
std::string outputNumber(Number n);
std::string substitute(std::string input);
std::string numberType(std::string input);
Number mulTwo(Number numA, Number numB);
Number invertOne(Number numA);
Number negateOne(Number numA);

inline bool operator>(const Number& a, const Number& b){
	if (a.type == 0 || b.type == 0){return false;}
	if (a.type == 1){
		if (b.type == 1){
			if (a.top.length()>b.top.length()){
				return true;
			}
			else if (a.top.length()<b.top.length()){
				return false;
			}
			else {
				int ii;
				for (ii=0;ii<a.top.length();ii++){
					if (a.top.at(ii) > b.top.at(ii)){
						return true;
					}
					else if (a.top.at(ii) < b.top.at(ii)){
						return false;
					}
				}
				return false;
			}
		}
		else if (b.type == 2 || b.type == 3){
			if (a.top.length()>b.top.length()){
				return true;
			}
			else {
				Number n;
				n.type = 2;
				n.top = a.top;
				n.bottom = "1";
				return n > b;
			}
		}
		else if (b.type < 0){
			return true;
		}
	}
	else if (a.type == 2 || a.type == 3){
		if (b.type == 1){
			if (a.top.length()<b.top.length()){
				return false;
			}
			else {
				Number n;
				n.type = 2;
				n.top = b.top;
				n.bottom = "1";
				return a > n;
			}
		}
		else if (b.type == 2 || b.type == 3){
			if (a.top.length() + b.bottom.length() > a.bottom.length()+b.top.length()+1){
				return true;
			}
			else if (a.top.length() + b.bottom.length() + 1 < a.bottom.length()+b.top.length()){
				return false;
			}
			else if (a.top == "0"){
				return false;
			}
			else if (b.top == "0"){
				return true;
			}
			else {
				Number n = mulTwo(a,invertOne(b));
				if (n.top.length()>n.bottom.length()){
					return true;
				}
				else if (n.top.length()<n.bottom.length()){
					return false;
				}
				else {
					int ii;
					for (ii=0;ii<n.top.length();ii++){
						if (n.top.at(ii) > n.bottom.at(ii)){
							return true;
						}
						else if (n.top.at(ii) < n.bottom.at(ii)){
							return false;
						}
					}
					return false;
				}
			}
		}
		else if (b.type < 0){
			return true;
		}
	}
	else if (a.type < 0){
		if (b.type < 0){
			return negateOne(b) > negateOne(a);
		}
		else if (b.type > 0){
			return false;
		}
	}
	return true;
}
inline bool operator<(const Number& a, const Number& b){
	if (a.type == 0 || b.type == 0){return false;}
	return b > a;
	/*
	if (a.type == 1){
		if (b.type == 1){
			if (a.top.length()<b.top.length()){
				return true;
			}
			else if (a.top.length()>b.top.length()){
				return false;
			}
			else {
				int ii;
				for (ii=0;ii<a.top.length();ii++){
					if (a.top.at(ii) < b.top.at(ii)){
						return true;
					}
					else if (a.top.at(ii) > b.top.at(ii)){
						return false;
					}
				}
				return false;
			}
		}
		else if (b.type == 2 || b.type == 3){
			if (a.top.length()<b.top.length()){
				return true;
			}
			else {
				Number n;
				n.type = 2;
				n.top = a.top;
				n.bottom = "1";
				return n < b;
			}
		}
		else if (b.type < 0){
			return false;
		}
	}
	else if (a.type == 2 || a.type == 3){
		if (b.type == 1){
			if (a.top.length()>b.top.length()){
				return false;
			}
			else {
				Number n;
				n.type = 2;
				n.top = b.top;
				n.bottom = "1";
				return a < n;
			}
		}
		else if (b.type == 2 || b.type == 3){
			if (a.top.length() + b.bottom.length() +1 < a.bottom.length()+b.top.length()){
				return true;
			}
			else if (a.top.length() + b.bottom.length() > a.bottom.length()+b.top.length() + 1){
				return false;
			}
			else if (b.top == "0"){
				return false;
			}
			else if (a.top == "0"){
				return true;
			}
			else {
				Number n = mulTwo(a,invertOne(b));
				if (n.top.length()<n.bottom.length()){
					return true;
				}
				else if (n.top.length()>n.bottom.length()){
					return false;
				}
				else {
					int ii;
					for (ii=0;ii<n.top.length();ii++){
						if (n.top.at(ii) < n.bottom.at(ii)){
							return true;
						}
						else if (n.top.at(ii) > n.bottom.at(ii)){
							return false;
						}
					}
					return false;
				}
			}
		}
		else if (b.type < 0){
			return false;
		}
	}
	else if (a.type < 0){
		if (b.type < 0){
			return negateOne(b) < negateOne(a);
		}
		else if (b.type > 0){
			return true;
		}
	}
	return true;
	*/
}
inline bool operator>=(const Number& a, const Number& b){
	if (a.type == 0 || b.type == 0){return false;}
	if (a < b){return false;}
	else {return true;}
}
inline bool operator<=(const Number& a, const Number& b){
	if (a.type == 0 || b.type == 0){return false;}
	if (a > b){return false;}
	else {return true;}
}
inline bool operator==(const Number& a, const Number& b){
	if (a.type == 0 || b.type == 0){return false;}
	if (a<b || a>b){
		return false;
	}
	return true;
}
flat_hash_map<std::string,Number> numbers;

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
		if (a.dewey.subject == b.subject && a.dewey.topic == b.topic && a.dewey.lesson == b.lesson && a.dewey.id == b.id){
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
		if (a.dewey.subject == b.subject && a.dewey.topic == b.topic && a.dewey.lesson == b.lesson){
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
		else if (a.dewey.lesson == "." || b.lesson == "."){
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

flat_hash_map<int,int> removeParList(flat_hash_map<int,int> nodes, std::string input);

#include "latexify.cpp"

#include "postfixify.cpp"

#include "makerules.cpp"

#include "makeanswers.cpp"

#include "applyrules.cpp"

#include "makenumbers.cpp"

std::string displayOne(Step step,std::string start,std::string end){
	flat_hash_map<char,std::string> partMap = step.partMap;
	if (step.rule < 0){
		return "";
	}
	std::string oneStep = "{\"start\":\""+latexOne(start,step.startNode,{})+"\",";
	std::string oldString = ruleIndex[step.rule].key + "@" + ruleIndex[step.rule].operands;
	
	oneStep += "\"input\":\""+latexOne(oldString)+"\",\"map\":[";

	for (flat_hash_map<char,std::string>::iterator iter = partMap.begin(); iter != partMap.end(); ++iter){
		std::string s(1,iter->first);
		std::string sec = iter->second;
		if (sec.length()>0 && sec.at(0) == '{'){
			sec = sec.substr(1,sec.length()-2);
			sec = latexOne(sec);
		}
		if (oneStep.at(oneStep.length()-1)=='['){
			oneStep += "\"" + s +"\",\""+ sec +"\"";
		}
		else {
			oneStep += ",\"" + s +"\",\""+ sec +"\"";
		}
		
	}
	oneStep += "],";
	oneStep += "\"output\":\""+latexOne(ruleIndex[step.rule].out)+"\",";
	int eNode = step.endNode;
	if (step.endNodes.size() > 0){
		eNode = step.endNodes[step.endNodes.size()-1];
	}
	oneStep += "\"final\":\""+latexOne(removeBracketsOne(end),eNode,{})+"\"}";
	
	return oneStep;
}

bool firstCorrect;
void initialRun(){
	prec['~'] = 101;
	prec['#'] = 100;
	int i;
	for (i=-128;i<0;i++){
		prec[i]=6;
	}
    prec['^'] = 5;
	prec['*'] = 4;
	prec['/'] = 4;
	prec['+'] = 3;
	prec['-'] = 3;
	prec['>'] = 2;
	prec['<'] = 2;
	prec['='] = 2;
	prec['!'] = 2;
	prec['['] = 2;
	prec[']'] = 2;
	prec[-94] = 2;//does not contain
	prec[-87] = 2;//contains
	prec[-111] = 2;//is
	prec[-110] = 2;//is not
	prec[-95] = 2;//in
	prec[-96] = 2;//not in
	prec['&'] = 1;
	prec['|'] = 0;
	prec['('] = -1;
	prec[')'] = -1;
	eloMap[1]=19956; eloMap[2]=16902; eloMap[3]=15097; eloMap[4]=13802; eloMap[5]=12788; eloMap[6]=11950; eloMap[7]=11234; eloMap[8]=10607; eloMap[9]=10048; eloMap[10]=9542; eloMap[11]=9080; eloMap[12]=8653; eloMap[13]=8256; eloMap[14]=7884; eloMap[15]=7533; eloMap[16]=7202; eloMap[17]=6886; eloMap[18]=6585; eloMap[19]=6297; eloMap[20]=6021; eloMap[21]=5754; eloMap[22]=5497; eloMap[23]=5248; eloMap[24]=5006; eloMap[25]=4771; eloMap[26]=4543; eloMap[27]=4320; eloMap[28]=4102; eloMap[29]=3889; eloMap[30]=3680; eloMap[31]=3475; eloMap[32]=3274; eloMap[33]=3076; eloMap[34]=2881; eloMap[35]=2688; eloMap[36]=2499; eloMap[37]=2311; eloMap[38]=2126; eloMap[39]=1943; eloMap[40]=1761; eloMap[41]=1581; eloMap[42]=1402; eloMap[43]=1224; eloMap[44]=1047; eloMap[45]=872; eloMap[46]=696; eloMap[47]=522; eloMap[48]=348; eloMap[49]=174; eloMap[50]=0; eloMap[51]=-174; eloMap[52]=-348; eloMap[53]=-522; eloMap[54]=-696; eloMap[55]=-872; eloMap[56]=-1047; eloMap[57]=-1224; eloMap[58]=-1402; eloMap[59]=-1581; eloMap[60]=-1761; eloMap[61]=-1943; eloMap[62]=-2126; eloMap[63]=-2311; eloMap[64]=-2499; eloMap[65]=-2688; eloMap[66]=-2881; eloMap[67]=-3076; eloMap[68]=-3274; eloMap[69]=-3475; eloMap[70]=-3680; eloMap[71]=-3889; eloMap[72]=-4102; eloMap[73]=-4320; eloMap[74]=-4543; eloMap[75]=-4771; eloMap[76]=-5006; eloMap[77]=-5248; eloMap[78]=-5497; eloMap[79]=-5754; eloMap[80]=-6021; eloMap[81]=-6297; eloMap[82]=-6585; eloMap[83]=-6886; eloMap[84]=-7202; eloMap[85]=-7533; eloMap[86]=-7884; eloMap[87]=-8256; eloMap[88]=-8653; eloMap[89]=-9080; eloMap[90]=-9542; eloMap[91]=-10048; eloMap[92]=-10607; eloMap[93]=-11234; eloMap[94]=-11950; eloMap[95]=-12788; eloMap[96]=-13802; eloMap[97]=-15097; eloMap[98]=-16902; eloMap[99]=-19956;
	overallScore = 0;
	subjectEq.op = 1; topicEq.op = 2; ruleEq.op = 3; idEq.op = 0; minEq.op = 4;
	

	firstCorrect = false;
	auto t1 = std::chrono::high_resolution_clock::now();
	ridx = 0;
	makeRules("rules/derivatives.csv");
	
	std::ifstream file1("cpp/subjects/prealgebra.csv"); //file just has some sentences
	if (!file1) {
		std::cout << "unable to open file";
	}
	std::string row;
	std::vector<std::string> rows;
	while (getline(file1, row)) {
		rows.push_back(row);
	}
	makeRulesNew(rows);
	
	std::ifstream file2("cpp/subjects/precalculus.csv"); //file just has some sentences
	if (!file2) {
		std::cout << "unable to open file";
	}
	rows.resize(0);
	while (getline(file2, row)) {
		rows.push_back(row);
	}
	makeRulesNew(rows);
	

	makeRules("subjects/algebraold.csv");
	
	std::ifstream file3("cpp/subjects/calculus.csv"); //file just has some sentences
	if (!file3) {
		std::cout << "unable to open file";
	}
	rows.resize(0);
	while (getline(file3, row)) {
		rows.push_back(row);
	}
	makeRulesNew(rows);
	
	auto t2 = std::chrono::high_resolution_clock::now();
}