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


std::string outputTree(Step stepS,Step stepE){
	std::string pfstr = stepS.next;
	//std::cout << "pfstr: " << pfstr << " and ";
	int i; int ii; int iii;
	//for (i=0;i<stepS.startNodes.size();i++){
	//	std::cout << stepS.startNodes[i] << " ; ";
	//}
	//std::cout << "\n";
	std::vector<std::string> treeOptions;
	flat_hash_map<std::string,std::vector<std::string>> listMap;
	flat_hash_map<int,std::string> operandMap;
	flat_hash_map<int,std::string> originalMap;
	std::vector<std::string> finalList;
	std::vector<std::string> orderedKeyList;
	flat_hash_map<std::string,std::vector<std::string>> nodeList;
	std::string startNode = "";
	std::string endNode = "";
	flat_hash_map<std::string,bool> startNodes;
	flat_hash_map<std::string,bool> endNodes;
	
    
    
	
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
			if (i==stepS.startNode){startNode = name;}
			if (i==stepE.endNode){endNode = name;}
			for (ii=0;ii<stepS.startNodes.size();ii++){
				if (i==stepS.startNodes[ii]){
					startNodes[name]=true;
					break;
				}
			}
			for (ii=0;ii<stepE.endNodes.size();ii++){
				if (i==stepE.endNodes[ii]){
					endNodes[name]=true;
					break;
				}
			}
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
			if (i==stepS.startNode){startNode = name;}
			if (i==stepE.endNode){endNode = name;}
			for (ii=0;ii<stepS.startNodes.size();ii++){
				if (i==stepS.startNodes[ii]){
					startNodes[name]=true;
					break;
				}
			}
			for (ii=0;ii<stepE.endNodes.size();ii++){
				if (i==stepE.endNodes[ii]){
					endNodes[name]=true;
					break;
				}
			}
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
	std::string nodes = "{";
	std::string allNodes = "[";
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
			std::string outText = "\""+name + "\": {\"text\":";
			outText += "\"" + latexMap[name] + "\",";
			if (name == startNode){
				outText += "\"startNode\": true,";
			}
			else if (startNodes.find(name) != startNodes.end()){
				outText += "\"startNodes\": true,";
			}
			if (name == endNode){
				outText += "\"endNode\": true,";
			}
			else if (endNodes.find(name) != endNodes.end()){
				outText += "\"endNodes\": true,";
			}
			
			outText += "\"op\": \"" + nodeList[orderedKeyList[ii]][2] + "\",";
			outText += "\"parent\": \""+ parent + "\"}";
		

			if (nodes == "{"){
				nodes += outText;
			}
			else {
				nodes += ","+outText;
			}
			//std::cout << outText << "\n";
			if (allNodes == "["){
				allNodes += "\""+nodeList[orderedKeyList[ii]][0] + "\"";
			}
			else {
				allNodes += ",\""+nodeList[orderedKeyList[ii]][0] + "\"";
			}
		}
		
		
	}
	
	allNodes += "]";
	nodes += "}";
	
	std::string treeStr = "\"nodes\":"+nodes+",\"allNodes\":"+allNodes;
	//std::cout <<  treeStr << "\n";
	return treeStr;
}





flat_hash_map<std::string,Answer> answerMap;
flat_hash_map<std::string,std::vector<int>> answerListMapF;
int maxFound;
int maxSteps;



#include "autocomplete.cpp"


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






void MakeAnswers(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string a(*s);
	
	answerListMapF.clear();
	answerMap.clear();

	rapidcsv::Document doc("./cpp/questions/" + a, rapidcsv::LabelParams(-1, -1));
	
	int nRows = doc.GetRowCount();
	int i; int ii; int iii;
	
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
				if (ii%6 == 2){
					Step step;
					step.next = rawAnswer[ii-5];
					step.rule = std::stoi(rawAnswer[ii-4]);
					step.startNode = std::stoi(rawAnswer[ii-3]);
					step.endNode = std::stoi(rawAnswer[ii-2]);
					step.startNodes = {};
					std::string currentNode = "";
					for (iii=0;iii<rawAnswer[ii-1].length();iii++){
						if (rawAnswer[ii-1].at(iii) == ','){
							step.startNodes.push_back(std::stoi(currentNode));
							currentNode = "";
						}
						else {
							currentNode += rawAnswer[ii-1].at(iii);
						}
					}
					if (currentNode.length()>0){
						step.startNodes.push_back(std::stoi(currentNode));
					}
					
					currentNode = "";
					for (iii=0;iii<rawAnswer[ii].length();iii++){
						if (rawAnswer[ii].at(iii) == ','){
							step.endNodes.push_back(std::stoi(currentNode));
							currentNode = "";
						}
						else {
							currentNode += rawAnswer[ii].at(iii);
						}
					}
					if (currentNode.length()>0){
						step.endNodes.push_back(std::stoi(currentNode));
					}
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
	std::cout << "your answer: " << mpf << " postfixed from " << a << "\n";
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
			if (v[iii].rule >= 0){
				if (ruleIndex[v[iii].rule].type == "e"){
					std::cout << "error: " << ruleIndex[v[iii].rule].out << "\n";
				}
			}
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
	jsonmessage = "[";
	for (i=0;i<bestSolution.size();i++){
		std::cout << "bs: " << bestSolution[i].next << "\n";
		std::cout << "bsr: " << bestSolution[i].rule << "\n";
		std::string treeStr;
		if (i>0){
			treeStr = outputTree(bestSolution[i],bestSolution[i-1]);
		}
		else {
			treeStr = outputTree(bestSolution[i],bestSolution[i]);
		}
		
		if (i+1<bestSolution.size()){
			std::string oneStep = displayOne(bestSolution[i],bestSolution[i].next,bestSolution[i+1].next);
			treeStr += ",\"step\":" + oneStep; 
		}
		
		if (jsonmessage == "["){
			jsonmessage += "{" + treeStr + "}";
		}
		else {
			jsonmessage += ",{" + treeStr + "}";
		}
		
		
			
		
	}
	jsonmessage += "]";
	
	
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