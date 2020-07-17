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
#include <variant>
#include <map>
#include <numeric>
#include <chrono>
#include <thread>
#include <sstream>
#include <iostream>
#include <array>
#include <vector>

#include "rapidcsv.h"
#include "parallel_hashmap/phmap.h"


using namespace std::chrono;
using phmap::flat_hash_map;
flat_hash_map<std::string,std::string> treeMap;
flat_hash_map<char,int> prec;
flat_hash_map<std::string,std::vector<std::vector<std::string>>> rules;
flat_hash_map<std::string,flat_hash_map<std::string,std::string>> allListMap;
std::string jsonmessage;
int duration1;
int duration2;
int duration3;
int yesC;
int noC;

		
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

	int len = a.length();
	if (b.length() > len){
		len = b.length();
	}
	int i;
	for (i=0;i<len;i++){
		int aa = a.at(len-1-i) - '0';
		if (aa<0 || aa>9){
			return "false";
		}
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
	for (iii=0;iii<input.length();iii++){
		if (input.at(iii) == '{'){
			foundBracket = true;
			bracketLength = 1;
			secondIndex = iii;
		}
		else if (input.at(iii) == '}') {
			bracketStrings.push_back(tempString);
			bracketLength++;
			break;
		}
		else if (input.at(iii) == '#' && !foundBracket) {
			operandToIndex[idx]=iii;
			idx++;
		}
		else if (input.at(iii) == '_' && !foundBracket) {
			iidx++;
		}
		else if (input.at(iii) == '@' && !foundBracket) {
			foundAt = true;
		}
		else if (input.at(iii) == '@' && foundBracket) {
			//tempString += input.at(iii);
			bracketStrings.push_back(tempString);
			tempString = "";
			bracketLength++;
		}
		else if (foundBracket){
			tempString += input.at(iii);
			bracketLength++;
		}
	}
	if (!foundBracket){
		return input;
	}
	
	int firstIndex = operandToIndex[iidx];
	std::cout << input << " --a\n";
	input.replace(secondIndex,bracketLength+1,bracketStrings[1]);
	std::cout << input << " --b\n";
	input.replace(firstIndex,1,bracketStrings[0]);
	std::cout << input << " --c\n";
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
	for (i=0;i<pfstr.length();i++){
		if (pfstr.at(i) == '@'){
			break;
		}
		else if (pfstr.at(i) != '#'){
			std::vector<std::string> secondS;
			std::vector<std::string> secondT;
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
					secondS.resize(listMap[s+'@'+t].size()/2);
					secondT.resize(listMap[s+'@'+t].size()/2);
					for (iii=0;iii<listMap[s+'@'+t].size()/2;iii++){
						secondS[iii]=listMap[s+'@'+t][iii*2];
						secondT[iii]=listMap[s+'@'+t][iii*2+1];
					}
					maxi = ii;
					break;
				}
			}
			std::vector<std::string> firstS;
			std::vector<std::string> firstT;
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
						firstS.resize(listMap[s+'@'+t].size()/2);
						firstT.resize(listMap[s+'@'+t].size()/2);
						for (iii=0;iii<listMap[s+'@'+t].size()/2;iii++){
							firstS[iii]=listMap[s+'@'+t][iii*2];
							firstT[iii]=listMap[s+'@'+t][iii*2+1];
						}
						break;
					}
				}
				
				
				for (ii=0;ii<firstS.size();ii++){
					for (iii=0;iii<secondS.size();iii++){
						fullTrees.push_back(firstS[ii] + secondS[iii]  + pfstr.at(i));
						fullTrees.push_back(firstT[ii] + secondT[iii]);
						
						//condensed
						fullTrees.push_back("#");
						fullTrees.push_back("{"+std::to_string(iidx)+"}_");
						originalMap[iidx]= firstS[ii] + secondS[iii] + pfstr.at(i) + '@' + firstT[ii] + secondT[iii];
						iidx++;
						
						if (pfstr.at(i) == '+' || pfstr.at(i) == '*'){
							fullTrees.push_back(secondS[iii] + firstS[ii]  + pfstr.at(i));
							fullTrees.push_back(secondT[iii] + firstT[ii]);
						}
					}
				}
				
			}
			else {
				for (iii=0;iii<secondS.size();iii++){
					fullTrees.push_back(secondS[iii] + pfstr.at(i));
					fullTrees.push_back(secondT[iii]);
					
					//condensed
					fullTrees.push_back("#");
					fullTrees.push_back("{"+std::to_string(iidx)+"}_");
					originalMap[iidx]= secondS[iii] + pfstr.at(i) + '@' + secondT[iii];
					iidx++;
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
				/*if (nodeList.find(nodeText) != nodeList.end()){
					nodeList[nodeText][1] = pname;
					orderedKeyList.push_back(nodeText);
				}
				else {
					name = "node"+std::to_string(treeIdx);
					treeIdx++;
					nodeList[nodeText] = {name,pname};
					orderedKeyList.push_back(nodeText);
				}*/
			}
			orderedKeyList.push_back(fullStr);
			
			//
			//for (ii=0;ii<fullTrees.size();ii++){
			//	std::cout << i << "-:::-" << fullTrees[ii] << '\n';
			//}
			
			listMap[fullStr]=fullTrees;
			finalList = fullTrees;
			
		}
		else {
			listMap["#@" + std::to_string(idx) + "_"]={"#",originalMap[idx]+'_'};
			finalList = {"#",originalMap[idx]+'_'};
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
	
	//std::cout << "\n\n---start Bracketless-----\n";
	flat_hash_map<int,std::string> bracketlessMap = removeBrackets(originalMap);
	
	
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
	
	flat_hash_map<std::string,int> uniqueMap;
	for (ii=0;ii<finalList.size()/2;ii++){
		std::vector<int> indexes; //start,length,iidx
		std::string currentOperand = "";
		int startIndex = 0;
		
		//std::cout << ii << "-:=1=:- " << finalList[ii*2]+'@'+finalList[ii*2+1] << '\n';
		int leftB = 0;
		int rightB = 0;
		
		bool isInt = true;
		std::string oldFinalList = finalList[ii*2+1];
		std::string oldRep ="";
		std::string oldOrig ="";
		for (iii=0;iii<finalList[ii*2+1].length();iii++){
			if (finalList[ii*2+1].at(iii) == '{'){
				startIndex = iii;
				currentOperand = "";
				isInt = true;
			}
			else if (finalList[ii*2+1].at(iii) == '}'){
				
				if (isInt){
					indexes.push_back(startIndex+1);
					indexes.push_back(iii-(startIndex+1));
					indexes.push_back(std::stoi(currentOperand));
				}
				
				currentOperand = "";
				isInt = true;
			}
			else {
				currentOperand += finalList[ii*2+1].at(iii);
				if (finalList[ii*2+1].at(iii) - '0' < 0 || finalList[ii*2+1].at(iii) - '0' > 9) {
					isInt = false;
				}
			}
		}
		
		for (iii=indexes.size()/3-1;iii>=0;iii--){
			std::string repText = bracketlessMap[indexes[iii*3+2]];
			oldRep += repText + "|||||";
			oldOrig += originalMap[indexes[iii*3+2]] + "|||||";
			finalList[ii*2+1].replace(indexes[iii*3],indexes[iii*3+1],repText);
			//std::cout << ii << "-:=2a=:- " << finalList[ii*2]+'@'+finalList[ii*2+1] << '\n';
			
		}
		
		leftB = 0;
		rightB = 0;
		
		for (iii=0;iii<finalList[ii*2+1].length();iii++){
			if (finalList[ii*2+1].at(iii) == '{'){
				leftB++;
			}
			else if (finalList[ii*2+1].at(iii) == '}'){
				rightB++;
				if (rightB > leftB){
					//std::cout << "\n!!!!!!!!!!!Old: " << oldFinalList << " andNew: "<< finalList[ii*2+1] << " andRep: " << oldRep << " andOrig: " << oldOrig << " !!!!!!!!!!!\n";
				}
			}
		}
		
		
		if (uniqueMap.find(finalList[ii*2]+'@'+finalList[ii*2+1]) == uniqueMap.end()){
			treeOptions.push_back(finalList[ii*2]+'@'+finalList[ii*2+1]);
			uniqueMap[finalList[ii*2]+'@'+finalList[ii*2+1]] = 1;
		}
		
		
		//std::cout << ii << "-:===:- " << treeOptions[ii] << '\n';
	}
	//for (flat_hash_map<int,std::string>::iterator iter = bracketlessMap.begin(); iter != bracketlessMap.end(); ++iter){
	//	std::cout << iter->first << " bracketless " << iter->second << '\n';
	//}
	//std::cout << '\n';
	return treeOptions;
}

flat_hash_map<std::string,std::vector<std::string>> makeListFull(std::string pfstr){
	std::vector<std::string> treeOptions;
	flat_hash_map<std::string,std::vector<std::string>> listMap;
	flat_hash_map<int,std::string> operandMap;
	flat_hash_map<int,std::string> originalMap;
	std::vector<std::string> finalList;
	
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
	for (i=0;i<pfstr.length();i++){
		if (pfstr.at(i) == '@'){
			break;
		}
		else if (pfstr.at(i) != '#'){
			std::vector<std::string> secondS;
			std::vector<std::string> secondT;
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
					secondS.resize(listMap[s+'@'+t].size()/2);
					secondT.resize(listMap[s+'@'+t].size()/2);
					for (iii=0;iii<listMap[s+'@'+t].size()/2;iii++){
						secondS[iii]=listMap[s+'@'+t][iii*2];
						secondT[iii]=listMap[s+'@'+t][iii*2+1];
					}
					maxi = ii;
					break;
				}
			}
			std::vector<std::string> firstS;
			std::vector<std::string> firstT;
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
						firstS.resize(listMap[s+'@'+t].size()/2);
						firstT.resize(listMap[s+'@'+t].size()/2);
						for (iii=0;iii<listMap[s+'@'+t].size()/2;iii++){
							firstS[iii]=listMap[s+'@'+t][iii*2];
							firstT[iii]=listMap[s+'@'+t][iii*2+1];
						}
						break;
					}
				}
				
				
				for (ii=0;ii<firstS.size();ii++){
					for (iii=0;iii<secondS.size();iii++){
						fullTrees.push_back(firstS[ii] + secondS[iii]  + pfstr.at(i));
						fullTrees.push_back(firstT[ii] + secondT[iii]);
						
						//condensed
						fullTrees.push_back("#");
						fullTrees.push_back("{"+std::to_string(iidx)+"}_");
						originalMap[iidx]= firstS[ii] + secondS[iii] + pfstr.at(i) + '@' + firstT[ii] + secondT[iii];
						iidx++;
						
						if (pfstr.at(i) == '+'){
							fullTrees.push_back(secondS[iii] + firstS[ii]  + pfstr.at(i));
							fullTrees.push_back(secondT[iii] + firstT[ii]);
						}
					}
				}
				
			}
			else {
				for (iii=0;iii<secondS.size();iii++){
					fullTrees.push_back(secondS[iii] + pfstr.at(i));
					fullTrees.push_back(secondT[iii]);
					
					//condensed
					fullTrees.push_back("#");
					fullTrees.push_back("{"+std::to_string(iidx)+"}_");
					originalMap[iidx]= secondS[iii] + pfstr.at(i) + '@' + secondT[iii];
					iidx++;
				}
			}
			
			
			
			std::string fullStr = firstStr + secondStr + pfstr.at(i) + '@' + firstTtr + secondTtr;
			
			//std::cout << i << "---" << fullStr << '\n';
			//
			//for (ii=0;ii<fullTrees.size();ii++){
			//	std::cout << i << "-:::-" << fullTrees[ii] << '\n';
			//}
			
			listMap[fullStr]=fullTrees;
			finalList = fullTrees;
			
		}
		else {
			listMap["#@" + std::to_string(idx) + "_"]={"#",originalMap[idx]+'_'};
			finalList = {"#",originalMap[idx]+'_'};
			operandMap[i]=std::to_string(idx);
			idx++;
		}
		
	}
	
	//std::cout << "\n\n---start Original-----\n";
	int iiii;
	
	//for (flat_hash_map<int,std::string>::iterator iter = originalMap.begin(); iter != originalMap.end(); ++iter){
	//	std::cout << iter->first << " and " << iter->second << '\n';
	//}
	
	//std::cout << "\n\n---start Bracketless-----\n";
	//flat_hash_map<int,std::string> bracketlessMap = removeBrackets(originalMap);
	
	//for (flat_hash_map<int,std::string>::iterator iter = bracketlessMap.begin(); iter != bracketlessMap.end(); ++iter){
	//	std::cout << iter->first << " and " << iter->second << '\n';
	//}
	
	/*
	flat_hash_map<std::string,std::vector<std::string>> newListMap;
	for (flat_hash_map<std::string,std::vector<std::string>>::iterator iter = listMap.begin(); iter != listMap.end(); ++iter){
		std::vector<std::string> oneList = iter->second;
		
		for (ii=0;ii<oneList.size()/2;ii++){
			std::vector<int> indexes; //start,length,iidx
			std::string currentOperand = "";
			int startIndex = 0;
		
			//std::cout << ii << "-:=1=:- " << iter->first << " *** " << oneList[ii*2]+'@'+oneList[ii*2+1] << '\n';
		
		
			for (iii=0;iii<oneList[ii*2+1].length();iii++){
				if (oneList[ii*2+1].at(iii) == '{'){
					startIndex = iii;
					currentOperand = "";
				}
				else if (oneList[ii*2+1].at(iii) == '}'){
					indexes.push_back(startIndex+1);
					indexes.push_back(iii-(startIndex+1));
					indexes.push_back(std::stoi(currentOperand));
					currentOperand = "";
				}
				else {
					currentOperand += oneList[ii*2+1].at(iii);
				}
			}
		
			for (iii=indexes.size()/3-1;iii>=0;iii--){
				std::string repText = bracketlessMap[indexes[iii*3+2]];
				bool foundBracket = false;
				for (iiii=0;iiii<repText.length();iiii++){
					if (repText.at(iiii) == '{'){
						foundBracket = true;
						break;
					}
				}
				//oneList[ii*2+1].replace(indexes[iii*3],indexes[iii*3+1],repText);
				//std::cout << ii << "-:=2a=:- " << oneList[ii*2]+'@'+oneList[ii*2+1] << '\n';
			
			}
			
			
		}
		
		newListMap[iter->first]=oneList;
	}
	*/
	
	//std::cout << '\n';
	return listMap;
}

flat_hash_map<std::string,std::string> makeList(std::string pfstr){
	std::vector<std::string> treeOptions;
	flat_hash_map<std::string,std::string> listMap;
	flat_hash_map<int,std::string> operandMap;
	flat_hash_map<int,std::string> originalMap;
	
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
			else {
				
			}

			
			std::string fullStr = firstStr + secondStr + pfstr.at(i) + '@' + firstTtr + secondTtr;
			
			
			listMap[fullStr]="";
			
		}
		else {
			listMap["#@" + std::to_string(idx) + "_"]="";
			operandMap[i]=std::to_string(idx);
			idx++;
		}
		
	}
	
	//std::cout << "\n\n---start Original-----\n";
	int iiii;
	
	
	
	//std::cout << '\n';
	return listMap;
}



#include "postfixify.cpp"

#include "makerules.cpp"

std::string applyRules(std::string userFullString) {
	auto a1 = std::chrono::high_resolution_clock::now();
	
	int iii; int iiii;
	flat_hash_map<std::string,std::string> allParts;
	//allParts = makeList(userFullString);
	
	
	if (allListMap.find(userFullString) != allListMap.end()){
		allParts = allListMap[userFullString];
		yesC++;
	}
	else {
		allParts = makeList(userFullString);
		allListMap[userFullString] = allParts;
		noC++;
	}
	
	auto a2 = std::chrono::high_resolution_clock::now();
	flat_hash_map<std::string,int> operandToIndex;
	flat_hash_map<std::string,int> operandToIndexSecond;
	flat_hash_map<std::string,std::string> operandList;
	std::string newPostfix = "";
	int idx = 0;
	//std::cout << "\n\n" << userFullString << '\n';
	for (iii=0;iii<userFullString.length();iii++){
		if (userFullString.at(iii) == '@'){
			break;
		}
		else if (userFullString.at(iii) == '#'){
			operandToIndex[std::to_string(idx)] = iii;
			idx++;
		}
	}
	idx = 0;
	bool midBracket = false;
	for (iii=0;iii<userFullString.length();iii++){
		if (userFullString.at(iii) == '_' && !midBracket){
			operandToIndexSecond[std::to_string(idx)] = iii+1;
			idx++;
		}
		else if (userFullString.at(iii) == '{'){
			midBracket = true;
		}
		else if (userFullString.at(iii) == '}'){
			midBracket = false;
		}
		else if (userFullString.at(iii) == '@' && !midBracket){
			operandToIndexSecond[std::to_string(idx)] = iii+1;
			idx++;
		}
	}
	bool foundAt = false;
	std::string currentOperand = "";
	idx = 0;
	midBracket = false;
	for (iii=0;iii<userFullString.length();iii++){
		if (userFullString.at(iii) == '@' && !midBracket){
			foundAt = true;
			currentOperand = "";
		}
		else if (userFullString.at(iii) == '{'){
			currentOperand += userFullString.at(iii);
			midBracket = true;
		}
		else if (userFullString.at(iii) == '}'){
			currentOperand += userFullString.at(iii);
			midBracket = false;
		}
		else if (foundAt && userFullString.at(iii) == '_' && !midBracket){
			operandList[std::to_string(idx)] = currentOperand;
			idx++;
			currentOperand = "";
		}
		else {
			currentOperand += userFullString.at(iii);
		}
	}
	auto a3 = std::chrono::high_resolution_clock::now();
	for (flat_hash_map<std::string,std::string>::iterator iter = allParts.begin(); iter != allParts.end(); ++iter){
		std::string onePart = iter->first;
		foundAt = false;
		bool foundFirst = false;
		int firstOperandIndex = 0;
		int firstOperandIndexSecond = 0;
		currentOperand = "";
		std::string fullStr = "";
		int replaceLength = 0;
		int replaceLengthSecond = 0;
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
				if (!foundFirst){
					firstOperandIndex = operandToIndex[currentOperand];
					firstOperandIndexSecond = operandToIndexSecond[currentOperand];
				}
				foundFirst = true;
				fullStr += operandList[currentOperand]+'_';
				replaceLengthSecond+= operandList[currentOperand].length()+1;
				currentOperand = "";
				
			}
			else if (foundAt){
				currentOperand += onePart.at(iii);
				//replaceLengthSecond++;
			}
			else {
				fullStr += onePart.at(iii);
				replaceLength++;
			}
			
		}
		//replace starting at firstOperandIndex for length=replaceLength
		//replace starting at firstOperandIndexSecond for length=replaceLengthSecond
		//std::cout << iter->first << " and "  << firstOperandIndex << " and "  << firstOperandIndexSecond << " and " << fullStr << '\n';
		//std::string tempReplaced = userFullString;
		//std::cout << tempReplaced.replace(firstOperandIndexSecond,replaceLengthSecond,";;;").replace(firstOperandIndex,replaceLength,"...") << "\n\n";
		

		std::string userString = fullStr;
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
			//std::cout << "Key Match: " << key << " and " << rules[key][0] << "\n";
			//std::cout << "userFullString @ keyMatch: "<< userFullString << "\n";
			int ruleIdx;
			for (ruleIdx=0;ruleIdx<rules[key].size();ruleIdx++){
				//std::cout << "Key Match: " << key << " and " << rules[key][ruleIdx][0] << "\n";
				std::vector<std::string> rule = rules[key][ruleIdx];
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
						opResult = addTwoInts(a,b);
					}
					if (rule[1].at(1)=='*'){
						opResult = mulTwoInts(a,b);
					}
					if (rule[1].at(1)=='-'){
						opResult = subTwoInts(a,b);
					}
					if (rule[1].at(1)=='/'){
						opResult = divTwoInts(a,b);
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
					//std::cout << "userFullString: "<< userFullString << " a " << firstOperandIndexSecond << " a " << replaceLengthSecond << " a " << newPostfixSecond << "\n";
					userFullString.replace(firstOperandIndexSecond,replaceLengthSecond,newPostfixSecond);
					//std::cout << "userFullString: "<< userFullString << "\n";
					userFullString.replace(firstOperandIndex,replaceLength,newPostfixFirst);
					userFullString = removeBracketsOne(userFullString);
					return userFullString;
				}
			}
		}
	}
	auto a4 = std::chrono::high_resolution_clock::now();
	duration1 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	duration2 += std::chrono::duration_cast<std::chrono::microseconds>( a3 - a2 ).count();
	duration3 += std::chrono::duration_cast<std::chrono::microseconds>( a4 - a3 ).count();
	if (newPostfix.length()==0){
		return userFullString;
	}
	return newPostfix;
	
}

/*
int main (int argc, char *argv[]) {

	duration1 = 0;
	duration2 = 0;
	duration3 = 0;
	yesC = 0;
	noC = 0;


	
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
	prec['&'] = 1;
	prec['|'] = 0;
	prec['('] = -1;
	prec[')'] = -1;
	

	auto t1 = std::chrono::high_resolution_clock::now();
	rules = makeRules();
	auto t2 = std::chrono::high_resolution_clock::now();
	
	int ii;
	//for (ii=0;ii<rules.size();ii++){
	//	std::cout << ii << "-=-" << rules[ii] << '\n';
	//}
	
	//auto t1 = std::chrono::high_resolution_clock::now();
	
	
	
	//std::string s = "ddx(x^3+x^2+7+11*2*3)"; 
	

  	
  	std::string s(argv[1]);
  	
	std::string pfstr = postfixify(s);
	std::cout << pfstr << '\n';
	
	
	std::string newPostfix = pfstr;
	std::string oldPostfix = "";
	
	int maxSteps = 10;
	while (newPostfix != oldPostfix && maxSteps >=0){
		auto t3 = std::chrono::high_resolution_clock::now();
		newPostfix = removeBracketsOne(newPostfix);
		std::cout << "\n\n-----------&&&&&--------\n\n" << newPostfix << " ------- " << maxSteps << "\n\n";
		oldPostfix = newPostfix;
		auto t4 = std::chrono::high_resolution_clock::now();
		std::vector<std::string> postList = makeTree(oldPostfix);
		auto t5 = std::chrono::high_resolution_clock::now();
		bool changedInput = false;
		std::cout << "postListSize: " << postList.size() << "\n\n";
		for (ii=0;ii<postList.size();ii++){
			//std::cout << "--------\n" << ii << " ---- " << postList[ii] << "\n--------------";
			newPostfix = applyRules(postList[ii]);
			//std::cout << "--------\n" << ii << " ---- " << newPostfix << "\n--------------";
			if (newPostfix != postList[ii]){
				std::cout << "Match: " << postList[ii] << " into "<< newPostfix << " from " << oldPostfix << '\n';
				changedInput = true;
				break;
			}
			//std::cout << "--------\n" << ii << " ---- " << newPostfix << "\n--------------";
			
		}
		auto t6 = std::chrono::high_resolution_clock::now();
		auto d1 = std::chrono::duration_cast<std::chrono::microseconds>( t4 - t3 ).count();
		auto d2 = std::chrono::duration_cast<std::chrono::microseconds>( t5 - t4 ).count();
		auto d3 = std::chrono::duration_cast<std::chrono::microseconds>( t6 - t5 ).count();
		std::cout << "TIMES: " << duration1 << " and " << duration2 << " and " << duration3 << "\n\n";
		std::cout << "NOYES: " << noC << " and " << yesC << "\n\n";
		if (!changedInput){break;}
		std::cout << "Match: " << pfstr << " into "<< newPostfix << '\n';
		
		maxSteps--;

	}
	
	//auto t2 = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>( t2 - t1 ).count();
    std::cout << duration;
    
    //run it again
	if (2==3){

		t1 = std::chrono::high_resolution_clock::now();

		s = "ddx(7*(x^3+5))"; 
  
		pfstr = postfixify(s);
		std::cout << pfstr << '\n';
	
	
		newPostfix = pfstr;
		oldPostfix = "";
	
		maxSteps = 5;
		while (newPostfix != oldPostfix && maxSteps >=0){
			auto t3 = std::chrono::high_resolution_clock::now();
			newPostfix = removeBracketsOne(newPostfix);
			std::cout << "\n\n-----------&&&&&--------\n\n" << newPostfix << " ------- " << maxSteps << "\n\n";
			oldPostfix = newPostfix;
			auto t4 = std::chrono::high_resolution_clock::now();
			std::vector<std::string> postList = makeTree(oldPostfix);
			auto t5 = std::chrono::high_resolution_clock::now();
			bool changedInput = false;
			std::cout << "postListSize: " << postList.size() << "\n\n";
			for (ii=0;ii<postList.size();ii++){
				//std::cout << "--------\n" << ii << " ---- " << postList[ii] << "\n--------------";
				newPostfix = applyRules(postList[ii]);
				//std::cout << "--------\n" << ii << " ---- " << newPostfix << "\n--------------";
				if (newPostfix != postList[ii]){
					std::cout << "Match: " << postList[ii] << " into "<< newPostfix << " from " << oldPostfix << '\n';
					changedInput = true;
					break;
				}
				//std::cout << "--------\n" << ii << " ---- " << newPostfix << "\n--------------";
			
			}
			auto t6 = std::chrono::high_resolution_clock::now();
			auto d1 = std::chrono::duration_cast<std::chrono::microseconds>( t4 - t3 ).count();
			auto d2 = std::chrono::duration_cast<std::chrono::microseconds>( t5 - t4 ).count();
			auto d3 = std::chrono::duration_cast<std::chrono::microseconds>( t6 - t5 ).count();
			std::cout << "TIMES: " << duration1 << " and " << duration2 << " and " << duration3 << "\n\n";
			std::cout << "NOYES: " << noC << " and " << yesC << "\n\n";
			if (!changedInput){break;}
			std::cout << "Match: " << pfstr << " into "<< newPostfix << '\n';
		
			maxSteps--;

		}
	}
    
}
*/

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
	prec['&'] = 1;
	prec['|'] = 0;
	prec['('] = -1;
	prec[')'] = -1;
	

	auto t1 = std::chrono::high_resolution_clock::now();
	makeRules("derivatives.csv");
	auto t2 = std::chrono::high_resolution_clock::now();
}

std::string getAnswer(std::string s){
	duration1 = 0;
	duration2 = 0;
	duration3 = 0;
	yesC = 0;
	noC = 0;


	int i;
	int ii;


  	
	std::string pfstr = postfixify(s);
	std::cout << pfstr << '\n';
	
	
	std::string newPostfix = pfstr;
	std::string oldPostfix = "";
	
	int maxSteps = 10;
	while (newPostfix != oldPostfix && maxSteps >=0){
		auto t3 = std::chrono::high_resolution_clock::now();
		newPostfix = removeBracketsOne(newPostfix);
		//std::cout << "\n\n-----------&&&&&--------\n\n" << newPostfix << " ------- " << maxSteps << "\n\n";
		oldPostfix = newPostfix;
		auto t4 = std::chrono::high_resolution_clock::now();
		std::vector<std::string> postList = makeTree(oldPostfix);
		auto t5 = std::chrono::high_resolution_clock::now();
		bool changedInput = false;
		//std::cout << "postListSize: " << postList.size() << "\n\n";
		for (ii=0;ii<postList.size();ii++){
			//std::cout << "--------\n" << ii << " ---- " << postList[ii] << "\n--------------";
			newPostfix = applyRules(postList[ii]);
			//std::cout << "--------\n" << ii << " ---- " << newPostfix << "\n--------------";
			if (newPostfix != postList[ii]){
				std::cout << "Match: " << postList[ii] << " into "<< newPostfix << " from " << oldPostfix << '\n';
				changedInput = true;
				break;
			}
			//std::cout << "--------\n" << ii << " ---- " << newPostfix << "\n--------------";
			
		}
		auto t6 = std::chrono::high_resolution_clock::now();
		auto d1 = std::chrono::duration_cast<std::chrono::microseconds>( t4 - t3 ).count();
		auto d2 = std::chrono::duration_cast<std::chrono::microseconds>( t5 - t4 ).count();
		auto d3 = std::chrono::duration_cast<std::chrono::microseconds>( t6 - t5 ).count();
		std::cout << "TIMES: " << duration1 << " and " << duration2 << " and " << duration3 << "\n";
		std::cout << "NOYES: " << noC << " and " << yesC << "\n";
		if (!changedInput){break;}
		std::cout << "Match: " << pfstr << " into "<< newPostfix << '\n';
		
		maxSteps--;

	}
	return "Hi World!!!!!";
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
	std::cout << "input: "<< str << "\n";
	jsonmessage = "";
	getAnswer(str);
	
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
               Nan::New("answer").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(GetAnswer)
                   ->GetFunction(context)
                   .ToLocalChecked());
}

NODE_MODULE(helloarray, Init)