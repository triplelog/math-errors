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
#include "parallel_hashmap/phmap.h"


using namespace std::chrono;
using phmap::flat_hash_map;
flat_hash_map<std::string,std::string> treeMap;
flat_hash_map<char,int> prec;

std::string arrayToString(int n, char input[]) { 
    int i; 
    std::string s = ""; 
    for (i = 0; i < n; i++) { 
        s = s + input[i]; 
    } 
    return s; 
}


std::string makePost(char infixexpr[]) {
	
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
		else if (firstChar == '^' || firstChar == '*' || firstChar == '+' || firstChar == '/' || firstChar == '~' || firstChar == '>' || firstChar == '<' || firstChar == '=' || firstChar == '!' || firstChar == '[' || firstChar == ']' || firstChar == '&' || firstChar == '|') {
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
		if (firstChar == '~'){
			//expstr += "-";
			expstr += "-+";
		}
		else if (firstChar == '/'){
			//expstr += "-";
			expstr += "/*";
		}
		else if (firstChar == '^' || firstChar == '*' || firstChar == '+' || firstChar == '>' || firstChar == '<' || firstChar == '=' || firstChar == '!' || firstChar == '[' || firstChar == ']' || firstChar == '&' || firstChar == '|') {
			expstr += ci;
		}
		else {
			intstr += ci;
			intstr += "_";
			expstr += "#";
		}

	}
	std::string retstr = expstr + "@" + intstr;
	return retstr;


}

std::vector<std::string> makeTree(std::string pfstr){
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
			
			if (pfstr.at(i) != '-' && pfstr.at(i) != '/'){
				
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
				}
			}
			
			
			
			std::string fullStr = firstStr + secondStr + pfstr.at(i) + '@' + firstTtr + secondTtr;
			/*
			std::cout << i << "---" << fullStr << '\n';
			
			for (ii=0;ii<fullTrees.size();ii++){
				std::cout << i << "-:-" << fullTrees[ii] << '\n';
			}
			*/
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
	
	for (ii=0;ii<finalList.size()/2;ii++){
		treeOptions.push_back(finalList[ii*2]+'@'+finalList[ii*2+1]);
		//std::cout << ii << "-:-" << treeOptions[ii] << '\n';
	}
	//std::cout << '\n';
	return treeOptions;
}
/*
function replaceDecimals(istr){
	dindex = istr.indexOf('.');
	while (dindex >-1){
		intpart = 0;
		decpart = 0;
		denom = 1;
		strparts = [dindex,dindex+1];
		for (var i=1;i<dindex+1;i++){
			if ("0123456789".indexOf(istr[dindex-i]) > -1){
				intpart += parseInt(istr[dindex-i])*Math.pow(10,i-1);
				strparts[0] = dindex-i;
			}
			else{break;}
		}
		for (var i=dindex+1;i<istr.length;i++){
			if ("0123456789".indexOf(istr[i]) > -1){
				decpart *=10;
				denom *=10;
				decpart += parseInt(istr[i]);
				strparts[1] = i+1;
			}
			else{break;}
		}
		istr = istr.substring(0,strparts[0])+'('+ (intpart*denom+decpart) +'/'+ denom +')'+istr.substring(strparts[1],);
		dindex = istr.indexOf('.');
	}

	return istr
}

function replaceNegatives(istr){
	dindex = istr.indexOf('-')
	while (dindex >-1){
		if (dindex == 0){
			if ("0123456789".indexOf(istr[1]) == -1) {
				istr = '-1*'+istr.substring(1,);
			}
			dindex = istr.indexOf('-',1);
		}
		else{
			if ("><=![]&|(".indexOf(istr[dindex-1])> -1) {
				if ("0123456789".indexOf(istr[dindex-1])== -1){
					istr = istr.substring(0,dindex)+'-1*'+istr.substring(dindex+1,);
				}
				dindex = istr.indexOf('-',dindex+1);
			}
			else{
				istr = istr.substring(0,dindex)+'~'+istr.substring(dindex+1,);
				dindex = istr.indexOf('-',dindex+1);
			}
		}
	}
				
	return istr
}
*/

std::string postfixify(std::string input_str) {
	/*input_str = input_str.toUpperCase();
	input_str = input_str.replace(/AND/g,'&');
	input_str = input_str.replace(/OR/g,'|');
	input_str = input_str.replace(/\[/g,'(');
	input_str = input_str.replace(/]/g,')');
	input_str = input_str.replace(/{/g,'(');
	input_str = input_str.replace(/}/g,')');
	input_str = input_str.replace(/>=/g,']');
	input_str = input_str.replace(/<=/g,'[');
	input_str = input_str.replace(/==/g,'=');
	input_str = input_str.replace(/!=/g,'!');
	input_str = input_str.replace(/\+-/g,'-');
	input_str = input_str.replace(/--/g,'+');
	input_str = replaceDecimals(input_str);
	input_str = replaceNegatives(input_str);*/
	
	
	//var twoparts = makePost(input_str);
	
	
	/*
	//Convert column names
	console.log(twoparts[0]);
	console.log(twoparts[1]);
	var firstpart = twoparts[0].split("_");
	for (var i=0;i<firstpart.length;i++){
		if (parseInt(firstpart[i]).toString() != firstpart[i]){
			for (var ii in colInfo) {
				if (colInfo[ii].toUpperCase() == firstpart[i]) {
					firstpart[i] = 'c'+ii;
					break;
				}
			}
		}
		else {
			firstpart[i] = firstpart[i]+'.1.I';
		}
	}
	var fullstr = firstpart.join("_")+'@'+twoparts[1];
	*/
	return "fullstr";
}

/*
inline Cppdata solvePostfixVV(char expstr[], std::vector<Cppdata> const intArray, std::vector<Cppdata> stack)
{

	int i;
  	int currentIndex = 0;
  	int arrayIndex = 0;

    for (i = 0; expstr[i]; i++) 
    { 
        if (expstr[i] == '#') {
        	stack[currentIndex] = intArray[arrayIndex];
        	currentIndex++;
        	arrayIndex++;
  
        } else 
        { 
            switch (expstr[i]) 
            { 
	            case '>': stack[currentIndex - 2].w = (stack[currentIndex - 2] > stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break; 
	            case '<': stack[currentIndex - 2].w = (stack[currentIndex - 2] < stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break;
	            case ']': stack[currentIndex - 2].w = (stack[currentIndex - 2] >= stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break; 
	            case '[': stack[currentIndex - 2].w = (stack[currentIndex - 2] <= stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break;
	            case '+': stack[currentIndex - 2] = stack[currentIndex - 2] + stack[currentIndex - 1]; break; 
	            case '-': stack[currentIndex - 2] = stack[currentIndex - 2] - stack[currentIndex - 1]; break; 
	            case '*': stack[currentIndex - 2] = stack[currentIndex - 2] * stack[currentIndex - 1]; break; 
	            case '/': stack[currentIndex - 2] = stack[currentIndex - 2] / stack[currentIndex - 1]; break;
	            case '=': stack[currentIndex - 2] = stack[currentIndex - 2] == stack[currentIndex - 1]; break;
	            case '!': stack[currentIndex - 2] = stack[currentIndex - 2] != stack[currentIndex - 1]; break;
	            //case '%': stack[currentIndex - 2] = stack[currentIndex - 2] % stack[currentIndex - 1]; break; 
	            case '&': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w > 1) ? 1 : 0; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            case '|': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w == 0) ? 0 : 1; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            //multiandcase '&': if (stack[currentIndex - 5] > 0 && stack[currentIndex - 4] > 0 && stack[currentIndex - 3] > 0 && stack[currentIndex - 2] > 0 && stack[currentIndex - 1] > 0) {stack[currentIndex - 5] = 1;} else {stack[currentIndex - 5] = -1;}; currentIndex--; currentIndex--; currentIndex--; currentIndex--; break; 
            
            } 
            currentIndex--;
        } 
    } 



	return stack[0];

}
*/

std::string makeRule(std::string input){
	char infixexpr[input.length() + 1]; 
    strcpy(infixexpr, input.c_str()); 

	infixexpr[input.length()] = '\0';
	std::string postfixed = makePost(infixexpr);
	//std::cout << postfixed;
	return postfixed;
	//return makeTree(postfixed)[0];
}

std::vector<std::string> makeRules(){
	std::vector<std::string> finalRules;
	std::vector<std::string> rawRules;
	rawRules.push_back("A^2");
	rawRules.push_back("A+B");
	
	int i;
	for (i=0;i<rawRules.size();i++){
		finalRules.push_back(makeRule(rawRules[i]));
	}
	return finalRules;
}

int main () {

	
	
    prec['^'] = 5;
	prec['*'] = 4;
	prec['/'] = 4;
	prec['+'] = 3;
	prec['~'] = 3;
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
	
	std::vector<std::string> rules = makeRules();
	int ii;
	for (ii=0;ii<rules.size();ii++){
		std::cout << ii << "-=-" << rules[ii] << '\n';
	}
	
	auto t1 = std::chrono::high_resolution_clock::now();
	
	
	
	std::string s = "x^2"; 
  
    char infixexpr[s.length() + 1]; 
    strcpy(infixexpr, s.c_str()); 

	infixexpr[s.length()] = '\0';
	std::string pfstr = makePost(infixexpr);
	//std::cout << pfstr << '\n';
	std::vector<std::string> postList = makeTree(pfstr);
	for (ii=0;ii<postList.size()/2;ii++){
		std::cout << ii << "-:-" << postList[ii] << '\n';
		int iii; int iiii;
		for (iii=0;iii<rules.size();iii++){
			for (iiii=0;iiii<postList[ii].length();iiii++){
				if (postList[ii].at(iiii) == '@' || rules[iii].at(iiii) == '@'){
					if (postList[ii].at(iiii) == '@' && rules[iii].at(iiii) == '@') {
						std::cout << "Match: " << postList[ii] << " and " << rules[iii] << '\n';
					}
					break;
				}
				else if (postList[ii].at(iiii) != rules[iii].at(iiii)){
					break;
				}
			}
		}
	}
	auto t2 = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>( t2 - t1 ).count();

    std::cout << duration;
}