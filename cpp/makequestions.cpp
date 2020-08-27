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

#include "commonstuff.cpp"

#include "solve.cpp"

flat_hash_map<std::string,int> answerListMap;
flat_hash_map<std::string,std::vector<int>> answerListMapF;
flat_hash_map<std::string,std::vector<Step>> reverseMap;
flat_hash_map<std::string,std::vector<Step>> reverseMapCorrect;
flat_hash_map<std::string,std::vector<Step>> correctSolutionList;
flat_hash_map<std::string,std::vector<Step>> incorrectSolutionList;
int totalAnswers;
std::vector<std::string> finishedAnswers;
flat_hash_map<std::string,bool> unfinishedOptions;

flat_hash_map<std::string,Answer> answerMap;
int maxFound;
int maxSteps;

bool foundOneAnswer;
bool startedWrong;


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
				if (ii==i-1){
					std::cout << "No match 1\n";
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
				if (maxi == 0){
					//TODO figure out why maxi is ever 0
					returnStringsCorrect.resize(0);
					returnStringsIncorrect.resize(0);
					break;
				}
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
					if (ii==maxi-1){
						std::cout << "No match 2\n";
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
						//duration2 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
						
						

						
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
					//duration2 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
					
					
					
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
	//std::cout << "ca key1: " << key << "\n";
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
	//std::cout << "ca key2: " << key << correct<< "\n";
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
	//std::cout << "pfstr: " << pfstr << "\n";
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
			if (!checkAnswer("#@" + originalMap[idx] + "_")){
				return false;
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
		//std::cout << "akey: " << key << "\n";
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


bool getAnswerList(std::string s, int nSteps) {
	//std::cout << "s: "<< s << "\n";

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

	//std::cout << "npf1: "<< newPostfix << "\n";
	newPostfix = removeBracketsOne(newPostfix);
	//std::cout << "npf2: "<< newPostfix << "\n";
	
	//std::cout << s << " before pl\n";
	auto a1 = std::chrono::high_resolution_clock::now();
	std::vector<std::vector<Step>> someStrings = makeTree(newPostfix);
	//std::cout << "npf3: "<< newPostfix << "\n";
	
	if (answerListMap.find(newPostfix) == answerListMap.end()){
		if (answerIsFinished){
			finishedAnswers.push_back(newPostfix);
			/*
			if (nSteps*2+6 < maxSteps && !startedWrong){

				if (doubleCheckAnswer(newPostfix)){
					std::cout << "One answer: " << newPostfix << " and " << maxSteps << "\n";
					if (nSteps*2+6 < maxSteps){
						maxSteps = nSteps*2+6;
					}
					std::cout << "One answer: " << newPostfix << " and " << maxSteps << "\n";
					foundOneAnswer = true;
				}
			}
			*/
		}
	}
	
	auto a2 = std::chrono::high_resolution_clock::now();
	int dd1 = std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();

	duration1 += dd1;


	
	//std::cout << dd1 << "  ";
	//std::cout << s << " after pl\n";

	std::vector<Step> allStrings; //vector of the next step
	flat_hash_map<std::string,bool> uniqueStrings;
	
	std::vector<int> pRules;
	flat_hash_map<int,bool> oldMap;
	if (answerListMapF.find(newPostfix) == answerListMapF.end()){
		answerListMap[newPostfix] = nSteps;
		answerListMapF[newPostfix] = {};
	}
	else {
		answerListMap[newPostfix] = nSteps;
		answerListMapF[newPostfix] = {};
		//pRules = answerListMapF[newPostfix];
		//for (iii=0;iii<pRules.size();iii++){
		//	oldMap[pRules[iii]]=true;
		//}
	}

		
	for (iii=0;iii<someStrings[0].size();iii++){
		someStrings[0][iii].next = removeBracketsOne(someStrings[0][iii].next);
		if (uniqueStrings.find(someStrings[0][iii].next) != uniqueStrings.end()){
	
		}
		else {
			Step step;
			step.next = someStrings[0][iii].next;
			step.rule = someStrings[0][iii].rule;
			step.startNode = someStrings[0][iii].startNode;
			step.endNode = someStrings[0][iii].endNode;
			step.startNodes = someStrings[0][iii].startNodes;
			step.endNodes = someStrings[0][iii].endNodes;
			allStrings.push_back(step);
			uniqueStrings[someStrings[0][iii].next]=true;
		}
	
	}
	//std::cout << "npf4: "<< newPostfix << "\n";
	
	//totalAnswers += allStrings.size();
	
	
	for (ii=0;ii<allStrings.size();ii++){
		if (nSteps == 0){
			std::cout << "next: " << allStrings[ii].next << "\n";
		}
		if (allStrings[ii].next == newPostfix){
			continue;
		}
		
		bool isMin = false;
		bool isClose = false;
		if (answerListMap.find(allStrings[ii].next) == answerListMap.end()){
			getAnswerList(allStrings[ii].next,nSteps+1);
			isMin = true;
		}
		else if (nSteps+1<answerListMap[allStrings[ii].next]){
			getAnswerList(allStrings[ii].next,nSteps+1);
			isMin = true;
		}
		else if (nSteps-1<answerListMap[allStrings[ii].next]){
			isClose = true;
		}
		
		if (isMin){
			Step step;
			step.next = newPostfix;
			step.rule = allStrings[ii].rule;
			step.startNode = allStrings[ii].endNode;
			step.endNode = allStrings[ii].startNode;
			step.startNodes = allStrings[ii].endNodes;
			step.endNodes = allStrings[ii].startNodes;
			reverseMapCorrect[allStrings[ii].next]={step};
		}
		else if (isClose){

			if (reverseMapCorrect.find(allStrings[ii].next) != reverseMapCorrect.end()){
				bool foundStep = false;
				for (iii=0;iii<reverseMapCorrect[allStrings[ii].next].size();iii++){
					if (reverseMapCorrect[allStrings[ii].next][iii].next == newPostfix){
						foundStep = true;
						break;
					}
				}
				if (!foundStep){
					Step step;
					step.next = newPostfix;
					step.rule = allStrings[ii].rule;
					step.startNode = allStrings[ii].endNode;
					step.endNode = allStrings[ii].startNode;
					step.startNodes = allStrings[ii].endNodes;
					step.endNodes = allStrings[ii].startNodes;
					reverseMapCorrect[allStrings[ii].next].push_back(step);
				}
			
			}
			else {
				Step step;
				step.next = newPostfix;
				step.rule = allStrings[ii].rule;
				step.startNode = allStrings[ii].endNode;
				step.endNode = allStrings[ii].startNode;
				step.startNodes = allStrings[ii].endNodes;
				step.endNodes = allStrings[ii].startNodes;
				reverseMapCorrect[allStrings[ii].next]={step};

			}
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
			step.startNode = someStrings[1][iii].startNode;
			step.endNode = someStrings[1][iii].endNode;
			step.startNodes = someStrings[1][iii].startNodes;
			step.endNodes = someStrings[1][iii].endNodes;
			allStrings.push_back(step);
			uniqueStrings[someStrings[1][iii].next]=true;
		}
	
	}
	
	
	totalAnswers += allStrings.size();
	//std::cout << "total answers: "<< totalAnswers << "\n";

	for (ii=0;ii<allStrings.size();ii++){
		startedWrong = true;
		if (allStrings[ii].next == newPostfix){
			continue;
		}
		if (allStrings[ii].rule < 0){
				std::cout << "negative ruleddd\n";
		}
		answerListMapF[newPostfix].push_back(allStrings[ii].rule);

		if (answerListMap.find(allStrings[ii].next) == answerListMap.end()){
			getAnswerList(allStrings[ii].next,nSteps+1);
		}
		else if (nSteps+1<answerListMap[allStrings[ii].next]){
			getAnswerList(allStrings[ii].next,nSteps+1);
		}
		if (reverseMap.find(allStrings[ii].next) == reverseMap.end()){
			Step step;
			step.next = newPostfix;
			step.rule = allStrings[ii].rule;
			step.startNode = allStrings[ii].endNode;
			step.endNode = allStrings[ii].startNode;
			step.startNodes = allStrings[ii].endNodes;
			step.endNodes = allStrings[ii].startNodes;
			reverseMap[allStrings[ii].next].push_back(step);
			
		}
		else {
			Step step;
			step.next = newPostfix;
			step.rule = allStrings[ii].rule;
			step.startNode = allStrings[ii].endNode;
			step.endNode = allStrings[ii].startNode;
			step.startNodes = allStrings[ii].endNodes;
			step.endNodes = allStrings[ii].startNodes;
			reverseMap[allStrings[ii].next]={step};

		}

	}
	
	return true;
		
	
}


#include "autocomplete.cpp"



std::vector<Step> makeSolutionList(std::string s, std::string q){
	std::vector<Step> v;
	//std::cout << "s: " << s << "\n";
	std::vector<Step> sv;
	int i; 
	if (s == q){
		Step step;
		step.next = s;
		step.rule = -1;
		step.startNode = 0;
		step.endNode = 0;
		step.startNodes = {};
		step.endNodes = {};
		v = {step};
		if (unfinishedOptions.find(s) == unfinishedOptions.end()){
			unfinishedOptions[s]=true;
		}
		correctSolutionList[s]=v;
		//std::cout << "sa: " << s << " and vsz: " << v.size() << "\n";
		return v;
	}
	else {
		if (correctSolutionList.find(s) == correctSolutionList.end()){
			Step step;
			step.next = "";
			step.rule = -1;
			step.startNode = 0;
			step.endNode = 0;
			step.startNodes = {};
			step.endNodes = {};
			correctSolutionList[s]={step};
		}
		
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
	int startApp;
	int endApp;
	std::vector<int> startsApp;
	std::vector<int> endsApp;
	for (i=0;i<sv.size();i++){
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
			startApp = sv[i].endNode;
			endApp = sv[i].startNode;
			startsApp = sv[i].endNodes;
			endsApp = sv[i].startNodes;
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
			minV[i].startNode = startApp;
			minV[i].endNode = endApp;
			minV[i].startNodes = startsApp;
			minV[i].endNodes = endsApp;
		}
		if (unfinishedOptions.find(minV[i].next) == unfinishedOptions.end()){
			unfinishedOptions[minV[i].next]=true;
		}
		v.push_back(minV[i]);
	}
	Step step;
	step.next = s;
	step.rule = -1;
	step.startNode = 0;
	step.endNode = 0;
	step.startNodes = {};
	step.endNodes = {};
	if (unfinishedOptions.find(s) == unfinishedOptions.end()){
		unfinishedOptions[s]=true;
	}
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
		step.startNode = 0;
		step.endNode = 0;
		step.startNodes = {};
		step.endNodes = {};
		v = {step};
		if (unfinishedOptions.find(s) == unfinishedOptions.end()){
			unfinishedOptions[s]=true;
		}
		incorrectSolutionList[s]=v;
		//std::cout << "sa: " << s << " and vsz: " << v.size() << "\n";
		return v;
	}
	else {
		Step step;
		step.next = "";
		step.rule = -1;
		step.startNode = 0;
		step.endNode = 0;
		step.startNodes = {};
		step.endNodes = {};
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
	int ruleApp;
	int startApp;
	int endApp;
	std::vector<int> startsApp;
	std::vector<int> endsApp;
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
			ruleApp = sv[i].rule;
			startApp = sv[i].endNode;
			endApp = sv[i].startNode;
			startsApp = sv[i].endNodes;
			endsApp = sv[i].startNodes;
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
		if (i==minSize-1){
			minV[i].rule = ruleApp;
			minV[i].startNode = startApp;
			minV[i].endNode = endApp;
			minV[i].startNodes = startsApp;
			minV[i].endNodes = endsApp;
		}
		if (unfinishedOptions.find(minV[i].next) == unfinishedOptions.end()){
			unfinishedOptions[minV[i].next]=true;
		}
		v.push_back(minV[i]);
	}
	Step step;
	step.next = s;
	step.rule = -1;
	step.startNode = 0;
	step.endNode = 0;
	step.startNodes = {};
	step.endNodes = {};
	if (unfinishedOptions.find(s) == unfinishedOptions.end()){
		unfinishedOptions[s]=true;
	}
	v.push_back(step);
	incorrectSolutionList[s]=v;
	//std::cout << "sc: " << s << " and vsz: " << v.size() << "\n";
	return v;
}

std::string fullAnswer(std::string s, std::string filen){
	std::string newPostfix = removeBracketsOne(s);
	std::cout << "\n\nStarting the Loop @$*&^@$*&^@*$&^@*$&^\n\n";
	
	auto a1 = std::chrono::high_resolution_clock::now();
	
	//maxSteps = 5;
	//getAnswerList(newPostfix,0);
	maxSteps = 15;
	getAnswerList(newPostfix,0);
	//maxSteps = 15;
	//getAnswerList(newPostfix,0);
	auto a2 = std::chrono::high_resolution_clock::now();
	std::cout << "\n\n\n\nCompleted the InCorrect Loop @$*&^@$*&^@*$&^@*$&^\n\n\n\n" << " and " << std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count() << "\n\n\n";
	std::cout << "total answers: "<< totalAnswers << "\n";
	//duration2 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	std::cout << "\n\nCompleted the Loop @$*&^@$*&^@*$&^@*$&^\n\n";
	int i; int ii; int iii; int iiii;
	
	a1 = std::chrono::high_resolution_clock::now();
	std::cout << "finished answers: " << finishedAnswers.size() << "\n";
	

	unfinishedOptions.clear();
	
	for (ii=0;ii<finishedAnswers.size();ii++){
		//std::cout << "f: " << finishedAnswers[ii] << "\n";
		if (doubleCheckAnswer(finishedAnswers[ii])){
			//std::cout << "cf: " << finishedAnswers[ii] << "\n";
			std::vector<Step> v = makeSolutionList(finishedAnswers[ii],newPostfix);
			int vsz = v.size();
			if (vsz > 0){
				
				Answer answer;
				answer.finished = true;
				answer.correct = true;
				if (vsz > 1){
					answer.next = v[vsz-2].next;
				}
				answer.solution = v;
				answerMap[finishedAnswers[ii]]=answer;
				
			}
			else {
				v = makeIncorrectSolutionList(finishedAnswers[ii],newPostfix);
				vsz = v.size();
				
				Answer answer;
				answer.finished = true;
				answer.correct = false;
				if (vsz > 1){
					answer.next = v[vsz-2].next;
				}
				answer.solution = v;
				answerMap[finishedAnswers[ii]]=answer;
			}
		}
	}
	int uos = 0;
	for (flat_hash_map<std::string,bool>::iterator iter = unfinishedOptions.begin(); iter != unfinishedOptions.end(); ++iter){
		if (answerMap.find(iter->first) != answerMap.end()){
			continue;
		}
		uos++;
		
		std::vector<Step> v = makeSolutionList(iter->first,newPostfix);
		int vsz = v.size();
		if (vsz > 0){
			Answer answer;
			answer.finished = false;
			answer.correct = true;
			if (vsz > 1){
				answer.next = v[vsz-2].next;
			}
			answer.solution = v;
			answerMap[iter->first]=answer;
		}
		else {
			std::vector<Step> vv = makeIncorrectSolutionList(iter->first,newPostfix);
			vsz = vv.size();
			if (vsz > 0){
				
				Answer answer;
				answer.finished = false;
				answer.correct = false;
				if (vsz > 1){
					answer.next = vv[vsz-2].next;
				}
				answer.solution = v;
				answerMap[iter->first]=answer;
			}
			else {
				std::cout << "no solution found? " << iter->first << "\n";
			}
		}

		
	}
	
	std::cout << "unfinished answers: " << uos << "\n";

	

	
	
	
	//for (flat_hash_map<std::string,std::vector<std::string>>::iterator iter = reverseMapCorrect.begin(); iter != reverseMapCorrect.end(); ++iter){
	//	std::cout << "rm: " << iter->first << " and " << iter->second.size() << "\n";		
	//}
	
	
	a2 = std::chrono::high_resolution_clock::now();
	std::cout << "time to find correct answers: " << " and " << std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count() << "\n\n\n";
	
	std::string error = "Don't know.";
	int ui = 0;
	
	
	
	std::cout << "in\n";
	inputify();
	
	std::ofstream myfile;
	myfile.open("./cpp/questions/" + filen);
	myfile << "\n";
	std::string deweyStr = "";
	if (currentQuestion.dewey.subject != "."){
		deweyStr += currentQuestion.dewey.subject;
		if (currentQuestion.dewey.topic != "."){
			deweyStr += "."+currentQuestion.dewey.topic;
			if (currentQuestion.dewey.lesson != "."){
				deweyStr += "."+currentQuestion.dewey.lesson;
			}
		}
	}
	myfile << deweyStr +"\n";
	for (flat_hash_map<std::string,Answer>::iterator iter = answerMap.begin(); iter != answerMap.end(); ++iter){
		std::string outStr = iter->first+",";
		outStr += iter->second.input+",";
		if (iter->second.correct && iter->second.finished){
			outStr += "c,";
		}
		else if (iter->second.finished){
			outStr += "e,";
		}
		else {
			outStr += "u,";
		}
		std::vector<Step> v = iter->second.solution;
		int vsz = v.size();
		for (iii=0;iii<vsz;iii++){
			outStr += v[iii].next+","+std::to_string(v[iii].rule)+","+std::to_string(v[iii].startNode)+","+std::to_string(v[iii].endNode)+",";
			outStr += "\"";
			for (iiii=0;iiii<v[iii].startNodes.size();iiii++){
				outStr += std::to_string(v[iii].startNodes[iiii]);
				if (iiii<v[iii].startNodes.size()-1){
					outStr += ",";
				}
				else {
					outStr += "\",";
				}
			}
			if (v[iii].startNodes.size()==0){
				outStr += "\",";
			}
			
			outStr += "\"";
			for (iiii=0;iiii<v[iii].endNodes.size();iiii++){
				outStr += std::to_string(v[iii].endNodes[iiii]);
				if (iiii<v[iii].endNodes.size()-1){
					outStr += ",";
				}
				else {
					outStr += "\",";
				}
			}
			if (v[iii].endNodes.size()==0){
				outStr += "\",";
			}
		}
		myfile << outStr +"\n";
		
		
		outStr = iter->first+",";
		if (answerListMapF.find(iter->first)== answerListMapF.end()){
			std::cout << "missing??????222222\n";
			myfile << outStr +"\n";
			continue;
		}
		for (iii=0;iii<answerListMapF[iter->first].size();iii++){
			outStr += std::to_string(answerListMapF[iter->first][iii])+",";
		}
		myfile << outStr +"\n";
	}
	myfile.close();
	//for (flat_hash_map<std::string,Answer>::iterator iter = answerMap.begin(); iter != answerMap.end(); ++iter){
	//	inputArray.push_back(inputify(iter->first));
	//}
	auto a3 = std::chrono::high_resolution_clock::now();
	std::cout << "time to inputify answers: " << " and " << std::chrono::duration_cast<std::chrono::microseconds>( a3 - a2 ).count() << "\n\n\n";
	
	
	
	

	return error;
}

bool getOneAnswer(std::string s, int nSteps, std::string oquestion) {
	//TODO: make this up-to-date with fullanswer
	if (nSteps > maxFound){
		maxFound = nSteps;
	}
	if (nSteps >= maxSteps){
		return true;
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
		if (doubleCheckAnswer(newPostfix)){
			Answer answer;
			answer.correct = true;
			answer.finished = true;
			//answer.solution = ;
			//answer.input = ;
			answerMap[newPostfix]=answer;
			std::cout << "One answer: " << newPostfix << "\n";
			return false;
		}
		
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
			if (!getOneAnswer(allStrings[ii].next,nSteps+1,oquestion)){
				return false;
			}
			Step step;
			step.next = newPostfix;
			step.rule = allStrings[ii].rule;
			reverseMapCorrect[allStrings[ii].next]={step};

		}

	}
	
	
	
	return true;
		
	
}

std::string oneAnswer(std::string s){
	std::string newPostfix = removeBracketsOne(s);
	std::cout << "\n\nStarting the Loop @$*&^@$*&^@*$&^@*$&^\n\n";
	reverseMap.clear();
	reverseMapCorrect.clear();
	finishedAnswers.resize(0);
	answerListMap.clear();
	answerListMapF.clear();
	correctSolutionList.clear();
	incorrectSolutionList.clear();
	answerMap.clear();
	auto a1 = std::chrono::high_resolution_clock::now();

	getOneAnswer(newPostfix,0,newPostfix);
	auto a2 = std::chrono::high_resolution_clock::now();
	std::cout << "\n\n\n\nCompleted the One Loop @$*&^@$*&^@*$&^@*$&^\n\n\n\n" << " and " << std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count() << "\n\n\n";
	std::cout << "total answers: "<< totalAnswers << "\n";
	//duration2 += std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count();
	std::cout << "\n\nCompleted the Loop @$*&^@$*&^@*$&^@*$&^\n\n";

	


	return "blank";
}


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



void GetQuestion(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	Dewey dewey;
	std::string q = "";
	if (info.Length()>0){
		v8::String::Utf8Value s(isolate, info[0]);
		std::string a(*s);
		q = a;
	}
	if (info.Length()>1){
		v8::String::Utf8Value s(isolate, info[1]);
		std::string a(*s);
		if (a.length()>0){
			dewey.subject = a;
		}
	}
	if (info.Length()>2){
		v8::String::Utf8Value s(isolate, info[2]);
		std::string a(*s);
		if (a.length()>0){
			dewey.topic = a;
		}
		
		
	}
	if (info.Length()>3){
		v8::String::Utf8Value s(isolate, info[3]);
		std::string a(*s);
		if (a.length()>0){
			dewey.lesson = a;
		}
		
	}
	
	answerConstraints.clear();
	constraintMap.clear();
	//std::vector<RawQuestion> qs = makeQuestions(dewey, "answerconstraints.csv");
	std::cout << "starting" << q << "\n";
	std::vector<RawQuestion> qs = makeQuestionsNew(dewey, q);
	std::cout << "done\n";
	currentQuestion = chooseQuestion(qs);
	
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(currentQuestion.text);

	
	info.GetReturnValue().Set(h.ToLocalChecked());
}
void PreviewQuestion(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string q(*s);
	Question rq = previewQuestion(q);

	std::string outstr = rq.text;
	maxSteps = 5;
	oneAnswer(rq.comp);
	//TODO: GET ANSWER FROM ANSWERMAP
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(outstr);
	
	
	info.GetReturnValue().Set(h.ToLocalChecked());
}
void GetAnswers(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string filen(*s);
	
	finishedAnswers.resize(0);
	answerListMap.clear();
	answerListMapF.clear();
	correctSolutionList.clear();
	incorrectSolutionList.clear();
	answerMap.clear();
	reverseMap.clear();
	reverseMapCorrect.clear();
	unfinishedOptions.clear();
	foundOneAnswer = false;
	startedWrong = false;
	maxSteps = 25;
	
	auto a1 = std::chrono::high_resolution_clock::now();
	maxFound = 0;
	
	std::cout << "mf:" << maxFound << " times: " << duration1 << " and " << duration2 << " and " << duration3 << "\n";
	
	std::string error = fullAnswer(currentQuestion.comp,filen);
	
	
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
               Nan::New("previewQuestion").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(PreviewQuestion)
                   ->GetFunction(context)
                   .ToLocalChecked());

}

NODE_MODULE(helloarray, Init)