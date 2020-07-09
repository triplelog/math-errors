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
flat_hash_map<std::string,std::vector<std::string>> rules;

std::string arrayToString(int n, char input[]) { 
    int i; 
    std::string s = ""; 
    for (i = 0; i < n; i++) { 
        s = s + input[i]; 
    } 
    return s; 
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
	
	char ddx{-69};
	
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
		else if (firstChar == ddx || firstChar == '^' || firstChar == '*' || firstChar == '+' || firstChar == '/' || firstChar == '~' || firstChar == '>' || firstChar == '<' || firstChar == '=' || firstChar == '!' || firstChar == '[' || firstChar == ']' || firstChar == '&' || firstChar == '|') {
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
		else if (firstChar == ddx || firstChar == '^' || firstChar == '*' || firstChar == '+' || firstChar == '>' || firstChar == '<' || firstChar == '=' || firstChar == '!' || firstChar == '[' || firstChar == ']' || firstChar == '&' || firstChar == '|') {
			expstr += ci;
		}
		else {
			intstr += ci;
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

std::vector<std::string> makeTree(std::string pfstr){
	std::vector<std::string> treeOptions;
	flat_hash_map<std::string,std::vector<std::string>> listMap;
	flat_hash_map<int,std::string> operandMap;
	flat_hash_map<int,std::string> originalMap;
	std::vector<std::string> finalList;
	
	int i; int ii; int iii;
	int idx =0;
	char ddx{-69};
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
			
			if (pfstr.at(i) != '-' && pfstr.at(i) != '/' && pfstr.at(i) != ddx){
				
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
	
	std::cout << "\n\n--------\n";
	int iiii;
	for (ii=0;ii<finalList.size()/2;ii++){
		std::vector<int> indexes; //start,length,iidx
		std::string currentOperand = "";
		int startIndex = 0;
		for (iii=0;iii<finalList[ii*2+1].length();iii++){
			if (finalList[ii*2+1].at(iii) == '{'){
				startIndex = iii;
				currentOperand = "";
			}
			else if (finalList[ii*2+1].at(iii) == '}'){
				indexes.push_back(startIndex+1);
				indexes.push_back(iii-(startIndex+1));
				indexes.push_back(std::stoi(currentOperand));
				currentOperand = "";
			}
			else {
				currentOperand += finalList[ii*2+1].at(iii);
			}
		}
		
		for (iii=indexes.size()/3-1;iii>=0;iii--){
			std::string repText = originalMap[iii*3+2];
			bool foundBracket = false;
			for (iiii=0;iiii<repText.length();iiii++){
				if (repText.at(iiii) == '{'){
					foundBracket = true;
					break;
				}
			}
			if (!foundBracket){
				finalList[ii*2+1].replace(indexes[iii*3],indexes[iii*3+1],repText);
			}
		}
		
		treeOptions.push_back(finalList[ii*2]+'@'+finalList[ii*2+1]);
		
		std::cout << ii << "-:==:- " << treeOptions[ii] << '\n';
	}
	for (flat_hash_map<int,std::string>::iterator iter = originalMap.begin(); iter != originalMap.end(); ++iter){
		std::cout << iter->first << " and " << iter->second << '\n';
	}
	std::cout << "\n\n________\n";
	//std::cout << '\n';
	return treeOptions;
}

flat_hash_map<std::string,std::vector<std::string>> makeList(std::string pfstr){
	std::vector<std::string> treeOptions;
	flat_hash_map<std::string,std::vector<std::string>> listMap;
	flat_hash_map<int,std::string> operandMap;
	flat_hash_map<int,std::string> originalMap;
	std::vector<std::string> finalList;
	
	int i; int ii; int iii;
	int idx =0;
	char ddx{-69};
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
			
			if (pfstr.at(i) != '-' && pfstr.at(i) != '/' && pfstr.at(i) != ddx){
				
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
						//as-is
						fullTrees.push_back(firstS[ii] + secondS[iii]  + pfstr.at(i));
						fullTrees.push_back(firstT[ii] + secondT[iii]);
						
						//condensed
						fullTrees.push_back(""+'#');
						fullTrees.push_back(std::to_string(iidx)+'_');
						originalMap[iidx]= firstS[ii] + secondS[iii] + pfstr.at(i) + '@' + firstT[ii] + secondT[iii];
						iidx++;
						
						//reversed
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
					fullTrees.push_back(""+'#');
					fullTrees.push_back(std::to_string(iidx)+'_');
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
	
	//std::cout << '\n';
	return listMap;
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


std::vector<std::string> postfixifyVector(std::string input_str){
	flat_hash_map<std::string,std::string> replacements;
	char ddx{-69};
	replacements["ddx"]="";
	replacements["ddx"]+=ddx;
	int i;
	std::string threeChars = "...";
	for (i=0;i<input_str.length();i++){
		threeChars.replace(0,1,"");
		threeChars += input_str.at(i);
		if (replacements.find(threeChars) != replacements.end()){
			input_str.replace(i-2,3,replacements[threeChars]);
			threeChars = "...";
			i--;
		}
		//std::cout << i << " : " << input_str << " 3chars: " << threeChars << '\n';
	}
	
	char infixexpr[input_str.length() + 1]; 
    strcpy(infixexpr, input_str.c_str()); 

	infixexpr[input_str.length()] = '\0';
	std::cout << makePost(infixexpr) << '\n';
	

	return makePostVector(infixexpr);
}
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
	
	flat_hash_map<std::string,std::string> replacements;
	char ddx{-69};
	replacements["ddx"]="";
	replacements["ddx"]+=ddx;
	int i;
	std::string threeChars = "...";
	for (i=0;i<input_str.length();i++){
		threeChars.replace(0,1,"");
		threeChars += input_str.at(i);
		if (replacements.find(threeChars) != replacements.end()){
			input_str.replace(i-2,3,replacements[threeChars]);
			threeChars = "...";
			i--;
		}
		//std::cout << i << " : " << input_str << " 3chars: " << threeChars << '\n';
	}
	
	char infixexpr[input_str.length() + 1]; 
    strcpy(infixexpr, input_str.c_str()); 

	infixexpr[input_str.length()] = '\0';
	std::cout << makePost(infixexpr) << '\n';
	

	return makePost(infixexpr);
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

std::vector<std::string> makeRule(std::string input){
	char infixexpr[input.length() + 1]; 
    strcpy(infixexpr, input.c_str()); 

	infixexpr[input.length()] = '\0';
	std::vector<std::string> postfixed = postfixifyVector(infixexpr);
	//std::cout << postfixed;
	return postfixed;
	//return makeTree(postfixed)[0];
}

flat_hash_map<std::string,std::vector<std::string>> makeRules(){
	flat_hash_map<std::string,std::vector<std::string>> finalRules;
	std::vector<std::vector<std::string>> rawRules;
	rawRules.push_back({"ddx(A+B)","ddx(A)+ddx(B)","Sum Rule."});
	rawRules.push_back({"ddx(x^3)","3*x^2","Turn exponent into multiplication."});
	rawRules.push_back({"ddx(5)","0","Turn exponent into multiplication."});
	int i; int ii;
	std::vector<std::string> fullPost;
	std::string key;
	std::string val1;
	std::string out;
	for (i=0;i<rawRules.size();i++){
		fullPost = makeRule(rawRules[i][0]);
		key = fullPost[0];
		val1 = fullPost[1];
		fullPost = makeRule(rawRules[i][1]);
		out = fullPost[0] + '@' + fullPost[1];
		
		finalRules[key] = {val1,out,rawRules[i][2]};
		// TODO: add possibility of appending to existing key, and adding all constraints
	}
	return finalRules;
}

std::string applyRules(std::string userFullString) {
	int iii; int iiii;
	flat_hash_map<std::string,std::vector<std::string>> allParts = makeList(userFullString);
	flat_hash_map<std::string,int> operandToIndex;
	flat_hash_map<std::string,int> operandToIndexSecond;
	flat_hash_map<std::string,std::string> operandList;
	std::string newPostfix = "";
	int idx = 0;
	std::cout << "\n\n" << userFullString << '\n';
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
	for (iii=0;iii<userFullString.length();iii++){
		if (userFullString.at(iii) == '_'){
			operandToIndexSecond[std::to_string(idx)] = iii+1;
			idx++;
		}
		if (userFullString.at(iii) == '@'){
			operandToIndexSecond[std::to_string(idx)] = iii+1;
			idx++;
		}
	}
	bool foundAt = false;
	std::string currentOperand = "";
	idx = 0;
	for (iii=0;iii<userFullString.length();iii++){
		if (userFullString.at(iii) == '@'){
			foundAt = true;
			currentOperand = "";
		}
		else if (foundAt && userFullString.at(iii) == '_'){
			operandList[std::to_string(idx)] = currentOperand;
			idx++;
			currentOperand = "";
		}
		else {
			currentOperand += userFullString.at(iii);
		}
	}
	for (flat_hash_map<std::string,std::vector<std::string>>::iterator iter = allParts.begin(); iter != allParts.end(); ++iter){
		std::string onePart = iter->first;
		foundAt = false;
		bool foundFirst = false;
		int firstOperandIndex = 0;
		int firstOperandIndexSecond = 0;
		currentOperand = "";
		std::string fullStr = "";
		int replaceLength = 0;
		int replaceLengthSecond = 0;
		for (iii=0;iii<onePart.length();iii++){
			if (onePart.at(iii) == '@'){
				foundAt = true;
				currentOperand = "";
				fullStr += onePart.at(iii);
			}
			else if (foundAt && onePart.at(iii) == '_'){
				if (!foundFirst){
					firstOperandIndex = operandToIndex[currentOperand];
					firstOperandIndexSecond = operandToIndexSecond[currentOperand];
				}
				foundFirst = true;
				fullStr += operandList[currentOperand]+'_';
				currentOperand = "";
				replaceLengthSecond++;
			}
			else if (foundAt){
				currentOperand += onePart.at(iii);
				replaceLengthSecond++;
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
		flat_hash_map<char,std::string> partMap;
		std::vector<std::string> userOperands;
		std::vector<std::string> ruleOperands;
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
			std::string currentOperand = "";
			for (iii=0;iii<rules[key][0].length();iii++){
				if (rules[key][0].at(iii) == '_'){
					ruleOperands.push_back(currentOperand);
					currentOperand = "";
				}
				else {
					currentOperand += rules[key][0].at(iii);
				}
			}
			currentOperand = "";
			for (iii=startAt;iii<userString.length();iii++){
				if (userString.at(iii) == '_'){
					userOperands.push_back(currentOperand);
					currentOperand = "";
				}
				else {
					currentOperand += userString.at(iii);
				}
			}
			if (ruleOperands.size() != userOperands.size()){
				//TODO: move to next rule
				return userString;
			}
			for (iii=0;iii<ruleOperands.size();iii++){
				if (ruleOperands[iii].length()==1){
					if (ruleOperands[iii].at(0) <= 'Z' && ruleOperands[iii].at(0) >= 'A'){
						partMap[ruleOperands[iii].at(0)] = userOperands[iii];
					}
					else if (ruleOperands[iii] != userOperands[iii]){
						//TODO: skip this rule
						return userString;
					}
				}
				else if (ruleOperands[iii] != userOperands[iii]){
					//TODO: skip this rule
					return userString;
				}
			}
			//TODO: add check that operand arrays are same size--check before inserting into partMap as well;
			newPostfix = "";
			bool pastKey = false;
			for (iii=0;iii<rules[key][1].length();iii++){
				if (pastKey){
					if (rules[key][1].at(iii) == '_'){
						if (currentOperand.length()==1 && currentOperand.at(0) <='Z' && currentOperand.at(0) >= 'A'){
							newPostfix += partMap[currentOperand.at(0)] + '_';
						}
						else {
							newPostfix += currentOperand + '_';
						}
						currentOperand = "";
					}
					else {
						currentOperand += rules[key][1].at(iii);
					}
				}
				else {
					if (rules[key][1].at(iii) == '@'){
						pastKey = true;
					}
					newPostfix += rules[key][1].at(iii);
				}
			}
		}
		
		if (newPostfix.length()>0){
			//std::cout << userFullString << " anand " << fullStr << " anand " << newPostfix << "\n\n";
			std::string newPostfixFirst = "";
			std::string newPostfixSecond = "";
			foundAt = false;
			for (iiii=0;iiii<newPostfix.length();iiii++){
				if (newPostfix.at(iiii) == '@'){
					foundAt = true;
				}
				else if (foundAt){
					newPostfixSecond += newPostfix.at(iiii);
				}
				else {
					newPostfixFirst += newPostfix.at(iiii);
				}
			}
			userFullString.replace(firstOperandIndexSecond,replaceLengthSecond,newPostfixSecond).replace(firstOperandIndex,replaceLength,newPostfixFirst);
			//std::cout << userFullString << " anand " << fullStr << " anand " << newPostfix << "\n\n";
			return userFullString;
		}
	}
	
	if (newPostfix.length()==0){
		return userFullString;
	}
	return newPostfix;
	
}
int main () {

	
	char ddx{-69};
	prec[ddx]=6;
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
	

	
	rules = makeRules();
	int ii;
	//for (ii=0;ii<rules.size();ii++){
	//	std::cout << ii << "-=-" << rules[ii] << '\n';
	//}
	
	auto t1 = std::chrono::high_resolution_clock::now();
	
	
	
	std::string s = "ddx(x^3+5)"; 
  
	std::string pfstr = postfixify(s);
	std::cout << pfstr << '\n';
	std::vector<std::string> postList = makeTree(pfstr);
	
	for (ii=0;ii<postList.size();ii++){
		std::string newPostfix = postList[ii];
		std::string oldPostfix = "";
		int maxSteps = 5;
		while (newPostfix != oldPostfix && maxSteps >=0){
			oldPostfix = newPostfix;
			newPostfix = applyRules(oldPostfix);
			maxSteps--;
			std::cout << "MatchT: " << postList[ii] << " into "<< newPostfix << " from " << oldPostfix << '\n';
		}
		std::cout << ii << "-:-" << postList[ii] << '\n';
		std::cout << "Match: " << postList[ii] << " into "<< newPostfix << '\n';
		
		

	}
	auto t2 = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>( t2 - t1 ).count();

    std::cout << duration;
}