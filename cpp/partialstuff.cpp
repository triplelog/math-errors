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

std::vector<std::vector<Step>> partialTree(std::string pfstr){
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

void OneRule(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string a(*s);
	
	//Dewey dewey;
	//TODO: check all rules of this dewey
	//make tree
	std::string postfixed = postfixify(a);
	std::vector<std::vector<Step>> steps = partialTree(postfixed);
	int i;
	for (i=0;i<steps[0].size();i++){
		flat_hash_map<char,std::string> partMap = steps[0][i].partMap;
		for (flat_hash_map<char,std::string>::iterator iter = partMap.begin(); iter != partMap.end(); ++iter){
					
			std::cout << "first: " << iter->first << " and " << iter->second << "\n";
		}
	}
	//if applies, grab initial form (i.e. A=...,B=...)
	//solve and grab new form
	//get final form
	//return all 4
	//if multiple rules or multiple branches return all possibles
	
	
	
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(a);

	
	info.GetReturnValue().Set(h.ToLocalChecked());
}

void LatexIt(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string a(*s);
	
	std::cout << "input: " << a <<"\n";
	std::string postfixed = postfixify(a);
	std::cout << "postfixed: " << postfixed <<"\n";
	std::string latexed = latexOne(postfixed);
	std::cout << "latexed: " << latexed <<"\n";
	
	
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(latexed);

	
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
               Nan::New("onerule").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(OneRule)
                   ->GetFunction(context)
                   .ToLocalChecked());
  exports->Set(context,
               Nan::New("latexify").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(LatexIt)
                   ->GetFunction(context)
                   .ToLocalChecked());

}

NODE_MODULE(helloarray, Init)