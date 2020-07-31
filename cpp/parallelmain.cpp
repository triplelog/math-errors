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
bool answerIsFinished;
struct RawQuestion {
	std::string qH = "";
	std::string qC = "";
	flat_hash_map<char,std::string> rangeMap;
	std::vector<std::vector<std::string>> rawRules;
};
struct Question {
	std::string text = "";
	std::string comp = "";
	std::vector<std::vector<std::string>> rawRules;
};
struct Answer {
	bool finished = false;
	bool correct = false;
	std::string next = "";
	std::string input = "";
	std::vector<std::string> errors;
};
struct Rule {
	std::string operands = "";
	std::string out = "";
	std::string type = "";
	std::string explanation = "";
	std::vector<std::string> constraints;
	int score = 0;
	int id;
};
struct Step {
	std::string next = "";
	int rule;
};
std::vector<Step> applyRulesVectorOnePart(std::string onePart,std::vector<int> oneIndex, std::string userFullString, bool isCorrect);


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


std::vector<std::vector<Step>> makeTree(std::string pfstr){
	flat_hash_map<std::string,std::vector<std::string>> listMap;
	flat_hash_map<int,int> operandMap;
	flat_hash_map<int,std::string> originalMap;
    std::vector<Step> returnStringsCorrect;
    std::vector<Step> returnStringsIncorrect;
	int i; int ii; int iii;
	int idx =0;
	bool startOperands = false;
	std::string currentOperator = "";
	int iidx = 0;
	bool midBrackets = false;
	answerIsFinished = true;
	
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

	
	for (i=0;i<pfstr.length();i++){
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
				
				if (mychar == '+'){
					std::vector<int> allSums ={startLeftIndex,maxi,maxi,i};
					bool moreTerms = true;
					int whileI =0;
					//std::cout << pfstr << " and " << allSums[0] << " and " << allSums[3] << "\n";
					while (moreTerms){
						moreTerms = false;
						for (whileI=0;whileI<allSums.size()/2;whileI++){
							if (pfstr.at(allSums[whileI*2+1]-1) == '+'){
								moreTerms = true;
								int tempMax = allSums[whileI*2+1]-1;
								for (ii=0;ii<tempMax;ii++){
									std::string s = "";
									std::string t = "";
									for (iii=ii;iii<tempMax;iii++){
										s += pfstr.at(iii);
										if (pfstr.at(iii) == '#'){
											t += originalMap[operandMap[iii]] + '_';
										}
									}
									if (listMap.find(s + '@' + t) != listMap.end()){
										allSums[whileI*2+1]=ii;
										allSums.push_back(ii);
										allSums.push_back(tempMax);
										break;
									}
								}
								break;
							}
						}
					}
					//if (allSums.size()>4){
					//	for (ii=0;ii<allSums.size();ii++){
					//		std::cout << ii << " with "<< allSums[ii] << "\n";
					//	}
					//}
					std::vector<std::string> possStr;
					
					
				}
				
				
				
				int fss = firstS.size();
				int sss = secondS.size();	
				std::string nFirst = "0";
				std::string nSecond = "0";	
				//std::cout << "new size: " << fss << " * " << sss << " by " << firstStr + secondStr + pfstr.at(i) + "@" + firstTtr + secondTtr << "\n";
				fullTrees.resize(ftSz+5+sss*fss*2*5);
				//condensed
				fullTrees[ftSz] = "#";
				ftSz++;

				std::string bless = firstStr + secondStr + pfstr.at(i) + '@' + firstTtr + secondTtr;

			
				fullTrees[ftSz] = "{"+bless+"}_";
				ftSz++;
				fullTrees[ftSz] = "0";
				ftSz++;
				
				fullTrees[ftSz] = firstStr + secondStr + pfstr.at(i);
				ftSz++;
				fullTrees[ftSz] = firstTtr + secondTtr;
				ftSz++;
				
				
				
				//50 ms to here from recent continue

				
				
				for (ii=0;ii<fss;ii++){
					nFirst = listMap[firstListMapKey][ii*5+2];
					if (nFirst=="4"){
						continue;
					}
					
					for (iii=0;iii<sss;iii++){
				
						nSecond = listMap[secondListMapKey][iii*5+2];
						if (nSecond=="4"){
							continue;
						}
						
						//2 ms
						
						
						if (nSecond=="3" || nFirst=="3"){
							
							continue;
						}
						
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

						//std::vector<int> tempV;
						//tempV = {startLeftIndex,i+1-startLeftIndex,startRightIndex,rightLength};
						if (!checkAnswer(firstS[ii] + secondS[iii] + pfstr.at(i) + '@' + firstT[ii] + secondT[iii])){
							answerIsFinished = false;
						}
						
						auto a1 = std::chrono::high_resolution_clock::now();
						//TODO: make this parallel
						//std::thread th1(apply1,firstS[ii] + secondS[iii] + pfstr.at(i) + '@' + firstT[ii] + secondT[iii],tempV,pfstr,isCorrect);
						//th1.join();
						
						//pp = tp.push(apply1,firstS[ii] + secondS[iii] + pfstr.at(i) + '@' + firstT[ii] + secondT[iii],tempV,pfstr,isCorrect);
						//pp.get();
						//std::future<bool> fut = std::async(apply1,firstS[ii] + secondS[iii] + pfstr.at(i) + '@' + firstT[ii] + secondT[iii],tempV,pfstr,isCorrect);
						//fut.get();
						//apply1(0,firstS[ii] + secondS[iii] + pfstr.at(i) + '@' + firstT[ii] + secondT[iii],tempV,pfstr,isCorrect);
						std::vector<Step> someStringsC = applyRulesVectorOnePart(firstS[ii] + secondS[iii] + pfstr.at(i) + '@' + firstT[ii] + secondT[iii],{startLeftIndex,i+1-startLeftIndex,startRightIndex,rightLength},pfstr,true);
						std::vector<Step> someStringsI = applyRulesVectorOnePart(firstS[ii] + secondS[iii] + pfstr.at(i) + '@' + firstT[ii] + secondT[iii],{startLeftIndex,i+1-startLeftIndex,startRightIndex,rightLength},pfstr,false);
						
						int iiiiii;
						for (iiiiii=0;iiiiii<someStringsC.size();iiiiii++){
							returnStringsCorrect.push_back(someStringsC[iiiiii]);
						}
						for (iiiiii=0;iiiiii<someStringsI.size();iiiiii++){
							returnStringsIncorrect.push_back(someStringsI[iiiiii]);
						}
						auto a2 = std::chrono::high_resolution_clock::now();
						duration2 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
						
						

						
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
						
				
						/*
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
					
					

							std::vector<std::string> someStrings = applyRulesVectorOnePart(secondS[iii] + firstS[ii]  + pfstr.at(i) + '@' + secondT[iii] + firstT[ii],{startLeftIndex,i+1-startLeftIndex,startRightIndex,rightLength},pfstr,isCorrect);
							int iiiiii;
							for (iiiiii=0;iiiiii<someStrings.size();iiiiii++){
								returnStrings.push_back(someStrings[iiiiii]);
							}
						}*/
						//62 ms to here from the 18 ms marker
						
					}
					
					
				}
				
				
				
			
			
			}
			else {
				fullTrees.resize(ftSz+5+secondS.size()*1*5);
				
				fullTrees[ftSz] = "#";
				ftSz++;

				std::string bless = secondStr + pfstr.at(i) + '@' + secondTtr;

			
				fullTrees[ftSz] = "{"+bless+"}_";
				ftSz++;
				fullTrees[ftSz] = "0";
				ftSz++;
				
				fullTrees[ftSz] = secondStr + pfstr.at(i);
				ftSz++;
				fullTrees[ftSz] = secondTtr;
				ftSz++;
				
				for (iii=0;iii<secondS.size();iii++){
				
					if (listMap[secondListMapKey][iii*5+2]=="4"){
						continue;
					}
				
					
					
					
					
				
				
				
					if (listMap[secondListMapKey][iii*5+2]=="3"){
						continue;
					}
					
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
					if (!checkAnswer(secondS[iii] + pfstr.at(i) + '@' + secondT[iii])){
						answerIsFinished = false;
					}
					auto a1 = std::chrono::high_resolution_clock::now();
					//TODO: make this parallel
					//std::vector<int> tempV;
					//tempV = {startLeftIndex,i+1-startLeftIndex,startRightIndex,rightLength};
					
					//apply2(0,secondS[iii] + pfstr.at(i) + '@' + secondT[iii],tempV,pfstr,isCorrect);
					//pp = tp.push(apply2,secondS[iii] + pfstr.at(i) + '@' + secondT[iii],tempV,pfstr,isCorrect);
					//pp.get();
						
						
					//std::thread th2(apply2,secondS[iii] + pfstr.at(i) + '@' + secondT[iii],tempV,pfstr,isCorrect);
					//th2.join();
					std::vector<Step> someStringsC = applyRulesVectorOnePart(secondS[iii] + pfstr.at(i) + '@' + secondT[iii],{startLeftIndex,i+1-startLeftIndex,startRightIndex,rightLength},pfstr,true);
					std::vector<Step> someStringsI = applyRulesVectorOnePart(secondS[iii] + pfstr.at(i) + '@' + secondT[iii],{startLeftIndex,i+1-startLeftIndex,startRightIndex,rightLength},pfstr,false);
					
					int iiiiii;
					for (iiiiii=0;iiiiii<someStringsC.size();iiiiii++){
						returnStringsCorrect.push_back(someStringsC[iiiiii]);
					}
					for (iiiiii=0;iiiiii<someStringsI.size();iiiiii++){
						returnStringsIncorrect.push_back(someStringsI[iiiiii]);
					}
					auto a2 = std::chrono::high_resolution_clock::now();
					duration2 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
					
					
					
					int numOperations = 0; int ni;
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
			
			//auto a3 = std::chrono::high_resolution_clock::now();
			
			listMap[fullStr]=fullTrees;
			
			//auto a4 = std::chrono::high_resolution_clock::now();
			//duration3 += std::chrono::duration_cast<std::chrono::microseconds>( a4 - a3 ).count();
			

			
			

			
			

			
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
	/*
	returnStrings = returnStrings1;
	returnStrings.resize(returnStrings1.size()+returnStrings2.size());
	for (ii=0;ii<returnStrings2.size();ii++){
		returnStrings[ii+returnStrings1.size()]=returnStrings2[ii];
	}
	returnStrings1.resize(0);
	returnStrings2.resize(0);*/

	return {returnStringsCorrect,returnStringsIncorrect};
	

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

bool checkAnswer(std::string answer){
	std::string key = "";
	std::string userString = answer;
	int startAt =0; int ii; int iii; int iiii;
	bool correct = true;
	for (ii=0;ii<answer.length();ii++){
		if (answer.at(ii) == '@'){
			startAt = ii+1;
			break;
		}
		else {
			key += answer.at(ii);
		}
	}
	if (answerConstraints.find(key) != answerConstraints.end()){
		int ruleIdx;
		for (ruleIdx=0;ruleIdx<answerConstraints[key].size();ruleIdx++){
			Rule rule = answerConstraints[key][ruleIdx];
			bool match = false;

			std::string currentOperand = "";
			flat_hash_map<char,std::string> partMap;
			std::vector<std::string> userOperands;
			std::vector<std::string> ruleOperands;
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
			bool midBracket = false;
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
	
			bool pastKey = false;
			if (!ignoreThis){
				for (iiii=0;iiii<rule.constraints.size();iiii++){
					pastKey = false;
					std::string constraintFix = "";
					currentOperand = "";
			
					for (iii=0;iii<rule.constraints[iiii].length();iii++){
						if (pastKey){
							if (rule.constraints[iiii].at(iii) == '_'){
								if (currentOperand.length()==1 && currentOperand.at(0) <='Z' && currentOperand.at(0) >= 'A'){
									constraintFix += partMap[currentOperand.at(0)] + '_';
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
						ignoreThis = true;
						break;
					}
				}
			}
			if (!ignoreThis){
				match = true;
			}
			
			if (match && rule.type == "i"){
				correct = false;
				break;
			}
			if (match && rule.type == "c"){
				if (constraintsMet.find(key) != constraintsMet.end()){
					for(ii=0;ii<constraintsMet[key].size();ii++){
						if (ruleIdx == constraintsMet[key][ii]){
							break;
						}
						if (ii==constraintsMet[key].size()-1){
							constraintsMet[key].push_back(ruleIdx);
							break;
						}
					}
					
				}
				else {
					constraintsMet[key] = {ruleIdx};
				}
				
			}
		}
	}
	return correct;

}

bool doubleCheckAnswer(std::string pfstr){
	flat_hash_map<std::string,std::vector<std::string>> listMap;
	flat_hash_map<int,int> operandMap;
	flat_hash_map<int,std::string> originalMap;
	std::vector<std::string> lastVector;
	int i; int ii; int iii;
	int idx =0;
	bool startOperands = false;
	std::string currentOperator = "";
	int iidx = 0;
	bool midBrackets = false;
	answerIsFinished = true;
	constraintsMet.clear();
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

	for (i=0;i<pfstr.length();i++){
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
				
				if (mychar == '+'){
					std::vector<int> allSums ={startLeftIndex,maxi,maxi,i};
					bool moreTerms = true;
					int whileI =0;
					//std::cout << pfstr << " and " << allSums[0] << " and " << allSums[3] << "\n";
					while (moreTerms){
						moreTerms = false;
						for (whileI=0;whileI<allSums.size()/2;whileI++){
							if (pfstr.at(allSums[whileI*2+1]-1) == '+'){
								moreTerms = true;
								int tempMax = allSums[whileI*2+1]-1;
								for (ii=0;ii<tempMax;ii++){
									std::string s = "";
									std::string t = "";
									for (iii=ii;iii<tempMax;iii++){
										s += pfstr.at(iii);
										if (pfstr.at(iii) == '#'){
											t += originalMap[operandMap[iii]] + '_';
										}
									}
									if (listMap.find(s + '@' + t) != listMap.end()){
										allSums[whileI*2+1]=ii;
										allSums.push_back(ii);
										allSums.push_back(tempMax);
										break;
									}
								}
								break;
							}
						}
					}
					//if (allSums.size()>4){
					//	for (ii=0;ii<allSums.size();ii++){
					//		std::cout << ii << " with "<< allSums[ii] << "\n";
					//	}
					//}
					std::vector<std::string> possStr;
					
					
				}
				
				

				
				int fss = firstS.size();
				int sss = secondS.size();	
				std::string nFirst = "0";
				std::string nSecond = "0";	
				//std::cout << "new size: " << fss << " * " << sss << " by " << firstStr + secondStr + pfstr.at(i) + "@" + firstTtr + secondTtr << "\n";
				fullTrees.resize(ftSz+5+sss*fss*2*5);
				//condensed
				fullTrees[ftSz] = "#";
				ftSz++;

				std::string bless = firstStr + secondStr + pfstr.at(i) + '@' + firstTtr + secondTtr;

			
				fullTrees[ftSz] = "{"+bless+"}_";
				ftSz++;
				fullTrees[ftSz] = "0";
				ftSz++;
				
				fullTrees[ftSz] = firstStr + secondStr + pfstr.at(i);
				ftSz++;
				fullTrees[ftSz] = firstTtr + secondTtr;
				ftSz++;
				
				
				
				//50 ms to here from recent continue

				
				
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
						
						
						if (nSecond=="3" || nFirst=="3"){
							
							continue;
						}
						
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

						if (!checkAnswer(firstS[ii] + secondS[iii]  + pfstr.at(i) + "@" + firstT[ii] + secondT[iii])){
							return false;
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
							if (!checkAnswer(secondS[iii] + firstS[ii] +  pfstr.at(i) + "@" + secondT[iii] + firstT[ii])){
								return false;
							}
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
					
					
							
						}
						//62 ms to here from the 18 ms marker
						
					}
					
					
				}
				
				
				
			
			
			}
			else {
				fullTrees.resize(ftSz+5+secondS.size()*1*5);
				
				fullTrees[ftSz] = "#";
				ftSz++;

				std::string bless = secondStr + pfstr.at(i) + '@' + secondTtr;

			
				fullTrees[ftSz] = "{"+bless+"}_";
				ftSz++;
				fullTrees[ftSz] = "0";
				ftSz++;
				
				fullTrees[ftSz] = secondStr + pfstr.at(i);
				ftSz++;
				fullTrees[ftSz] = secondTtr;
				ftSz++;
				
				for (iii=0;iii<secondS.size();iii++){
				
					if (listMap[secondListMapKey][iii*5+2]=="4"){
						continue;
					}
				
					
					
					
					
				
				
				
					if (listMap[secondListMapKey][iii*5+2]=="3"){
						continue;
					}
					
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
					
					
					
					int numOperations = 0; int ni;
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
					
					if (!checkAnswer(secondS[iii] +  pfstr.at(i) + "@" + secondT[iii])){
						return false;
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
					
				
					
				}
			}
		

			

			//std::cout << "fullTrees size: " << fullTrees.size() << " @ " << i << "\n";
			std::string fullStr = firstStr + secondStr + pfstr.at(i) + '@' + firstTtr + secondTtr;
			
		
			//Parent Node
			std::string opStr = "";
			opStr += pfstr.at(i);
			fullTrees.resize(ftSz);

			listMap[fullStr]=fullTrees;
			lastVector = fullTrees;

			

			
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
			lastVector = {"#",originalMap[idx]+'_',"0",firstRemed,secondRemed};
			operandMap[i]=idx;
			idx++;
		}
		
	}
	
	//for (ii=0;ii<lastVector.size()/5;ii++){
	//	checkAnswer(lastVector[ii*5]+"@"+lastVector[ii*5+1])
	//}
	for (flat_hash_map<std::string,std::vector<Rule>>::iterator iter = answerConstraints.begin(); iter != answerConstraints.end(); ++iter){
		std::string key = iter->first;
		for (i=0;i<answerConstraints[key].size();i++){
			if (answerConstraints[key][i].type == "c"){
				bool cMatch = false;
				if (constraintsMet.find(key) == constraintsMet.end()){
					return false;
				}
				for (ii=0;ii<constraintsMet[key].size();ii++){
					if (constraintsMet[key][ii] == i){
						cMatch = true;
						break;
					}
				}
				if (!cMatch){
					return false;
				}
			}
		}
	}
	

	return true;
	

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
	ridx = 0;
	makeRules("derivatives.csv");
	makeRules("arithmetic.csv");
	
	auto t2 = std::chrono::high_resolution_clock::now();
}

flat_hash_map<std::string,std::vector<int>> answerListMap;
flat_hash_map<std::string,std::vector<int>> answerListMapF;
flat_hash_map<std::string,std::vector<Step>> reverseMap;
flat_hash_map<std::string,std::vector<Step>> reverseMapCorrect;
int totalAnswers;
std::vector<std::string> finishedAnswers;
std::vector<std::string> unfinishedAnswers;
std::vector<std::string> correctAnswers;
std::vector<std::string> finishedErrors;
std::vector<std::string> unfinishedErrors;
std::vector<std::string> unfinishedCorrect;
flat_hash_map<std::string,Answer> answerMap;
int maxFound;
int maxSteps;


bool getAnswerList(std::string s, int nSteps) {

	if (nSteps > maxFound){
		maxFound = nSteps;
	}
	if (nSteps >= maxSteps){
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

	
	newPostfix = removeBracketsOne(newPostfix);
	
	//std::cout << s << " before pl\n";
	auto a1 = std::chrono::high_resolution_clock::now();
	std::vector<std::vector<Step>> someStrings = makeTree(newPostfix);
	
	if (answerIsFinished){
		finishedAnswers.push_back(newPostfix);
		//std::cout << newPostfix << "\n";
	}
	else {
		unfinishedAnswers.push_back(newPostfix);
	}
	auto a2 = std::chrono::high_resolution_clock::now();
	int dd1 = std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();

	duration1 += dd1;


	
	//std::cout << dd1 << "  ";
	//std::cout << s << " after pl\n";

	std::vector<Step> allStrings; //vector of the next step
	flat_hash_map<std::string,bool> uniqueStrings;

	
	for (iii=0;iii<someStrings[0].size();iii++){
		someStrings[0][iii].next = removeBracketsOne(someStrings[0][iii].next);
		if (uniqueStrings.find(someStrings[0][iii].next) != uniqueStrings.end()){
	
		}
		else {
			Step step;
			step.next = someStrings[0][iii].next;
			step.rule = someStrings[0][iii].rule;
			allStrings.push_back(step);
			uniqueStrings[someStrings[0][iii].next]=true;
		}
	
	}
	
	answerListMap[newPostfix] = {};
	answerListMapF[newPostfix] = {};
	//totalAnswers += allStrings.size();
	
	for (ii=0;ii<allStrings.size();ii++){
		if (allStrings[ii].next == newPostfix){
			continue;
		}
		if (answerListMap.find(allStrings[ii].next) != answerListMap.end()){
			Step step;
			step.next = newPostfix;
			step.rule = allStrings[ii].rule;
			reverseMapCorrect[allStrings[ii].next].push_back(step);
			
		}
		else {
			getAnswerList(allStrings[ii].next,nSteps+1);
			Step step;
			step.next = newPostfix;
			step.rule = allStrings[ii].rule;
			reverseMapCorrect[allStrings[ii].next]={step};

		}

	}
	
	
	//totalAnswers += allStrings.size();
	//std::cout << "total answers: "<< totalAnswers << "\n";
	
	//allStrings.resize(0);
	for (iii=0;iii<someStrings[1].size();iii++){
		someStrings[1][iii].next = removeBracketsOne(someStrings[1][iii].next);
		if (uniqueStrings.find(someStrings[1][iii].next) != uniqueStrings.end()){
	
		}
		else {
			Step step;
			step.next = someStrings[1][iii].next;
			step.rule = someStrings[1][iii].rule;
			allStrings.push_back(step);
			uniqueStrings[someStrings[1][iii].next]=true;
		}
	
	}
	
	
	totalAnswers += allStrings.size();
	//std::cout << "total answers: "<< totalAnswers << "\n";
	for (ii=0;ii<allStrings.size();ii++){
		answerListMapF[newPostfix].push_back(allStrings[ii].rule);
		if (allStrings[ii].next == newPostfix){
			continue;
		}
		if (answerListMapF.find(allStrings[ii].next) != answerListMapF.end()){
			Step step;
			step.next = newPostfix;
			step.rule = allStrings[ii].rule;
			reverseMap[allStrings[ii].next].push_back(step);
			
		}
		else {
			getAnswerList(allStrings[ii].next,nSteps+1);
			Step step;
			step.next = newPostfix;
			step.rule = allStrings[ii].rule;
			reverseMap[allStrings[ii].next]={step};

		}

	}
	
	return true;
		
	
}

#include "autocomplete.cpp"

flat_hash_map<std::string,std::vector<Step>> correctSolutionList;
flat_hash_map<std::string,std::vector<Step>> incorrectSolutionList;
std::vector<Step> makeSolutionList(std::string s, std::string q){
	std::vector<Step> v;
	//std::cout << "s: " << s << "\n";
	std::vector<Step> sv;
	int i; 
	if (s == q){
		Step step;
		step.next = s;
		step.rule = -1;
		v = {step};
		correctSolutionList[s]=v;
		//std::cout << "sa: " << s << " and vsz: " << v.size() << "\n";
		return v;
	}
	else {
		Step step;
		step.next = "";
		step.rule = -1;
		correctSolutionList[s]={step};
	}
	if (reverseMapCorrect.find(s) != reverseMapCorrect.end()){
		sv = reverseMapCorrect.find(s)->second;
	}
	else {
		v = {};
		correctSolutionList[s]=v;
		return v;
	}
	//std::cout << "svszb: " << sv.size() << "\n";

	if (sv.size() ==0){
		v = {};
		correctSolutionList[s]=v;
		//std::cout << "sb: " << s << " and vsz: " << v.size() << "\n";
		return v;
	}
	//std::cout << "sv0: " << sv[0] << "\n";
	
	int minSize = 100000; int l; int idx = 0;
	std::vector<Step> minV;
	int ruleApp;
	for (i=0;i<sv.size();i++){
		//std::cout << "i: " << i << " and " << sv[i*2] << "\n";
		if (correctSolutionList.find(sv[i].next) != correctSolutionList.end()){
			if (correctSolutionList[sv[i].next].size()==1 && correctSolutionList[sv[i].next][0].next == ""){
				continue;
			}
		}
		else {
			makeSolutionList(sv[i].next,q);
		}
		l = correctSolutionList[sv[i].next].size();
		if (l == 0){
			continue;
		}
		if (l < minSize){
			minSize = l;
			minV = correctSolutionList[sv[i].next];
			ruleApp = sv[i].rule;
		}
	}
	if (minSize == 100000){
		v = {};
		correctSolutionList[s]=v;
		//std::cout << "sb: " << s << " and vsz: " << v.size() << "\n";
		return v;
	}

	for (i=0;i<minSize;i++){
		if (i==minSize-1){
			minV[i].rule = ruleApp;
		}
		v.push_back(minV[i]);
	}
	Step step;
	step.next = s;
	step.rule = -1;
	v.push_back(step);
	correctSolutionList[s]=v;
	//std::cout << "sc: " << s << " and vsz: " << v.size() << "\n";
	return v;
}

std::vector<Step> makeIncorrectSolutionList(std::string s, std::string q){
	std::vector<Step> v;
	//std::cout << "s: " << s << "\n";
	std::vector<Step> sv;
	int i; 
	if (s == q){
		Step step;
		step.next = s;
		step.rule = -1;
		v = {step};
		incorrectSolutionList[s]=v;
		//std::cout << "sa: " << s << " and vsz: " << v.size() << "\n";
		return v;
	}
	else {
		Step step;
		step.next = "";
		step.rule = -1;
		incorrectSolutionList[s]={step};
	}
	if (reverseMap.find(s) != reverseMap.end()){
		sv = reverseMap.find(s)->second;
	}
	else {
		v = {};
		incorrectSolutionList[s]=v;
		return v;
	}
	//std::cout << "svszb: " << sv.size() << "\n";

	if (sv.size() ==0){
		v = {};
		incorrectSolutionList[s]=v;
		//std::cout << "sb: " << s << " and vsz: " << v.size() << "\n";
		return v;
	}
	//std::cout << "sv0: " << sv[0] << "\n";
	
	int minSize = 100000; int l; int idx = 0;
	std::vector<Step> minV;
	for (i=0;i<sv.size();i++){
		//std::cout << "i: " << i << " and " << sv[i*2] << "\n";
		if (incorrectSolutionList.find(sv[i].next) != incorrectSolutionList.end()){
			if (incorrectSolutionList[sv[i].next].size()==1 && incorrectSolutionList[sv[i].next][0].next == ""){
				continue;
			}
		}
		else {
			makeIncorrectSolutionList(sv[i].next,q);
		}
		l = incorrectSolutionList[sv[i].next].size();
		if (l == 0){
			continue;
		}
		if (l < minSize){
			minSize = l;
			minV = incorrectSolutionList[sv[i].next];
		}
	}
	if (minSize == 100000){
		if (correctSolutionList.find(s) != correctSolutionList.end()){
			v=correctSolutionList[s];
			incorrectSolutionList[s]=v;
		}
		else {
			v = {};
			incorrectSolutionList[s]=v;
		}
		
		//std::cout << "sb: " << s << " and vsz: " << v.size() << "\n";
		return v;
	}
	for (i=0;i<minSize;i++){
		v.push_back(minV[i]);
	}
	Step step;
	step.next = s;
	step.rule = -1;
	v.push_back(step);
	incorrectSolutionList[s]=v;
	//std::cout << "sc: " << s << " and vsz: " << v.size() << "\n";
	return v;
}

std::string fullAnswer(std::string s){
	std::string newPostfix = removeBracketsOne(s);
	std::cout << "\n\nStarting the Loop @$*&^@$*&^@*$&^@*$&^\n\n";
	reverseMap.clear();
	reverseMapCorrect.clear();
	auto a1 = std::chrono::high_resolution_clock::now();
	getAnswerList(newPostfix,0);
	auto a2 = std::chrono::high_resolution_clock::now();
	std::cout << "\n\n\n\nCompleted the InCorrect Loop @$*&^@$*&^@*$&^@*$&^\n\n\n\n" << " and " << std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count() << "\n\n\n";
	std::cout << "total answers: "<< totalAnswers << "\n";
	//duration2 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	std::cout << "\n\nCompleted the Loop @$*&^@$*&^@*$&^@*$&^\n\n";
	int i; int ii;
	
	a1 = std::chrono::high_resolution_clock::now();
	std::cout << "finished answers: " << finishedAnswers.size() << "\n";
	std::cout << "unfinished answers: " << unfinishedAnswers.size() << "\n";
	

	for (ii=0;ii<finishedAnswers.size();ii++){
		if (doubleCheckAnswer(finishedAnswers[ii])){
			
			std::vector<Step> v = makeSolutionList(finishedAnswers[ii],newPostfix);
			int vsz = v.size();
			if (vsz > 0){
				//std::cout << "fully correct: "<< tempFinished[ii] << "\n";
				correctAnswers.push_back(finishedAnswers[ii]);
				Answer answer;
				answer.finished = true;
				answer.correct = true;
				if (vsz > 1){
					answer.next = v[vsz-2].next;
				}
				answerMap[finishedAnswers[ii]]=answer;
				
			}
			else {
				finishedErrors.push_back(finishedAnswers[ii]);
				Answer answer;
				answer.finished = true;
				answer.correct = false;
				if (vsz > 1){
					answer.next = v[vsz-2].next;
				}
				answerMap[finishedAnswers[ii]]=answer;
			}
		}
		else {

			unfinishedAnswers.push_back(finishedAnswers[ii]);
		}
	}
	std::cout << "unfinished answers: " << unfinishedAnswers.size() << "\n";
	finishedAnswers.resize(0);

	for (ii=0;ii<unfinishedAnswers.size();ii++){
		
		std::vector<Step> v = makeSolutionList(unfinishedAnswers[ii],newPostfix);
		int vsz = v.size();
		if (vsz > 0){
			unfinishedCorrect.push_back(unfinishedAnswers[ii]);
			Answer answer;
			answer.finished = false;
			answer.correct = true;
			if (vsz > 1){
				answer.next = v[vsz-2].next;
			}
			answerMap[unfinishedAnswers[ii]]=answer;
		}
		else {
			std::vector<Step> vv = makeIncorrectSolutionList(unfinishedAnswers[ii],newPostfix);
			vsz = vv.size();
			if (vsz > 0){
				unfinishedErrors.push_back(unfinishedAnswers[ii]);
				Answer answer;
				answer.finished = false;
				answer.correct = true;
				if (vsz > 1){
					answer.next = vv[vsz-2].next;
				}
				answerMap[unfinishedAnswers[ii]]=answer;
			}
			else {
				std::cout << "no solution found? " << unfinishedAnswers[ii] << "\n";
			}
		}
		
	}
	//TODO: loop through the finished errors to collect all errors
	
	unfinishedAnswers.resize(0);


	std::cout << "correct answers: " << correctAnswers.size() << "\n";
	std::cout << "unfinished errors: " << unfinishedErrors.size() << "\n";
	std::cout << "unfinished correct: " << unfinishedCorrect.size() << "\n";
	std::cout << "finished errors: " << finishedErrors.size() << "\n";
	
	
	
	//for (flat_hash_map<std::string,std::vector<std::string>>::iterator iter = reverseMapCorrect.begin(); iter != reverseMapCorrect.end(); ++iter){
	//	std::cout << "rm: " << iter->first << " and " << iter->second.size() << "\n";		
	//}
	
	
	a2 = std::chrono::high_resolution_clock::now();
	std::cout << "time to find correct answers: " << " and " << std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count() << "\n\n\n";
	
	std::string error = "Don't know.";
	int ui = 0;
	
	
	
	std::cout << "in\n";
	inputify();
	//for (flat_hash_map<std::string,Answer>::iterator iter = answerMap.begin(); iter != answerMap.end(); ++iter){
	//	inputArray.push_back(inputify(iter->first));
	//}
	auto a3 = std::chrono::high_resolution_clock::now();
	std::cout << "time to inputify answers: " << " and " << std::chrono::duration_cast<std::chrono::microseconds>( a3 - a2 ).count() << "\n\n\n";
	
	
	
	
	
	
	/*
	if (reverseMap.find(mpf) != reverseMap.end()){
		error = "Found";
		std::string oneStep = mpf;
		std::cout << oneStep << "\n";
		jsonmessage = "";
		while (reverseMap.find(oneStep) != reverseMap.end() && oneStep != newPostfix){
			std::string rawRule = reverseMap[oneStep][1];
			
			std::string key = "";
			int ruleIdx = 0;
			bool isSecond = false;
			for (ii=0;ii<rawRule.length();ii++){
				if (rawRule.at(ii) == ','){
					isSecond = true;
				}
				else if (isSecond){
					ruleIdx *= 10;
					ruleIdx += (rawRule.at(ii) - '0');
				}
				else {
					key += rawRule.at(ii);
				}
			}
			std::cout << "key: " << key << " and ruleIdx: " << ruleIdx << " from: " << rawRule << "\n";
			std::vector<std::string> rule = rules[key][ruleIdx];
			if (rule[2] != "c"){
				std::cout << "The error is: "<< rule[3] << "\n";
			}
			
			outputTree(oneStep);
			oneStep = reverseMap[oneStep][0];
		}
	}*/

	return error;
}


/*
bool correctAnswer(std::string s){
	//std::cout << "input: " << s << "\n";
	std::string newPostfix = removeBracketsOne(s);
	//std::cout << "postfixed: " << postfixify(s) << "\n";
	std::cout << "\n\n\n\nStarting the Loop @$*&^@$*&^@*$&^@*$&^\n\n\n\n";
	mapSave = 0; mapMake = 0;
	answerListMap.clear();
	reverseMap.clear();
	correctSolutionList.clear();
	auto a1 = std::chrono::high_resolution_clock::now();
	totalAnswers = 0;
	getAnswerList(newPostfix,true,0);
	auto a2 = std::chrono::high_resolution_clock::now();
	//duration1 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	std::cout << "\n\n\n\nCompleted the Correct Loop @$*&^@$*&^@*$&^@*$&^\n\n\n\n" << totalAnswers << " and " << std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count() << "\n\n\n";
	int i; int ii; int iii; int iiii;

	
	int minLen = 10000;
	int minIdx = 0;
	bool isCorrect = false;
	int ui = 0;


	std::vector<std::string> tempCorrect = correctAnswers;
	correctAnswers.resize(0);
	
	//for (flat_hash_map<std::string,std::vector<std::string>>::iterator iter = reverseMap.begin(); iter != reverseMap.end(); ++iter){
		//std::cout << "rm: " << iter->first << " and " << iter->second.size() << "\n";		
	//}
	
	a1 = std::chrono::high_resolution_clock::now();
	
	correctSolutionList[newPostfix]={newPostfix};
	for (ii=0;ii<tempCorrect.size();ii++){
		if (doubleCheckAnswer(tempCorrect[ii])){
			correctAnswers.push_back(tempCorrect[ii]);
			//std::cout << "correct: " << tempCorrect[ii] << "\n";
			answerListMap.erase(tempCorrect[ii]);
			//std::cout << "erased: " << tempCorrect[ii] << "\n";
			std::vector<std::string> v = makeSolutionList(tempCorrect[ii]);
			//std::cout << "made solution list: " << tempCorrect[ii] << "\n";
			//std::cout << "len of sol: " << v.size() << "\n";
		}

	}
	
	a2 = std::chrono::high_resolution_clock::now();
	std::cout << "time to makesolutionlist: " << std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count() << "\n\n\n";
	
	

	for (flat_hash_map<std::string,std::vector<std::string>>::iterator iter = answerListMap.begin(); iter != answerListMap.end(); ++iter){
		unfinishedAnswers.push_back(iter->first);
	}
	std::cout << "correct answers: " << correctAnswers.size() << " choices"<< "\n";
	std::cout << "unfinished answers: " << unfinishedAnswers.size() << " choices"<< "\n";

	return isCorrect;
}
*/
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
Question currentQuestion;
void CheckAnswer(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string a(*s);

	std::string mpf = postfixify(a);
	std::cout << "your answer: " << mpf << "\n";
	int ii; int iii; int iiii;
	
	if (answerMap.find(mpf) != answerMap.end()){
		Answer userAnswer = answerMap[mpf];
		std::cout << "correct? " << userAnswer.correct <<"\n";
		std::cout << "finished? " << userAnswer.finished <<"\n";
		
	}
	else {
		std::cout << "unknown answer" << "\n";
	}
	
	
	auto a1 = std::chrono::high_resolution_clock::now();
	
	flat_hash_map<int,std::vector<int>> branches;
	for (ii=0;ii<ridx;ii++){
		branches[ii]={0,0};
	}
	for (ii=0;ii<correctAnswers.size();ii++){
		std::vector<Step> v = correctSolutionList[correctAnswers[ii]];
		flat_hash_map<int,bool> alreadyApp;
		flat_hash_map<int,bool> alreadyOpp;
		for (iii=0;iii<v.size();iii++){
			if (alreadyApp.find(v[iii].rule) != alreadyApp.end()){
			}
			else {
				//TODO: make the rule match reality
				//branches[v[iii].rule][0]++;
				alreadyApp[v[iii].rule]=true;
			}
			std::vector<int> allOptions = answerListMapF[v[iii].next];
			for (iiii=0;iiii<allOptions.size();iiii++){
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
	for (ii=0;ii<ridx;ii++){
		std::cout << branches[ii][1] << "\n";
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
			jsonmessage += "outArray.push(\""+latexOne(autoAnswers[i])+"\");\n";
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
	for (i=0;i<correctAnswers.size();i++){
		if (correctAnswers[i] == pfstr){
			std::cout << "match: " << pfstr << " and " << correctAnswers[i] << "\n";
			std::vector<Step> v = correctSolutionList[pfstr];
			bestSolution = v;
			foundSolution = true;
			break;
		}
		else {
			std::cout << "no match: " << pfstr << " and " << correctAnswers[i] << "\n";
			std::vector<Step> v = correctSolutionList[correctAnswers[i]];
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
		for (i=0;i<correctAnswers.size();i++){
			std::vector<Step> v = correctSolutionList[correctAnswers[i]];
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
		if (foundSolution){
			bestSolution = oldBest;
		}
	}
	for (i=0;i<bestSolution.size();i++){
		outputTree(bestSolution[i].next);
	}
	
	
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(jsonmessage);

	
	info.GetReturnValue().Set(h.ToLocalChecked());
}
void GetQuestion(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	
	std::vector<RawQuestion> qs = makeQuestions("answerconstraints.csv");
	currentQuestion = chooseQuestion("blank",qs);
	
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(currentQuestion.text);

	
	info.GetReturnValue().Set(h.ToLocalChecked());
}
void GetAnswers(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	
	
	finishedAnswers.resize(0);
	unfinishedAnswers.resize(0);
	
	correctAnswers.resize(0);
	unfinishedCorrect.resize(0);
	unfinishedErrors.resize(0);
	finishedErrors.resize(0);
	
	correctSolutionList.clear();
	incorrectSolutionList.clear();
	answerMap.clear();
	maxSteps = 25;
	
	auto a1 = std::chrono::high_resolution_clock::now();
	maxFound = 0;
	
	std::cout << "mf:" << maxFound << " times: " << duration1 << " and " << duration2 << " and " << duration3 << "\n";
	
	std::string error = fullAnswer(currentQuestion.comp);

	auto a2 = std::chrono::high_resolution_clock::now();
	duration3 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	std::cout << "times: " << duration1 << " and " << duration2 << " and " << duration3 << "\n";
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(currentQuestion.text);

	
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
               Nan::New("question").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(GetQuestion)
                   ->GetFunction(context)
                   .ToLocalChecked());
  exports->Set(context,
               Nan::New("answers").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(GetAnswers)
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
}

NODE_MODULE(helloarray, Init)