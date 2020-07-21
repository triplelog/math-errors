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

#include "rapidcsv.h"
#include "parallel_hashmap/phmap.h"


using namespace std::chrono;
using phmap::flat_hash_map;

std::vector<std::string> applyRulesVectorOnePart(std::string onePart,std::vector<int> oneIndex, std::string userFullString, bool isCorrect);

flat_hash_map<char,int> prec;
flat_hash_map<std::string,std::vector<std::vector<std::string>>> rules;
//flat_hash_map<std::string,std::vector<std::string>> allListMapFull;
//flat_hash_map<std::string,std::vector<std::vector<std::string>>> allListMapBottom;
flat_hash_map<std::string,bool> constraintMap;
std::vector<std::string> bottomTreesString;
std::vector<std::vector<int>> bottomTreesIndex;
int btSz;
std::string jsonmessage;
int duration1;
int duration2;
int duration3;
int yesC;
int noC;
int mapSave;
int mapMake;

		
std::string arrayToString(int n, char input[]) { 
    int i; 
    std::string s = ""; 
    for (i = 0; i < n; i++) { 
        s = s + input[i]; 
    } 
    return s; 
}

std::string addTwoInts(std::string a, std::string b){
	std::string revsum = "";
	int base = 10;
	if (b.length() > a.length()){
		std::string c = a;
		a = b;
		b = c;
	}
	int len = a.length();
	while (len > b.length()){
		b = "0"+b;
	}
	int i;
	int charSum =0;
	int carry = 0;
	for (i=0;i<a.length();i++){
		int aa = a.at(len-1-i) - '0';
		if (aa<0 || aa>9){
			return "false";
		}
		int bb = b.at(len-1-i) - '0';
		if (bb<0 || bb>9){
			return "false";
		}
		charSum = aa + bb + carry;
		carry = 0;
		while (charSum >= base){
			charSum -= base;
			carry++;
		}
		revsum += std::to_string(charSum);
	}
	while (carry > 0){
		charSum = carry;
		carry = 0;
		while (charSum >= base){
			charSum -= base;
			carry++;
		}
		revsum += std::to_string(charSum);
	}
	std::string sum = "";
	for (i=revsum.length()-1;i>=0;i--){
		sum += revsum.at(i);
	}
	return sum;
}

std::string mulTwoInts(std::string a, std::string b){
	int base = 10;
	if (b.length() > a.length()){
		std::string c = a;
		a = b;
		b = c;
	}
	int len = a.length();
	while (len > b.length()){
		b = "0"+b;
	}
	int i;
	for (i=0;i<a.length();i++){
		int aa = a.at(len-1-i) - '0';
		if (aa<0 || aa>9){
			return "false";
		}
		int bb = b.at(len-1-i) - '0';
		if (bb<0 || bb>9){
			return "false";
		}
	}
	int prod = std::stoi(a);
	prod *= std::stoi(b);
	return std::to_string(prod);
}

std::string divTwoInts(std::string a, std::string b){
	int base = 10;
	int i;
	int len = a.length();
	for (i=0;i<len;i++){
		int aa = a.at(len-1-i) - '0';
		if (aa<0 || aa>9){
			return "false";
		}
	}
	len = b.length();
	for (i=0;i<len;i++){
		int bb = b.at(len-1-i) - '0';
		if (bb<0 || bb>9){
			return "false";
		}
	}
	int div = std::stoi(a);
	int divb = std::stoi(b);
	if (div % divb == 0){
		div /= divb;
	}
	else {
		return "false";
	}
	return std::to_string(div);
}

std::string subTwoInts(std::string a, std::string b){
	int base = 10;
	int i;
	int len = a.length();
	for (i=0;i<len;i++){
		int aa = a.at(len-1-i) - '0';
		if (aa<0 || aa>9){
			return "false";
		}
	}
	len = b.length();
	for (i=0;i<len;i++){
		int bb = b.at(len-1-i) - '0';
		if (bb<0 || bb>9){
			return "false";
		}
	}
	int div = std::stoi(a);
	div -= std::stoi(b);
	return std::to_string(div);
}

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

std::vector<std::string> makePostVector(char infixexpr[]) {
	
	std::string intstr = "";
	std::string expstr = "";
	char topToken;
	std::vector<std::string> postfixList;
	int pfidx =0;
	std::vector<char> opStack;
	int osidx = 0;
	std::vector<std::string> tokenList;
	int idx = 0;
	int len=0;
	int i;
	for (i = 0; infixexpr[i]; i++) 
    {
    	len = i+1;
    }
	char temptoken[len];
	tokenList.resize(len);
	postfixList.resize(len);
	opStack.resize(len);
	int iidx = 0;
	
	
	
	for (i = 0; infixexpr[i]; i++) 
    {
		char ie = infixexpr[i];
		if (prec.find(ie) == prec.end()){
			temptoken[iidx] = ie;
			temptoken[iidx+1] = '\0';
			iidx++;
		}
		else{
			if (iidx != 0){
				tokenList[idx] = arrayToString(iidx,temptoken);
				idx++;
			}
			std::string s(1,ie);
			tokenList[idx] = s;
			idx++;
			temptoken[0] = '\0';
			iidx=0;
		}
	}
	if (iidx != 0){
		tokenList[idx] = arrayToString(iidx,temptoken);
		idx++;
	}
	
	tokenList.resize(idx);
	
	
	for (i=0;i<idx;i++){
		std::string token = tokenList[i];
		char firstChar = token.at(0);
		if (firstChar == '('){
			opStack[osidx] = firstChar;
			osidx++;
		}
		else if (firstChar == ')'){
			topToken = opStack[osidx-1];
			osidx--;
			
			while (topToken != '('){
				std::string s(1,topToken);
				postfixList[pfidx] = s;
				pfidx++;
				topToken = opStack[osidx-1];
				osidx--;
			}
		}
		else if (firstChar < 0 || firstChar == '^' || firstChar == '*' || firstChar == '+' || firstChar == '/' || firstChar == '-' || firstChar == '>' || firstChar == '<' || firstChar == '=' || firstChar == '!' || firstChar == '[' || firstChar == ']' || firstChar == '&' || firstChar == '|') {
			while ((osidx > 0) && (prec[opStack[osidx-1]] >= prec[firstChar])){
				topToken = opStack[osidx-1];
				osidx--;
				std::string s(1,topToken);
				postfixList[pfidx] = s;
				pfidx++;
			}
			opStack[osidx] = firstChar;
			osidx++;
		}
		else {
			postfixList[pfidx] = token;
			pfidx++;
		}
	}
	while (osidx > 0){
		topToken = opStack[osidx-1];
		osidx--;
		std::string s(1,topToken);
		postfixList[pfidx] = s;
		pfidx++;
	}
	

	for (i=0;i<pfidx;i++){
		
		std::string ci = postfixList[i];
		char firstChar = ci.at(0);
		if (firstChar == '-'){
			//expstr += "-";
			expstr += "-+";
		}
		else if (firstChar == '/'){
			//expstr += "-";
			expstr += "/*";
		}
		else if (firstChar < 0 || firstChar == '^' || firstChar == '*' || firstChar == '+' || firstChar == '>' || firstChar == '<' || firstChar == '=' || firstChar == '!' || firstChar == '[' || firstChar == ']' || firstChar == '&' || firstChar == '|') {
			expstr += ci;
		}
		else {
			
			if (ci == "pi" || ci == "Pi" || ci == "PI"){
				intstr += "\\\\pi";
			}
			else if (ci == "alpha"){
				intstr += "\\\\alpha";
			}
			else if (ci == "beta"){
				intstr += "\\\\beta";
			}
			else if (ci == "theta"){
				intstr += "\\\\theta";
			}
			else {
				intstr += ci;
			}
			intstr += "_";
			expstr += "#";
		}

	}
	
	return {expstr,intstr};


}

std::string makePost(char infixexpr[]) {
	std::vector<std::string> v = makePostVector(infixexpr);
	
	std::string retstr = v[0]+ "@" + v[1];
	return retstr;


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

flat_hash_map<int,std::string> removeBrackets(flat_hash_map<int,std::string> originalMap) {
	
	flat_hash_map<int,std::string> newMap;
	flat_hash_map<int,std::string> tempMap;
	int nKeys = 0; int count = 0; int originalTotal = 0; int newTotal = 0;
	for (flat_hash_map<int,std::string>::iterator iter = originalMap.begin(); iter != originalMap.end(); ++iter){
		originalTotal++;
		std::string input = iter->second;
		int iii; int iiii;
		bool foundBracket = false;
		for (iii=0;iii<input.length();iii++){
			if (input.at(iii) == '{'){
				foundBracket = true;
				break;
			}
		}
		if (!foundBracket){
			newMap[iter->first]=input;
			newTotal++;
		}
		else {
			nKeys++;
		}
		
	}
	
	while (nKeys>0 && count < 1000){
		for (flat_hash_map<int,std::string>::iterator iter = originalMap.begin(); iter != originalMap.end(); ++iter){
			if (newMap.find(iter->first) != newMap.end()){
				continue;
			}
			//std::cout << iter->first << " and " << iter->second << '\n';
			std::string input = iter->second;
			if (tempMap.find(iter->first) != tempMap.end()){
				input = tempMap[iter->first];
			}
			std::vector<int> indexes; //start,length,iidx,idx of #
			flat_hash_map<int,int> operandToIndex;
			std::string currentOperand = "";
			int startIndex = 0;
			int idx = 0; int iii; int iiii;
			for (iii=0;iii<input.length();iii++){
				if (input.at(iii) == '#'){
					operandToIndex[idx] = iii;
					idx++;
				}
				else if (input.at(iii) == '@'){
					idx = 0;
				}
				else if (input.at(iii) == '_'){
					idx++;
				}
				else if (input.at(iii) == '{'){
					startIndex = iii;
					currentOperand = "";
				}
				else if (input.at(iii) == '}'){
					indexes.push_back(startIndex+1);
					indexes.push_back(iii-(startIndex+1));
					indexes.push_back(std::stoi(currentOperand));
					indexes.push_back(operandToIndex[idx]);
					currentOperand = "";
				}
				else {
					currentOperand += input.at(iii);
				}
			}
			bool foundBracket = false;
			for (iii=indexes.size()/4-1;iii>=0;iii--){
				std::string repText = originalMap[indexes[iii*4+2]];
				if (newMap.find(indexes[iii*4+2]) != newMap.end()) {
					repText = newMap[indexes[iii*4+2]];
				}
			
				bool foundAt = false;
				for (iiii=0;iiii<repText.length();iiii++){
					if (repText.at(iiii) == '{'){
						foundBracket = true;
						break;
					}
				}
		
			}
			std::string oldInput = input;
			for (iii=indexes.size()/4-1;iii>=0;iii--){
				std::string repText = originalMap[indexes[iii*4+2]];
				if (newMap.find(indexes[iii*4+2]) != newMap.end()) {
					repText = newMap[indexes[iii*4+2]];
				}
			
				std::string secondText = "";
				std::string firstText = "";
				bool foundAt = false;
				for (iiii=0;iiii<repText.length();iiii++){
					if (repText.at(iiii) == '{'){
						break;
					}
					else if (repText.at(iiii) == '@'){
						foundAt = true;
					}
					else if (foundAt){
						secondText += repText.at(iiii);
					}
					else {
						firstText += repText.at(iiii);
					}
				}
				if (!foundBracket){
					input.replace(indexes[iii*4]-1,indexes[iii*4+1]+3,secondText);
					input.replace(indexes[iii*4+3],1,firstText);
					break;
				}
		
			}
			if (!foundBracket){
				tempMap[iter->first]=input;
				foundBracket = false;
				for (iii=0;iii<input.length();iii++){
					if (input.at(iii) == '{'){
						foundBracket = true;
						break;
					}
				}
				if (!foundBracket){
					newMap[iter->first]=input;
					newTotal++;
					nKeys--;
				}
			}
		}
		count++;
	}
	
	/* Check no brackets still around
	for (flat_hash_map<int,std::string>::iterator iter = newMap.begin(); iter != newMap.end(); ++iter){
		newTotal++;
		std::string input = iter->second;
		int iii; int iiii;
		bool foundBracket = false;
		for (iii=0;iii<input.length();iii++){
			if (input.at(iii) == '{'){
				foundBracket = true;
				break;
			}
		}
	}
	*/
	return newMap;
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



std::vector<std::string> makeTree(std::string pfstr){
	flat_hash_map<std::string,std::vector<std::string>> listMap;
	flat_hash_map<int,int> operandMap;
	flat_hash_map<int,std::string> originalMap;
    std::vector<std::string> returnStrings;
    bool isCorrect = true;
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
	
	
	//std::cout << "before third: " << pfstr << "\n";
	bottomTreesString.resize(0);
	bottomTreesIndex.resize(0);
	btSz = 0;
	for (i=0;i<pfstr.length();i++){
		int lmSz = 0;
		for (flat_hash_map<std::string,std::vector<std::string>>::iterator iter = listMap.begin(); iter != listMap.end(); ++iter){
			lmSz+= iter->second.size();
		}
		std::cout << lmSz << "\n";
		char mychar = pfstr.at(i);
		if (mychar == '@'){
			break;
		}
		else if (mychar != '#'){
			
			
			std::vector<std::string> secondS;
			std::vector<std::string> secondT;
			std::vector<std::string> secondSBL;
			std::vector<std::string> secondTBL;
			std::string secondStr = "";
			std::string secondTtr = "";
			std::string secondListMapKey = "";
			
			std::vector<std::string> fullTrees;
			int ftSz = 0;
			bool foundFullTrees = false;
			std::string inStr = "";
			int prevLeftIndex = 0;
			int prevRightOperand = 0;

			
			int maxi = i-1;
			int startLeftIndex = maxi;
			int startRightOperand = 10000;
			int endRightOperand = -1;
			for (ii=0;ii<i;ii++){
				std::string s = "";
				std::string t = "";
				int tempStartRightOperand = 10000;
				int tempEndRightOperand = -1;
				for (iii=ii;iii<i;iii++){
					s += pfstr.at(iii);
					if (pfstr.at(iii) == '#'){
						t += originalMap[operandMap[iii]] + '_';
						if (operandMap[iii]<tempStartRightOperand){
							tempStartRightOperand = operandMap[iii];
						}
						if (operandMap[iii]>tempEndRightOperand){
							tempEndRightOperand = operandMap[iii];
						}
					}
				}
				if (listMap.find(s + '@' + t) != listMap.end()){
					secondStr = s;
					secondTtr = t;
					secondListMapKey = s + "@" + t;
					int lms = listMap[s+'@'+t].size()/5;
					secondS.resize(lms);
					secondT.resize(lms);
					secondSBL.resize(lms);
					secondTBL.resize(lms);
					for (iii=0;iii<lms;iii++){
						secondS[iii]=listMap[s+'@'+t][iii*5];
						secondT[iii]=listMap[s+'@'+t][iii*5+1];
						secondSBL[iii]=listMap[s+'@'+t][iii*5+3];
						secondTBL[iii]=listMap[s+'@'+t][iii*5+4];
					}
					maxi = ii;
					startLeftIndex = ii;
					startRightOperand = tempStartRightOperand;
					endRightOperand = tempEndRightOperand;
					break;
				}
			}
			
			
	

			std::vector<std::string> firstS;
			std::vector<std::string> firstT;
			std::vector<std::string> firstSBL;
			std::vector<std::string> firstTBL;
			std::string firstStr = "";
			std::string firstTtr = "";
			std::string firstListMapKey = "";
	
	
	
			if (mychar != '-' && mychar != '/' && (mychar >= 0 || mychar <= -69 )){ // Is at least binary function
		

				for (ii=0;ii<maxi;ii++){
					std::string s = "";
					std::string t = "";
					int tempStartRightOperand = 10000;
					for (iii=ii;iii<maxi;iii++){
						s += pfstr.at(iii);
						if (pfstr.at(iii) == '#'){
							t += originalMap[operandMap[iii]] + '_';
							if (operandMap[iii]<tempStartRightOperand){
								tempStartRightOperand = operandMap[iii];
							}
						}
					}
					if (listMap.find(s + '@' + t) != listMap.end()){
						firstListMapKey = s + "@" + t;
						firstStr = s;
						firstTtr = t;
						int lms = listMap[s+'@'+t].size()/5;
						firstS.resize(lms);
						firstT.resize(lms);
						firstSBL.resize(lms);
						firstTBL.resize(lms);
						for (iii=0;iii<lms;iii++){
							firstS[iii]=listMap[s+'@'+t][iii*5];
							firstT[iii]=listMap[s+'@'+t][iii*5+1];
							firstSBL[iii]=listMap[s+'@'+t][iii*5+3];
							firstTBL[iii]=listMap[s+'@'+t][iii*5+4];
						}
						startLeftIndex = ii;
						startRightOperand = tempStartRightOperand;
						break;
					}
				}
				
				//bottomTreesString.resize(btSz+secondS.size()*firstS.size()*2);
				//bottomTreesIndex.resize(btSz+secondS.size()*firstS.size()*2);
				fullTrees.resize(ftSz+secondS.size()*firstS.size()*3*5);
				
				int fss = firstS.size();
				int sss = secondS.size();	
				std::string nFirst = "0";
				std::string nSecond = "0";	
				std::cout << "new size: " << fss << " * " << sss << "\n";
				for (ii=0;ii<fss;ii++){
					nFirst = listMap[firstListMapKey][ii*5+2];
					if (nFirst=="4"){
						continue;
					}
					
					auto a2 = std::chrono::high_resolution_clock::now();
					for (iii=0;iii<sss;iii++){
				
						nSecond = listMap[secondListMapKey][iii*5+2];
						if (nSecond=="4"){
							continue;
						}
						
						//2 ms
						
						
						//condensed
						fullTrees[ftSz] = "#";
						ftSz++;

						std::string bless = firstSBL[ii] + secondSBL[iii] + pfstr.at(i) + '@' + firstTBL[ii] + secondTBL[iii];

					
						fullTrees[ftSz] = "{"+bless+"}_";
						ftSz++;
						if (nSecond=="2" || nFirst=="2"){
							fullTrees[ftSz] = "2";
							ftSz++;
						}
						else if (nSecond=="1" || nFirst=="1"){
							fullTrees[ftSz] = "1";
							ftSz++;
						}
						else {
							fullTrees[ftSz] = "0";
							ftSz++;
						}
						fullTrees[ftSz] = firstSBL[ii] + secondSBL[iii] + pfstr.at(i);
						ftSz++;
						fullTrees[ftSz] = firstTBL[ii] + secondTBL[iii];
						ftSz++;
						
						//50 ms to here from recent continue
						
				
						//std::cout << "possible part: " << firstS[ii] + secondS[iii] + pfstr.at(i) + '@' + firstT[ii] + secondT[iii] << " and " << startLeftIndex << " and " << startRightOperand << " and " << endRightOperand << " from " << pfstr << "\n";
						
						
						std::string tempFull = pfstr;
						int iiiii; int operandIdx = -1; int startRightIndex = -1; int rightLength= 0;
				
						for (iiiii=0;iiiii<tempFull.length();iiiii++){
							if (tempFull.at(iiiii) == '_'){
								operandIdx++;
								if (operandIdx <=endRightOperand){
									rightLength++;
								}
								else {
									break;
								}
							}
							else if (tempFull.at(iiiii) == '@'){
								operandIdx++;
							}
							else if (operandIdx==startRightOperand && startRightIndex<0){
								startRightIndex = iiiii;
								rightLength = 1;
							}
							else{
								rightLength++;
							}
						}
						
						
				
						
						std::vector<int> tempV;
						tempV = {startLeftIndex,i+1-startLeftIndex,startRightIndex,rightLength};
						
						
						
						//bottomTreesString[btSz]= firstS[ii] + secondS[iii] + pfstr.at(i) + '@' + firstT[ii] + secondT[iii];
						//bottomTreesIndex[btSz]= tempV;
						//btSz++;
						std::vector<std::string> someStrings = applyRulesVectorOnePart(firstS[ii] + secondS[iii] + pfstr.at(i) + '@' + firstT[ii] + secondT[iii],tempV,pfstr,isCorrect);
						int iiiiii;
						for (iiiiii=0;iiiiii<someStrings.size();iiiiii++){
							returnStrings.push_back(someStrings[iiiiii]);
						}
						//50 ms to here from recent continue
						
				
						
						
						if (nSecond=="3" || nFirst=="3"){
							
							continue;
						}

						
						int numOperations = 0; int ni;
						for (ni=0;ni<firstS[ii].size();ni++){
							if (firstS[ii].at(ni)=='@'){
								break;
							}
							else if (firstS[ii].at(ni)!='#'){
								numOperations++;
							}
						}
						for (ni=0;ni<secondS[iii].size();ni++){
							if (secondS[iii].at(ni)=='@'){
								break;
							}
							else if (secondS[iii].at(ni)!='#'){
								numOperations++;
							}
						}
						if (numOperations > 10){
							continue;
						}
						fullTrees[ftSz] = firstS[ii] + secondS[iii]  + pfstr.at(i);
						ftSz++;
						fullTrees[ftSz] = firstT[ii] + secondT[iii];
						ftSz++;
						if (nSecond=="2" || nFirst=="2"){
							fullTrees[ftSz] = "3";
							ftSz++;
						}
						else if (nSecond=="1" || nFirst=="1"){
							fullTrees[ftSz] = "2";
							ftSz++;
						}
						else {
							fullTrees[ftSz] = "1";
							ftSz++;
						}
						fullTrees[ftSz] = firstSBL[ii] + secondSBL[iii]  + pfstr.at(i);
						ftSz++;
						fullTrees[ftSz] = firstTBL[ii] + secondTBL[iii];
						ftSz++;
						
						//18 ms to here from recent continue
						
				
				
						if (pfstr.at(i) == '+' || pfstr.at(i) == '*'){
							fullTrees[ftSz] = secondS[iii] + firstS[ii]  + pfstr.at(i);
							ftSz++;
							fullTrees[ftSz] = secondT[iii] + firstT[ii];
							ftSz++;
							if (nSecond=="2" || nFirst=="2"){
								fullTrees[ftSz] = "3";
								ftSz++;
							}
							else if (nSecond=="1" || nFirst=="1"){
								fullTrees[ftSz] = "2";
								ftSz++;
							}
							else {
								fullTrees[ftSz] = "1";
								ftSz++;
							}
							fullTrees[ftSz] = secondSBL[iii] + firstSBL[ii]  + pfstr.at(i);
							ftSz++;
							fullTrees[ftSz] = secondTBL[iii] + firstTBL[ii];
							ftSz++;
					
					
							//bottomTreesString[btSz] = secondS[iii] + firstS[ii]  + pfstr.at(i) + '@' + secondT[iii] + firstT[ii];
							//bottomTreesIndex[btSz] = {startLeftIndex,i+1-startLeftIndex,startRightIndex,rightLength};
							//btSz++;
							std::vector<std::string> someStrings = applyRulesVectorOnePart(secondS[iii] + firstS[ii]  + pfstr.at(i) + '@' + secondT[iii] + firstT[ii],{startLeftIndex,i+1-startLeftIndex,startRightIndex,rightLength},pfstr,isCorrect);
							int iiiiii;
							for (iiiiii=0;iiiiii<someStrings.size();iiiiii++){
								returnStrings.push_back(someStrings[iiiiii]);
							}
						}
						//62 ms to here from the 18 ms marker
						
					}
					auto a3 = std::chrono::high_resolution_clock::now();
					duration2 += std::chrono::duration_cast<std::chrono::microseconds>( a3 - a2 ).count();
					
					
				}
				
				
				
			
			
			}
			else {
				//bottomTreesString.resize(btSz+secondS.size());
				//bottomTreesIndex.resize(btSz+secondS.size());
				fullTrees.resize(ftSz+secondS.size()*2*5);
				for (iii=0;iii<secondS.size();iii++){
				
					if (listMap[secondListMapKey][iii*5+2]=="4"){
						continue;
					}
				
					
				
					fullTrees[ftSz] = "#";
					ftSz++;
					std::string bless = secondSBL[iii] + pfstr.at(i) + '@' + secondTBL[iii];
					fullTrees[ftSz] = "{"+bless+"}_";
					ftSz++;
					if (listMap[secondListMapKey][iii*5+2]=="2"){
						fullTrees[ftSz] = "2";
						ftSz++;
					}
					else if (listMap[secondListMapKey][iii*5+2]=="1"){
						fullTrees[ftSz] = "1";
						ftSz++;
					}
					else {
						fullTrees[ftSz] = "0";
						ftSz++;
					}
					fullTrees[ftSz] = secondSBL[iii] + pfstr.at(i);
					ftSz++;
					fullTrees[ftSz] = secondTBL[iii];
					ftSz++;
					
				
					//std::cout << "possible part: " << secondS[iii] + pfstr.at(i) + '@' + secondT[iii] << " and " << startLeftIndex << " and " << startRightOperand << " and " << endRightOperand << " from " << pfstr << "\n";
				
					std::string tempFull = pfstr;
					int iiiii; int operandIdx = -1; int startRightIndex = -1; int rightLength= 0;
					for (iiiii=0;iiiii<tempFull.length();iiiii++){
						if (tempFull.at(iiiii) == '_'){
							operandIdx++;
							if (operandIdx <=endRightOperand){
								rightLength++;
							}
							else {
								break;
							}
						}
						else if (tempFull.at(iiiii) == '@'){
							operandIdx++;
						}
						else if (operandIdx==startRightOperand && startRightIndex<0){
							startRightIndex = iiiii;
							rightLength = 1;
						}
						else{
							rightLength++;
						}
					}
					//bottomTreesString[btSz]=secondS[iii] + pfstr.at(i) + '@' + secondT[iii];
					//bottomTreesIndex[btSz]={startLeftIndex,i+1-startLeftIndex,startRightIndex,rightLength};
					//btSz++;
					std::vector<std::string> someStrings = applyRulesVectorOnePart(secondS[iii] + pfstr.at(i) + '@' + secondT[iii],{startLeftIndex,i+1-startLeftIndex,startRightIndex,rightLength},pfstr,isCorrect);
					int iiiiii;
					for (iiiiii=0;iiiiii<someStrings.size();iiiiii++){
						returnStrings.push_back(someStrings[iiiiii]);
					}
				
				
				
					if (listMap[secondListMapKey][iii*5+2]=="3"){
						continue;
					}
				
					fullTrees[ftSz] = secondS[iii] + pfstr.at(i);
					ftSz++;
					fullTrees[ftSz] = secondT[iii];
					ftSz++;
					if (listMap[secondListMapKey][iii*5+2]=="2"){
						fullTrees[ftSz] = "3";
						ftSz++;
					}
					else if (listMap[secondListMapKey][iii*5+2]=="1"){
						fullTrees[ftSz] = "2";
						ftSz++;
					}
					else {
						fullTrees[ftSz] = "1";
						ftSz++;
					}
					fullTrees[ftSz] = secondSBL[iii] + pfstr.at(i);
					ftSz++;
					fullTrees[ftSz] = secondTBL[iii];
					ftSz++;
					
				
					//condensed
					//fullTrees.push_back("#");
					//fullTrees.push_back("{"+std::to_string(iidx)+"}_");
					//originalMap[iidx]= secondS[iii] + pfstr.at(i) + '@' + secondT[iii];
					//iidx++;
				}
			}
		

			

			//std::cout << "fullTrees size: " << fullTrees.size() << " @ " << i << "\n";
			std::string fullStr = firstStr + secondStr + pfstr.at(i) + '@' + firstTtr + secondTtr;
			
		
			//Parent Node
			std::string opStr = "";
			opStr += pfstr.at(i);
			fullTrees.resize(ftSz);
			
			auto a3 = std::chrono::high_resolution_clock::now();
			
			listMap[fullStr]=fullTrees;
			
			auto a4 = std::chrono::high_resolution_clock::now();
			duration3 += std::chrono::duration_cast<std::chrono::microseconds>( a4 - a3 ).count();
			

			
			
			//bottomTreesString.resize(btSz);
			//bottomTreesIndex.resize(btSz);
			
			

			
		}
		else {
			std::string remed = removeBracketsOne("#@"+originalMap[idx]+'_');
			std::string firstRemed = "";
			std::string secondRemed = "";
			bool isSecondPart = false;
			for (ii=0;ii<remed.length();ii++){
				if (remed.at(ii) == '@'){
					isSecondPart = true;
				}
				else if (isSecondPart){
					secondRemed += remed.at(ii);
				}
				else {
					firstRemed += remed.at(ii);
				}
			}
			listMap["#@" + originalMap[idx] + "_"]={"#",originalMap[idx]+'_',"0",firstRemed,secondRemed};
			operandMap[i]=idx;
			idx++;
		}
		
	}
		
	
	//std::cout << "\n\n---start Original-----\n";
	int iiii;
	return returnStrings;
	

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
	bottomTreesString.resize(0);
	bottomTreesIndex.resize(0);
	btSz = 0;
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
	
	std::cout << "\n\n---start Bracketless-----\n";
	flat_hash_map<int,std::string> bracketlessMap = removeBrackets(originalMap);
	

	std::cout << " ENd bracketless\n";
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

std::vector<std::string> applyRulesVector(std::string userFullString, bool isCorrect) {
	auto a1 = std::chrono::high_resolution_clock::now();
	int iii; int iiii;

	auto a3 = std::chrono::high_resolution_clock::now();
	std::vector<std::vector<std::string>> allOptions;
	std::vector<std::string> allStrings;
	std::string newPostfix = "";
	bool midBracket = false;
	bool foundAt = false;
	int ii;
	for (ii=0;ii<bottomTreesString.size();ii++){
		std::string onePart = bottomTreesString[ii];
		//std::cout << ii << " anda" << onePart << "\n";
		/*
		foundAt = false;
		bool foundFirst = false;
		//int firstOperandIndex = 0;
		//int firstOperandIndexSecond = 0;
		currentOperand = "";
		std::string fullStr = "";
		//int replaceLength = 0;
		//int replaceLengthSecond = 0;
		midBracket = false;
		for (iii=0;iii<onePart.length();iii++){
			if (onePart.at(iii) == '@' && !midBracket){
				foundAt = true;
				currentOperand = "";
				fullStr += onePart.at(iii);
			}
			else if (foundAt && onePart.at(iii) == '{'){
				midBracket = true;
				currentOperand += onePart.at(iii);
				//replaceLengthSecond++;
			}
			else if (foundAt && onePart.at(iii) == '}'){
				midBracket = false;
				currentOperand += onePart.at(iii);
				//replaceLengthSecond++;
			}
			else if (foundAt && !midBracket && onePart.at(iii) == '_'){
				//if (!foundFirst){
				//	firstOperandIndex = operandToIndex[currentOperand];
				//	firstOperandIndexSecond = operandToIndexSecond[currentOperand];
				//}
				foundFirst = true;
				fullStr += operandList[currentOperand]+'_';
				//replaceLengthSecond+= operandList[currentOperand].length()+1;
				currentOperand = "";
				
			}
			else if (foundAt){
				currentOperand += onePart.at(iii);
				//replaceLengthSecond++;
			}
			else {
				fullStr += onePart.at(iii);
				//replaceLength++;
			}
			
		}
		*/
		//replace starting at firstOperandIndex for length=replaceLength
		//replace starting at firstOperandIndexSecond for length=replaceLengthSecond
		//std::cout << iter->first << " and "  << firstOperandIndex << " and "  << firstOperandIndexSecond << " and " << fullStr << '\n';
		//std::string tempReplaced = userFullString;
		//std::cout << tempReplaced.replace(firstOperandIndexSecond,replaceLengthSecond,";;;").replace(firstOperandIndex,replaceLength,"...") << "\n\n";
		

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
				if (rule[1].at(0)=='='){
					
					newPostfix = "#@";
					std::string a = partMap[rule[1].at(2)];
					std::string b = partMap[rule[1].at(3)];
					std::string opResult;
					if (rule[1].at(1)=='+'){
						//std::cout << a << " and " << b << " arithadd\n";
						opResult = addTwoInts(a,b);
						//std::cout << "arithend\n";
					}
					if (rule[1].at(1)=='*'){
						//std::cout << a << " and " << b << " arithmul\n";
						opResult = mulTwoInts(a,b);
						//std::cout << "arithend\n";
					}
					if (rule[1].at(1)=='-'){
						//std::cout << a << " and " << b << " arithesub\n";
						opResult = subTwoInts(a,b);
						//std::cout << "arithend\n";
					}
					if (rule[1].at(1)=='/'){
						//std::cout << a << " and " << b << " arithdiv\n";
						opResult = divTwoInts(a,b);
						//std::cout << "arithend\n";
					}
					
					if (opResult == "false"){
						newPostfix = "";
						continue;
					}
					newPostfix += opResult+'_';
					
					
				}
				else {
					for (iii=0;iii<rule[1].length();iii++){
						if (pastKey){
							if (rule[1].at(iii) == '_'){
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
					if (newPostfix.length()>0){
						//Constraints go here
						for (iiii=3;iiii<rule.size();iiii++){
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
					
					/*
					//std::cout << "userFullString: "<< userFullString << " a " << firstOperandIndexSecond << " a " << replaceLengthSecond << " a " << newPostfixSecond << "\n";
					std::string tempTemp = userFullString;
					tempTemp.replace(firstOperandIndexSecond,replaceLengthSecond,newPostfixSecond);
					//std::cout << "userFullString: "<< userFullString << "\n";
					tempTemp.replace(firstOperandIndex,replaceLength,newPostfixFirst);
					tempTemp = removeBracketsOne(tempTemp);
					newStrings.push_back(tempTemp);
					allStrings.push_back(tempTemp);
					//return userFullString;
					*/
					
					std::string tempTemp = userFullString;
					//std::cout << bottomTrees[ii][1] << " b " << bottomTrees[ii][2] << " c " << bottomTrees[ii][3] << " d " << bottomTrees[ii][4] << "\n";
					tempTemp.replace(bottomTreesIndex[ii][2],bottomTreesIndex[ii][3]+1,newPostfixSecond);
					//std::cout << "userFullString: "<< userFullString << "\n";
					tempTemp.replace(bottomTreesIndex[ii][0],bottomTreesIndex[ii][1],newPostfixFirst);
					//std::cout << bottomTrees[ii][1] << " bb " << bottomTrees[ii][2] << " c " << bottomTrees[ii][3] << " d " << bottomTrees[ii][4] << "\n";
					tempTemp = removeBracketsOne(tempTemp);
					newStrings.push_back(tempTemp);
					allStrings.push_back(tempTemp);
					
				}
			}
			
		}
		if (newStrings.size()>0){
			allOptions.push_back(newStrings);
			
		}
	}
	
	auto a4 = std::chrono::high_resolution_clock::now();
	//duration1 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	//duration2 += std::chrono::duration_cast<std::chrono::microseconds>( a3 - a2 ).count();
	//duration3 += std::chrono::duration_cast<std::chrono::microseconds>( a4 - a3 ).count();

	return allStrings;
	
}

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
			if (rule[1].at(0)=='='){
				
				newPostfix = "#@";
				std::string a = partMap[rule[1].at(2)];
				std::string b = partMap[rule[1].at(3)];
				std::string opResult;
				if (rule[1].at(1)=='+'){
					//std::cout << a << " and " << b << " arithadd\n";
					opResult = addTwoInts(a,b);
					//std::cout << "arithend\n";
				}
				if (rule[1].at(1)=='*'){
					//std::cout << a << " and " << b << " arithmul\n";
					opResult = mulTwoInts(a,b);
					//std::cout << "arithend\n";
				}
				if (rule[1].at(1)=='-'){
					//std::cout << a << " and " << b << " arithesub\n";
					opResult = subTwoInts(a,b);
					//std::cout << "arithend\n";
				}
				if (rule[1].at(1)=='/'){
					//std::cout << a << " and " << b << " arithdiv\n";
					opResult = divTwoInts(a,b);
					//std::cout << "arithend\n";
				}
				
				if (opResult == "false"){
					newPostfix = "";
					continue;
				}
				newPostfix += opResult+'_';
				
				
			}
			else {
				for (iii=0;iii<rule[1].length();iii++){
					if (pastKey){
						if (rule[1].at(iii) == '_'){
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
				if (newPostfix.length()>0){
					//Constraints go here
					for (iiii=3;iiii<rule.size();iiii++){
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
				
				/*
				//std::cout << "userFullString: "<< userFullString << " a " << firstOperandIndexSecond << " a " << replaceLengthSecond << " a " << newPostfixSecond << "\n";
				std::string tempTemp = userFullString;
				tempTemp.replace(firstOperandIndexSecond,replaceLengthSecond,newPostfixSecond);
				//std::cout << "userFullString: "<< userFullString << "\n";
				tempTemp.replace(firstOperandIndex,replaceLength,newPostfixFirst);
				tempTemp = removeBracketsOne(tempTemp);
				newStrings.push_back(tempTemp);
				allStrings.push_back(tempTemp);
				//return userFullString;
				*/
				
				std::string tempTemp = userFullString;
				//std::cout << bottomTrees[ii][1] << " b " << bottomTrees[ii][2] << " c " << bottomTrees[ii][3] << " d " << bottomTrees[ii][4] << "\n";
				tempTemp.replace(oneIndex[2],oneIndex[3]+1,newPostfixSecond);
				//std::cout << "userFullString: "<< userFullString << "\n";
				tempTemp.replace(oneIndex[0],oneIndex[1],newPostfixFirst);
				//std::cout << bottomTrees[ii][1] << " bb " << bottomTrees[ii][2] << " c " << bottomTrees[ii][3] << " d " << bottomTrees[ii][4] << "\n";
				tempTemp = removeBracketsOne(tempTemp);
				newStrings.push_back(tempTemp);
				allStrings.push_back(tempTemp);
				
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
	

	auto t1 = std::chrono::high_resolution_clock::now();
	makeRules("derivatives.csv");
	auto t2 = std::chrono::high_resolution_clock::now();
}

flat_hash_map<std::string,std::vector<std::string>> answerListMap;
int totalAnswers;
/*
void getAnswerListOld(std::string s,bool isCorrect, int nSteps) {

	
	
	
	std::vector<std::vector<std::string>> answerList;

	//std::cout << s << "\n";
	int i;
	int ii;
	int iii;
	int iiii;

	jsonmessage = "";
	std::string pfstr = s;
	//std::cout << pfstr << '\n';


	std::string newPostfix = pfstr;

	int maxSteps = 10;
	newPostfix = removeBracketsOne(newPostfix);
	
	//std::cout << s << " before pl\n";
	auto a1 = std::chrono::high_resolution_clock::now();
	makeTree(newPostfix);
	auto a2 = std::chrono::high_resolution_clock::now();
	int dd1 = std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	duration1 += dd1;
	//std::cout << dd1 << "  ";
	//std::cout << s << " after pl\n";

	std::vector<std::string> allStrings; //vector of the next step
	
	std::vector<std::string> someStrings = applyRulesVector(newPostfix,isCorrect);
	//std::cout << s << " andand " << someStrings.size() << "\n";
	for (iii=0;iii<someStrings.size();iii++){
		//std::cout << someStrings[iii] << "\n";
		someStrings[iii] = removeBracketsOne(someStrings[iii]);
		allStrings.push_back(someStrings[iii]);
	}

	answerList.push_back({newPostfix});
	
	
	
	
	for (ii=0;ii<allStrings.size();ii++){
		std::vector<std::vector<std::string>> tailAnswerList;
		
		if (answerListMap.find(allStrings[ii]) != answerListMap.end()){
			tailAnswerList = answerListMap[allStrings[ii]];
		}
		else {
			getAnswerList(allStrings[ii],isCorrect);
			tailAnswerList = answerListMap[allStrings[ii]];
		}
		
		for (iii=0;iii<tailAnswerList.size();iii++){
			if (tailAnswerList[iii].size()<maxSteps){
				std::vector<std::string> oneAnswer;
				oneAnswer = {newPostfix};
				bool hasLoop = false;
				for (iiii=0;iiii<tailAnswerList[iii].size();iiii++){
					if (tailAnswerList[iii][iiii] == newPostfix){
						hasLoop = true;
						break;
					}
					oneAnswer.push_back(tailAnswerList[iii][iiii]);
				}
				if (!hasLoop){
					answerList.push_back(oneAnswer);
				}
				
			}
		}
		
	
	}


		
	answerListMap[newPostfix] = answerList;
}
*/
bool getAnswerList(std::string s,bool isCorrect, int nSteps) {

	
	if (nSteps >= 10){
		return false;
	}
	//std::cout << s << "\n";
	int i;
	int ii;
	int iii;
	int iiii;

	jsonmessage = "";
	std::string pfstr = s;
	//std::cout << pfstr << '\n';


	std::string newPostfix = pfstr;

	int maxSteps = 10;
	newPostfix = removeBracketsOne(newPostfix);
	
	std::cout << s << " before pl\n";
	auto a1 = std::chrono::high_resolution_clock::now();
	std::vector<std::string> someStrings = makeTree(newPostfix);
	auto a2 = std::chrono::high_resolution_clock::now();
	int dd1 = std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	duration1 += dd1;
	//std::cout << dd1 << "  ";
	std::cout << s << " after pl\n";

	std::vector<std::string> allStrings; //vector of the next step
	flat_hash_map<std::string,bool> uniqueStrings;
	
	std::cout << bottomTreesString.size() << "\n";

	
	for (iii=0;iii<someStrings.size();iii++){
		//std::cout << someStrings[iii] << "\n";
		someStrings[iii] = removeBracketsOne(someStrings[iii]);
		if (uniqueStrings.find(someStrings[iii]) != uniqueStrings.end()){
	
		}
		else {
			allStrings.push_back(someStrings[iii]);
			uniqueStrings[someStrings[iii]]=true;
		}
	
	}

	answerListMap[newPostfix] = allStrings;
	totalAnswers += allStrings.size();
	std::cout << totalAnswers << "\n";
	for (ii=0;ii<allStrings.size();ii++){
		std::cout << allStrings[ii] << "\n";
		if (answerListMap.find(allStrings[ii]) != answerListMap.end()){
		
		}
		else {
			getAnswerList(allStrings[ii],isCorrect,nSteps+1);
		}
		
	
	}

	return true;
		
	
}

std::string fullAnswer(std::string s, std::string a){
	std::string newPostfix = removeBracketsOne(postfixify(s));
	std::cout << "\n\n\n\nStarting the Loop @$*&^@$*&^@*$&^@*$&^\n\n\n\n";
	auto a1 = std::chrono::high_resolution_clock::now();
	getAnswerList(newPostfix,false,0);
	auto a2 = std::chrono::high_resolution_clock::now();
	//duration1 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	std::cout << "\n\n\n\nCompleted the Loop @$*&^@$*&^@*$&^@*$&^\n\n\n\n" << answerListMap[newPostfix].size() << "\n\n\n";
	int i; int ii;
	std::string mpf = postfixify(a);
	std::string error = "Don't know.";
	int ui = 0;
	flat_hash_map<std::string,int> uniqueAnswers;
	for (i=0;i<answerListMap[newPostfix].size();i++){
		//std::cout << "answer: " << answerListMap[newPostfix][i][answerListMap[newPostfix][i].size()-1] << "\n";
		if (uniqueAnswers.find(answerListMap[newPostfix][i]) != uniqueAnswers.end()){
			uniqueAnswers[answerListMap[newPostfix][i]]++;
		}
		else {
			uniqueAnswers[answerListMap[newPostfix][i]]=1;
			ui++;
		}
		
		if (answerListMap[newPostfix][i] == mpf){
			//TODO: grab the error
			//TODO: send that info to node to display/add to database
			error = "Found";
		}
		
	}
	std::cout << "n maybe wrong answers: " << i  << " and unique: " << ui << "\n";
	return error;
}

bool correctAnswer(std::string s, std::string a){
	std::string newPostfix = removeBracketsOne(postfixify(s));
	std::cout << "\n\n\n\nStarting the Loop @$*&^@$*&^@*$&^@*$&^\n\n\n\n";
	mapSave = 0; mapMake = 0;
	auto a1 = std::chrono::high_resolution_clock::now();
	totalAnswers = 0;
	getAnswerList(newPostfix,true,0);
	auto a2 = std::chrono::high_resolution_clock::now();
	//duration1 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	std::cout << "\n\n\n\nCompleted the Loop @$*&^@$*&^@*$&^@*$&^\n\n\n\n" << totalAnswers << "\n\n\n";
	int i; int ii;
	std::string mpf = postfixify(a);
	
	int minLen = 10000;
	int minIdx = 0;
	bool isCorrect = false;
	int ui = 0;
	flat_hash_map<std::string,int> uniqueAnswers;
	for (i=0;i<answerListMap[newPostfix].size();i++){
		//std::cout << "correct: " << answerListMap[newPostfix][i][answerListMap[newPostfix][i].size()-1] << "\n";
		if (uniqueAnswers.find(answerListMap[newPostfix][i]) != uniqueAnswers.end()){
			uniqueAnswers[answerListMap[newPostfix][i]]++;
		}
		else {
			uniqueAnswers[answerListMap[newPostfix][i]]=1;
			ui++;
			std::cout << answerListMap[newPostfix][i] << "\n";
		}
		
		if (answerListMap[newPostfix][i] == mpf){
			isCorrect = true;
		}
	}
	std::cout << "your answer: " << mpf << "\n";
	std::cout << "n answers: " << i  << " and unique: " << ui << "\n";

	jsonmessage = "";
	for (ii=0;ii<answerListMap[newPostfix].size();ii++){
		//std::cout << minIdx << " with " << answerListMap[newPostfix][minIdx][ii] << "\n";
		
		outputTree(answerListMap[newPostfix][ii]);
	}
	return isCorrect;
}

void Hello(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	//v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	//v8::String::Utf8Value s(isolate, info[0]);
	//std::string str(*s);
	jsonmessage = "var rule = {};";
	initialRun();
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(jsonmessage);
	info.GetReturnValue().Set(h.ToLocalChecked());
}
void GetAnswer(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string str(*s);
	v8::String::Utf8Value sa(isolate, info[1]);
	std::string astr(*sa);
	std::cout << "input: "<< str << "\n";
	jsonmessage = "";
	
	bool isCorrect = correctAnswer(str,astr);
	
	std::cout << "Time to correct: " << duration1 << " and " << duration2 << " and " << duration3 << "\n";
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(jsonmessage);
	std::string error = "None!";
	if (!isCorrect){
		error = fullAnswer(str,astr);
		
	}
	std::cout << "Time to error: " << duration1 << "\n";
	//std::cout << "TIMES: " << duration1 << " and " << duration2 << " and " << duration3 << "\n";
	std::cout << "Error: " << error << "\n";
	
	//std::cout << "TIMES: " << duration1 << " and " << duration2 << " and " << duration3 << "\n";
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
               Nan::New("answer").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(GetAnswer)
                   ->GetFunction(context)
                   .ToLocalChecked());
}

NODE_MODULE(helloarray, Init)