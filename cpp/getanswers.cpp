#include <nan.h>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <math.h>
#include <limits.h>
#include <time.h>
#include <string.h> 
#include <ctype.h>
#include <cmath>
#include <iostream>
#include <fstream>
#include <variant>
#include <map>
#include <numeric>
#include <chrono>
#include <thread>
#include <sstream>
#include <array>
#include <vector>
#include <unistd.h>
#include <thread>
#include <future>
#include "rapidcsv.h"
#include "ctpl/ctpl_stl.h"
#include "parallel_hashmap/phmap.h"


using namespace std::chrono;
using phmap::flat_hash_map;

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

#include "solve.cpp"

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

std::vector<std::string> outputTree(std::string pfstr){
	std::vector<std::string> treeOptions;
	flat_hash_map<std::string,std::vector<std::string>> listMap;
	flat_hash_map<int,std::string> operandMap;
	flat_hash_map<int,std::string> originalMap;
	std::vector<std::string> finalList;
	std::vector<std::string> orderedKeyList;
	flat_hash_map<std::string,std::vector<std::string>> nodeList;
	
    
    
	int i; int ii; int iii;
	int idx =0;
	bool startOperands = false;
	std::string currentOperator = "";
	int iidx = 0;
	bool midBrackets = false;
	for (i=0;i<pfstr.length();i++){
		if (pfstr.at(i) == '@'){
			startOperands = true;
		}
		else if (startOperands && !midBrackets){
			if (pfstr.at(i) == '_'){
				originalMap[iidx] = currentOperator;
				iidx++; 
				currentOperator = "";
			}
			else if (pfstr.at(i) == '{'){
				midBrackets = true;
				currentOperator += pfstr.at(i);
			}
			else {
				currentOperator += pfstr.at(i);
			}
		}
		else if (startOperands && midBrackets){
			if (pfstr.at(i) == '}'){
				midBrackets = false;
				currentOperator += pfstr.at(i);
			}
			else {
				currentOperator += pfstr.at(i);
			}
		}
	}
	

    
    
    
	int treeIdx = 0;
	//std::cout << "before third: " << pfstr << "\n";

	for (i=0;i<pfstr.length();i++){
		
		if (pfstr.at(i) == '@'){
			break;
		}
		else if (pfstr.at(i) != '#'){
			std::string secondStr = "";
			std::string secondTtr = "";
			
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
					maxi = ii;
					break;
				}
			}
			std::string firstStr = "";
			std::string firstTtr = "";
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
						break;
					}
				}
				
				
			}

			std::string fullStr = firstStr + secondStr + pfstr.at(i) + '@' + firstTtr + secondTtr;
			
			
			//Parent Node
			std::string opStr = "";
			opStr += pfstr.at(i);
			std::string name = "node"+std::to_string(treeIdx);
			treeIdx++;
			std::string parent = "";
			std::string nodeText = fullStr;
			std::string pname = name;
			nodeList[fullStr]={pname,parent,opStr};
			
			
			//Child 1
			nodeText = secondStr + '@' + secondTtr;
			if (nodeList.find(nodeText) != nodeList.end()){
				
				if (secondStr.at(secondStr.length()-1) == pfstr.at(i) && ( pfstr.at(i) == '+' || pfstr.at(i) == '*') ){
					std::vector<std::string> revList;
					for (flat_hash_map<std::string,std::vector<std::string>>::iterator iter = nodeList.begin(); iter != nodeList.end(); ++iter){
						if (iter->second[1] == nodeList[nodeText][0]){
							nodeList[iter->first][1] = pname;
							revList.push_back(iter->first);
						}
					}
					int okSz = orderedKeyList.size();
					for (ii=0;ii<okSz;ii++){
						for (iii=revList.size()-1;iii>=0;iii--){
							if (orderedKeyList[ii] == revList[iii]){
								orderedKeyList.push_back(revList[iii]);
							}
						}
					}
					
				}
				else {
					nodeList[nodeText][1] = pname;
					orderedKeyList.push_back(nodeText);
				}
				
			}
			else {
				name = "node"+std::to_string(treeIdx);
				treeIdx++;
				if (secondStr.at(secondStr.length()-1) == pfstr.at(i) && ( pfstr.at(i) == '+' || pfstr.at(i) == '*')){
					std::vector<std::string> revList;
					for (flat_hash_map<std::string,std::vector<std::string>>::iterator iter = nodeList.begin(); iter != nodeList.end(); ++iter){
						if (iter->second[1] == name){
							nodeList[iter->first][1] = pname;
							revList.push_back(iter->first);
						}
					}
					int okSz = orderedKeyList.size();
					for (ii=0;ii<okSz;ii++){
						for (iii=revList.size()-1;iii>=0;iii--){
							if (orderedKeyList[ii] == revList[iii]){
								orderedKeyList.push_back(revList[iii]);
							}
						}
					}
				}
				else {
					nodeList[nodeText] = {name,pname,opStr};
					orderedKeyList.push_back(nodeText);
				}
				
			}
			
			if (firstStr.length() > 0){
				//Child 2
				nodeText = firstStr + '@' + firstTtr;
				if (nodeList.find(nodeText) != nodeList.end()){
					if (firstStr.at(firstStr.length()-1) == pfstr.at(i) && ( pfstr.at(i) == '+' || pfstr.at(i) == '*')){
						std::vector<std::string> revList;
						for (flat_hash_map<std::string,std::vector<std::string>>::iterator iter = nodeList.begin(); iter != nodeList.end(); ++iter){
							if (iter->second[1] == nodeList[nodeText][0]){
								nodeList[iter->first][1] = pname;
								revList.push_back(iter->first);
							}
						}
						int okSz = orderedKeyList.size();
						for (ii=0;ii<okSz;ii++){
							for (iii=revList.size()-1;iii>=0;iii--){
								if (orderedKeyList[ii] == revList[iii]){
									orderedKeyList.push_back(revList[iii]);
								}
							}
						}
					}
					else {
						nodeList[nodeText][1] = pname;
						orderedKeyList.push_back(nodeText);
					}
				
				}
				else {
					name = "node"+std::to_string(treeIdx);
					treeIdx++;
					if (firstStr.at(firstStr.length()-1) == pfstr.at(i) && ( pfstr.at(i) == '+' || pfstr.at(i) == '*')){
						std::vector<std::string> revList;
						for (flat_hash_map<std::string,std::vector<std::string>>::iterator iter = nodeList.begin(); iter != nodeList.end(); ++iter){
							if (iter->second[1] == name){
								nodeList[iter->first][1] = pname;
								revList.push_back(iter->first);
							}
						}
						int okSz = orderedKeyList.size();
						for (ii=0;ii<okSz;ii++){
							for (iii=revList.size()-1;iii>=0;iii--){
								if (orderedKeyList[ii] == revList[iii]){
									orderedKeyList.push_back(revList[iii]);
								}
							}
						}
					}
					else {
						nodeList[nodeText] = {name,pname,opStr};
						orderedKeyList.push_back(nodeText);
					}
				
				}
				
			}
			orderedKeyList.push_back(fullStr);
			

			
			listMap[fullStr]={"#","_"};
			
		}
		else {
			listMap["#@" + std::to_string(idx) + "_"]={"#","_"};
			operandMap[i]=std::to_string(idx);
			
			std::string name = "node"+std::to_string(treeIdx);
			treeIdx++;
			nodeList["#@" + std::to_string(idx) + "_"] = {name,"","#"};
			orderedKeyList.push_back("#@" + std::to_string(idx) + "_");
			idx++;
		}
		
	}
		
	
	//std::cout << "\n\n---start Original-----\n";
	int iiii;
	
	//for (flat_hash_map<int,std::string>::iterator iter = originalMap.begin(); iter != originalMap.end(); ++iter){
	//	std::cout << iter->first << " and " << iter->second << '\n';
	//}
	

	//std::cout << " ENd bracketless\n";
	//for (flat_hash_map<int,std::string>::iterator iter = bracketlessMap.begin(); iter != bracketlessMap.end(); ++iter){
	//	std::cout << iter->first << " and " << iter->second << '\n';
	//}
	
	flat_hash_map<std::string,std::string> skipList;
	jsonmessage += "-DOJS-\nnodes = {};\n";
	std::string nodeString = "allNodes = [";
	//std::cout << "-DOJS-\nnodes = {};\n";
	
	std::vector<std::string> forLatex;
	
	for (ii=orderedKeyList.size()-1;ii>=0;ii--){
		//std::cout << "anything: " << orderedKeyList[ii] << " and node: " << nodeList[orderedKeyList[ii]][0] << "\n";
		if (skipList.find(orderedKeyList[ii]) != skipList.end()){
			//std::cout << "skip: " << nodeList[orderedKeyList[ii]][0] << "\n";
			continue;
		}
		else {
			skipList[orderedKeyList[ii]] = "";
		}
		
		std::string name = nodeList[orderedKeyList[ii]][0];
		std::string parent = nodeList[orderedKeyList[ii]][1];
		std::string postfix = fromOriginal(orderedKeyList[ii],originalMap);
		forLatex.push_back(name);
		forLatex.push_back(parent);
		forLatex.push_back(postfix);
		
		
	}
	flat_hash_map<std::string,std::string> latexMap =toLatex(forLatex);
	
	
	skipList.clear();
	for (ii=orderedKeyList.size()-1;ii>=0;ii--){
		if (skipList.find(orderedKeyList[ii]) != skipList.end()){
			//std::cout << "skip: " << nodeList[orderedKeyList[ii]][0] << "\n";
			continue;
		}
		else {
			skipList[orderedKeyList[ii]] = "";
		}
		
		std::string name = nodeList[orderedKeyList[ii]][0];
		std::string parent = nodeList[orderedKeyList[ii]][1];
		std::string postfix = fromOriginal(orderedKeyList[ii],originalMap);

		if (latexMap.find(name) != latexMap.end()){
			std::string outText = "nodes[\""+name + "\"] = {text:";
			outText += "\"" + latexMap[name] + "\",";
			outText += "op: \"" + nodeList[orderedKeyList[ii]][2] + "\",";
			outText += "parent: \""+ parent + "\"};\n";
		
			jsonmessage += outText + "\n";
			//std::cout << outText << "\n";
			nodeString += "\""+nodeList[orderedKeyList[ii]][0] + "\", ";
		}
		
		
	}
	
	nodeString += "];\n";
	jsonmessage += nodeString + "\n";
	//std::cout <<  nodeString << "\n";
	jsonmessage += "trees.push({nodes:nodes,allNodes:allNodes});\n-ODJS-\n";
	//std::cout << "trees.push({nodes:nodes,allNodes:allNodes});\n-ODJS-\n";
	
	//for (flat_hash_map<int,std::string>::iterator iter = bracketlessMap.begin(); iter != bracketlessMap.end(); ++iter){
	//	std::cout << iter->first << " and " << iter->second << '\n';
	//}
	
	//std::cout << "\n\n----End bracketless----\n";
	
	
	//for (flat_hash_map<int,std::string>::iterator iter = bracketlessMap.begin(); iter != bracketlessMap.end(); ++iter){
	//	std::cout << iter->first << " bracketless " << iter->second << '\n';
	//}
	//std::cout << '\n';
	return treeOptions;
}


#include "postfixify.cpp"

#include "makerules.cpp"

#include "makeanswers.cpp"

#include "applyrules.cpp"

#include "makenumbers.cpp"



void initialRun(){
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
	prec[-94] = 2;
	prec['&'] = 1;
	prec['|'] = 0;
	prec['('] = -1;
	prec[')'] = -1;
	eloMap[1]=19956; eloMap[2]=16902; eloMap[3]=15097; eloMap[4]=13802; eloMap[5]=12788; eloMap[6]=11950; eloMap[7]=11234; eloMap[8]=10607; eloMap[9]=10048; eloMap[10]=9542; eloMap[11]=9080; eloMap[12]=8653; eloMap[13]=8256; eloMap[14]=7884; eloMap[15]=7533; eloMap[16]=7202; eloMap[17]=6886; eloMap[18]=6585; eloMap[19]=6297; eloMap[20]=6021; eloMap[21]=5754; eloMap[22]=5497; eloMap[23]=5248; eloMap[24]=5006; eloMap[25]=4771; eloMap[26]=4543; eloMap[27]=4320; eloMap[28]=4102; eloMap[29]=3889; eloMap[30]=3680; eloMap[31]=3475; eloMap[32]=3274; eloMap[33]=3076; eloMap[34]=2881; eloMap[35]=2688; eloMap[36]=2499; eloMap[37]=2311; eloMap[38]=2126; eloMap[39]=1943; eloMap[40]=1761; eloMap[41]=1581; eloMap[42]=1402; eloMap[43]=1224; eloMap[44]=1047; eloMap[45]=872; eloMap[46]=696; eloMap[47]=522; eloMap[48]=348; eloMap[49]=174; eloMap[50]=0; eloMap[51]=-174; eloMap[52]=-348; eloMap[53]=-522; eloMap[54]=-696; eloMap[55]=-872; eloMap[56]=-1047; eloMap[57]=-1224; eloMap[58]=-1402; eloMap[59]=-1581; eloMap[60]=-1761; eloMap[61]=-1943; eloMap[62]=-2126; eloMap[63]=-2311; eloMap[64]=-2499; eloMap[65]=-2688; eloMap[66]=-2881; eloMap[67]=-3076; eloMap[68]=-3274; eloMap[69]=-3475; eloMap[70]=-3680; eloMap[71]=-3889; eloMap[72]=-4102; eloMap[73]=-4320; eloMap[74]=-4543; eloMap[75]=-4771; eloMap[76]=-5006; eloMap[77]=-5248; eloMap[78]=-5497; eloMap[79]=-5754; eloMap[80]=-6021; eloMap[81]=-6297; eloMap[82]=-6585; eloMap[83]=-6886; eloMap[84]=-7202; eloMap[85]=-7533; eloMap[86]=-7884; eloMap[87]=-8256; eloMap[88]=-8653; eloMap[89]=-9080; eloMap[90]=-9542; eloMap[91]=-10048; eloMap[92]=-10607; eloMap[93]=-11234; eloMap[94]=-11950; eloMap[95]=-12788; eloMap[96]=-13802; eloMap[97]=-15097; eloMap[98]=-16902; eloMap[99]=-19956;
	overallScore = 0;
	subjectEq.op = 1; topicEq.op = 2; ruleEq.op = 3; idEq.op = 0; minEq.op = 4;
	

	auto t1 = std::chrono::high_resolution_clock::now();
	ridx = 0;
	makeRules("rules/derivatives.csv");
	makeRules("subjects/prealgebra.csv");
	makeRules("subjects/algebra.csv");
	
	auto t2 = std::chrono::high_resolution_clock::now();
}


flat_hash_map<std::string,Answer> answerMap;
int maxFound;
int maxSteps;



#include "autocomplete.cpp"




void Hello(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	//v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	//v8::String::Utf8Value s(isolate, info[0]);
	//std::string str(*s);
	jsonmessage = "var rule = {};";
	srand(time(NULL));
	initialRun();
	
	//makeInt("[10,12)U((0,5)U[4,6]U(8,10])");
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(jsonmessage);
	info.GetReturnValue().Set(h.ToLocalChecked());
}


int eloToProb(int elo){
	int pyes; int ei;
	for (ei=1;ei<99;ei++){
		int m = (eloMap[ei]+eloMap[ei+1])/2;
		if (elo > m){
			pyes = ei;
			break;
		}
		if (ei == 98){
			pyes = 99;
		}
	}
	return pyes;
}
int probCorrect(){
	long probc = 1;
	long probt = 2;
	int ii; int iii;
	for (flat_hash_map<std::string,Answer>::iterator iter = answerMap.begin(); iter != answerMap.end(); ++iter){
		if (iter->second.correct && iter->second.finished){
			int p = 100;
			std::vector<Step> v;
			v = iter->second.solution;
			for (iii=0;iii<v.size();iii++){
				if (v[iii].rule >= 0){
					int pp = ruleIndex[v[iii].rule].score;
					p *= eloToProb(-1*pp);
					p /= 50;
				}
			}
			probc += p;
			probt += p;
		}
		if (!iter->second.correct && iter->second.finished){
			int p = 100;
			std::vector<Step> v;
			v = iter->second.solution;
			for (iii=0;iii<v.size();iii++){
				if (v[iii].rule >= 0){
					int pp = ruleIndex[v[iii].rule].score;
					p *= eloToProb(-1*pp);
					p /= 50;
				}
			}
			probt += p;
		}
	}
	return probc*10000/probt;
}

flat_hash_map<std::string,std::vector<int>> answerListMapF;

void MakeAnswers(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string a(*s);
	std::cout << "your question: " << a << "\n";
	

	rapidcsv::Document doc("testanswer.txt", rapidcsv::LabelParams(-1, -1));
	
	int nRows = doc.GetRowCount();
	int i; int ii;
	
	std::cout << "Rows: " << nRows << "\n";
	std::string q;
	if (nRows>0){
		std::vector<std::string> rawQ = doc.GetRow<std::string>(0);
		q = rawQ[0];
	}
	for (i=2;i<nRows;i++){
		if (i%2 == 0){
			std::vector<std::string> rawAnswer = doc.GetRow<std::string>(i);
			if (rawAnswer.size()< 3){
				continue;
			}
			std::string key = rawAnswer[0];
			Answer answer;
			answer.input = rawAnswer[1];
			if (rawAnswer[2] =="c"){
				answer.correct = true;
				answer.finished = true;
			}
			else if (rawAnswer[2] =="e"){
				answer.correct = false;
				answer.finished = true;
			}
			else if (rawAnswer[2] =="u"){
				answer.correct = false;
				answer.finished = false;
			}
			answer.solution.resize(0);
			for (ii=3;ii<rawAnswer.size();ii++){
				if (ii%2 == 0){
					Step step;
					step.next = rawAnswer[ii-1];
					step.rule = std::stoi(rawAnswer[ii]);
					answer.solution.push_back(step);
				}
			}
			answerMap[key]=answer;
		}
		else {
			std::vector<std::string> rawAnswer = doc.GetRow<std::string>(i);
			if (rawAnswer.size()< 1){
				continue;
			}
			std::string key = rawAnswer[0];
			std::vector<int> ruleOpps;
			for (ii=1;ii<rawAnswer.size();ii++){
				if (rawAnswer[ii]==""){
					break;
				}
				ruleOpps.push_back(std::stoi(rawAnswer[ii]));
			}
			answerListMapF[key]=ruleOpps;
		}
		
		
	}

	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(q);

	
	info.GetReturnValue().Set(h.ToLocalChecked());
}

void CheckAnswer(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string a(*s);

	std::string mpf = postfixify(a);
	std::cout << "your answer: " << mpf << "\n";
	int ii; int iii; int iiii;
	
	auto a1 = std::chrono::high_resolution_clock::now();



	if (answerMap.find(mpf) != answerMap.end()){
		Answer userAnswer = answerMap[mpf];
		std::cout << "correct? " << userAnswer.correct <<"\n";
		std::cout << "finished? " << userAnswer.finished <<"\n";
	
	

		flat_hash_map<int,std::vector<int>> branches;
		flat_hash_map<int,std::vector<bool>> userData;
		for (ii=0;ii<ridx;ii++){
			userData[ii]={false,false};
		}
		std::vector<Step> v;
		v = userAnswer.solution;

		flat_hash_map<int,bool> alreadyApp;
		flat_hash_map<int,bool> alreadyOpp;
		for (iii=0;iii<v.size();iii++){
			if (answerListMapF.find(v[iii].next)== answerListMapF.end()){
				std::cout << "missing??????\n";
				continue;
			}
			if (alreadyApp.find(v[iii].rule) != alreadyApp.end()){
			}
			else {
				//TODO: make the rule match reality
				if (v[iii].rule >= 0){
					userData[v[iii].rule][0]=true;
				}
				alreadyApp[v[iii].rule]=true;
			}
			std::vector<int> allOptions = answerListMapF[v[iii].next];
			for (iiii=0;iiii<allOptions.size();iiii++){
				if (alreadyOpp.find(allOptions[iiii]) != alreadyOpp.end()){
					continue;
				}
				else {
					userData[allOptions[iiii]][1]=true;
					alreadyOpp[allOptions[iiii]]=true;
				}
			}
		}
		int apc = probCorrect();
	
		for (ii=0;ii<ridx;ii++){
			if (userData[ii][1]){
				branches[ii]={0,0};
			}
		}


		for (flat_hash_map<std::string,Answer>::iterator iter = answerMap.begin(); iter != answerMap.end(); ++iter){
			if (iter->second.finished){
				std::vector<Step> v = iter->second.solution;
		
				flat_hash_map<int,bool> alreadyApp;
				flat_hash_map<int,bool> alreadyOpp;
				for (iii=0;iii<v.size();iii++){
					if (answerListMapF.find(v[iii].next)== answerListMapF.end()){
						std::cout << "missing??????222222\n";
						continue;
					}
					if (branches.find(v[iii].rule) != branches.end()){
						if (alreadyApp.find(v[iii].rule) != alreadyApp.end()){
						}
						else {
							//TODO: make the rule match reality
							if (v[iii].rule >= 0){
								branches[v[iii].rule][0]++;
							}
							alreadyApp[v[iii].rule]=true;
						}
					}
					std::vector<int> allOptions = answerListMapF[v[iii].next];
					for (iiii=0;iiii<allOptions.size();iiii++){
						if (branches.find(allOptions[iiii]) != branches.end()){
							if (alreadyOpp.find(allOptions[iiii]) != alreadyOpp.end()){
								continue;
							}
							else {
								branches[allOptions[iiii]][1]++;
								alreadyOpp[allOptions[iiii]]=true;
							}
						}
					}
				}
			}
		}
		for (flat_hash_map<int,std::vector<int>>::iterator iter = branches.begin(); iter != branches.end(); ++iter){
			int rr = (branches[iter->first][0]*2 + 1)*100/(branches[iter->first][1]*2+2);

			if (rr < 1){
				rr = 1;
			}
			if (rr > 99){
				rr = 99;
			}
			int r = eloMap[rr];
			//std::cout << iter->first << " and " << branches[iter->first][0] << " and "<< branches[iter->first][1] << " and " << r << "\n";
			//std::cout << iter->first << " and " << userData[iter->first][0] << " and "<< userData[iter->first][1] << "\n";
			int score = ruleIndex[iter->first].score;
			int d = r - score;
			int ei;
			int pyes = eloToProb(d);
			int pno = eloToProb(-1*d);
			int k = ruleIndex[iter->first].k;
			if (userData[iter->first][0]){
				ruleIndex[iter->first].score = score + k*pno/100;
			}
			else{
				ruleIndex[iter->first].score = score - k*pyes/100;
			}
			if (k>100){
				ruleIndex[iter->first].k -= 4;
			}
			 
			//std::cout << iter->first << " new score: " << ruleIndex[iter->first].score << " and pyes:" << pyes << "\n";
		}
		int ppc = probCorrect();
	
		int aelo;
		if (apc <= 100){
			aelo = eloMap[1];
		}
		else if (apc >= 9900){
			aelo = eloMap[99];
		}
		else {
			aelo = eloMap[apc/100]*(100-(apc%100))+eloMap[apc/100+1]*(apc%100);
			aelo /= 100;
		}
		int pelo;
		if (ppc <= 100){
			pelo = eloMap[1];
		}
		else if (ppc >= 9900){
			pelo = eloMap[99];
		}
		else {
			pelo = eloMap[ppc/100]*(100-(ppc%100))+eloMap[ppc/100+1]*(ppc%100);
			pelo /= 100;
		}
		overallScore += aelo - pelo;

		std::cout << " apc: " << apc << " ppc: " << ppc << " ovscore: " << overallScore << "\n";

	}
	else {
		std::cout << "unknown answer" << "\n";
	}
	
	
	auto a2 = std::chrono::high_resolution_clock::now();
	std::cout << "grade time: " << std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count() << "\n";

	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(a);

	
	info.GetReturnValue().Set(h.ToLocalChecked());
}

void AutoAnswer(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string a(*s);
	
	
	auto a1 = std::chrono::high_resolution_clock::now();
	std::string newPostfix = "#@0_";
	std::vector<std::string> autoAnswers = autocomplete(newPostfix,a);
	auto a2 = std::chrono::high_resolution_clock::now();
	std::string jsonmessage = "outArray = [];\n";
	std::cout << "autocomplete time: " << std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count()  << "\n";
	int i;
	for (i=0;i<autoAnswers.size();i++){
		//std::cout << autoAnswers[i] << "\n";
		if (answerMap.find(autoAnswers[i]) != answerMap.end()){
			jsonmessage += "outArray.push({latex:\""+latexOne(autoAnswers[i])+"\",input:\""+answerMap[autoAnswers[i]].input+"\"});\n";
		}
		
	}
	

	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(jsonmessage);

	
	info.GetReturnValue().Set(h.ToLocalChecked());
}

void GetSolution(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string a(*s);
	
	std::string pfstr = postfixify(a);
	int i; int ii;
	
	std::vector<Step> bestSolution;
	bool foundSolution = false;
	
	for (flat_hash_map<std::string,Answer>::iterator iter = answerMap.begin(); iter != answerMap.end(); ++iter){

		if (iter->first == pfstr && iter->second.correct && iter->second.finished){
			std::cout << "match: " << pfstr << " and " << iter->first << "\n";
			bestSolution = iter->second.solution;
			foundSolution = true;
			break;
		}
		else if (iter->second.correct && iter->second.finished){
			
			std::vector<Step> v = iter->second.solution;
			if (v.size()<bestSolution.size() || bestSolution.size() == 0){
				bestSolution = v;
			}
		}
	}
	jsonmessage = "";
	
	while (!foundSolution){
		foundSolution = true;
		std::vector<Step> oldBest = bestSolution;
		bestSolution.resize(0);
		for (flat_hash_map<std::string,Answer>::iterator iter = answerMap.begin(); iter != answerMap.end(); ++iter){
			if (iter->second.correct && iter->second.finished){
				std::vector<Step> v = iter->second.solution;
				for (ii=0;ii<v.size();ii++){
					if (ii>=oldBest.size()){
						if (v.size()<bestSolution.size() || bestSolution.size() == 0){
							bestSolution = v;
							foundSolution = false;
						}
					
						break;
					}
					if (v[ii].next != oldBest[ii].next){
						break;
					}
					//std::cout << "step: " << v[ii] << "\n";
					//outputTree(v[ii]);
				}
			}
		}
		if (foundSolution){
			bestSolution = oldBest;
		}
	}
	
	for (i=0;i<bestSolution.size();i++){
		std::cout << "bs: " << bestSolution[i].next << "\n";
		std::cout << "bsr: " << bestSolution[i].rule << "\n";
		outputTree(bestSolution[i].next);
	}
	
	
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(jsonmessage);

	
	info.GetReturnValue().Set(h.ToLocalChecked());
}


void Init(v8::Local<v8::Object> exports) {
  v8::Local<v8::Context> context = exports->CreationContext();
  exports->Set(context,
               Nan::New("hello").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(Hello)
                   ->GetFunction(context)
                   .ToLocalChecked());
  exports->Set(context,
               Nan::New("check").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(CheckAnswer)
                   ->GetFunction(context)
                   .ToLocalChecked());
  exports->Set(context,
               Nan::New("auto").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(AutoAnswer)
                   ->GetFunction(context)
                   .ToLocalChecked());
  exports->Set(context,
               Nan::New("solution").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(GetSolution)
                   ->GetFunction(context)
                   .ToLocalChecked());
  exports->Set(context,
               Nan::New("makeanswers").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(MakeAnswers)
                   ->GetFunction(context)
                   .ToLocalChecked());


}

NODE_MODULE(helloarray, Init)