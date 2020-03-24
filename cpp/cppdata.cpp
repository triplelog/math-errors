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


using namespace std::chrono;

inline std::string addpar(std::string input_str, char exp){
	return input_str;
}
inline std::string addLatex(std::string str1, std::string str2, char exp){
	if (exp == '/'){
		return "\\frac{"+str1+"}{"+str2+"}";
	}
	else if (exp == '+'){
		return str1 + " + "+ str2;
	}
	else if (exp == '-'){
		return str1 + " - "+ str2;
	}
	else if (exp == '*'){
		return str1 + " * "+ str2;
	}
	return str1;
}

inline std::string solvePostfixString(char expstr[], std::vector<std::string> const stringArray, int stringArraySize)
{
	std::vector<std::string> stack;
	stack.resize(stringArraySize);
	int i;
  	int currentIndex = 0;
  	int arrayIndex = 0;

    for (i = 0; expstr[i]; i++) 
    { 
        if (expstr[i] == '#') {
        	stack[currentIndex] = stringArray[arrayIndex];
        	currentIndex++;
        	arrayIndex++;
  
        } else 
        { 
            switch (expstr[i]) 
            { 
	            //case '>': stack[currentIndex - 2].w = (stack[currentIndex - 2] > stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break; 
	            //case '<': stack[currentIndex - 2].w = (stack[currentIndex - 2] < stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break;
	            //case ']': stack[currentIndex - 2].w = (stack[currentIndex - 2] >= stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break; 
	            //case '[': stack[currentIndex - 2].w = (stack[currentIndex - 2] <= stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break;
	            case '+': stack[currentIndex - 2] = addpar(stack[currentIndex - 2],'+') + " + " + addpar(stack[currentIndex - 1],'+'); break; 
	            case '-': stack[currentIndex - 2] = addpar(stack[currentIndex - 2],'-') + " - " + addpar(stack[currentIndex - 1],'-'); break; 
	            case '*': stack[currentIndex - 2] = addpar(stack[currentIndex - 2],'*') + " * " + addpar(stack[currentIndex - 1],'*'); break; 
	            case '/': stack[currentIndex - 2] = addpar(stack[currentIndex - 2],'/') + " / " + addpar(stack[currentIndex - 1],'/'); break;
	            //case '=': stack[currentIndex - 2] = stack[currentIndex - 2] == stack[currentIndex - 1]; break;
	            //case '!': stack[currentIndex - 2] = stack[currentIndex - 2] != stack[currentIndex - 1]; break;
	            //case '%': stack[currentIndex - 2] = stack[currentIndex - 2] % stack[currentIndex - 1]; break; 
	            //case '&': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w > 1) ? 1 : 0; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            //case '|': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w == 0) ? 0 : 1; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            //multiandcase '&': if (stack[currentIndex - 5] > 0 && stack[currentIndex - 4] > 0 && stack[currentIndex - 3] > 0 && stack[currentIndex - 2] > 0 && stack[currentIndex - 1] > 0) {stack[currentIndex - 5] = 1;} else {stack[currentIndex - 5] = -1;}; currentIndex--; currentIndex--; currentIndex--; currentIndex--; break; 
            
            } 
            currentIndex--;
        } 
    } 



	return stack[0];

}

inline std::string latexifyString(char expstr[], std::vector<std::string> const stringArray, int stringArraySize)
{
	std::vector<std::string> stack;
	stack.resize(stringArraySize);
	int i;
  	int currentIndex = 0;
  	int arrayIndex = 0;

    for (i = 0; expstr[i]; i++) 
    { 
        if (expstr[i] == '#') {
        	stack[currentIndex] = stringArray[arrayIndex];
        	currentIndex++;
        	arrayIndex++;
  
        } else 
        { 
            switch (expstr[i]) 
            { 
	            //case '>': stack[currentIndex - 2].w = (stack[currentIndex - 2] > stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break; 
	            //case '<': stack[currentIndex - 2].w = (stack[currentIndex - 2] < stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break;
	            //case ']': stack[currentIndex - 2].w = (stack[currentIndex - 2] >= stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break; 
	            //case '[': stack[currentIndex - 2].w = (stack[currentIndex - 2] <= stack[currentIndex - 1]) ? 1 : 0; stack[currentIndex - 2].t = 'B'; break;
	            case '+': stack[currentIndex - 2] = addLatex(stack[currentIndex - 2],stack[currentIndex - 1],'+'); break; 
	            case '-': stack[currentIndex - 2] = addLatex(stack[currentIndex - 2],stack[currentIndex - 1],'-'); break; 
	            case '*': stack[currentIndex - 2] = addLatex(stack[currentIndex - 2],stack[currentIndex - 1],'*'); break; 
	            case '/': stack[currentIndex - 2] = addLatex(stack[currentIndex - 2],stack[currentIndex - 1],'/'); break;
	            //case '=': stack[currentIndex - 2] = stack[currentIndex - 2] == stack[currentIndex - 1]; break;
	            //case '!': stack[currentIndex - 2] = stack[currentIndex - 2] != stack[currentIndex - 1]; break;
	            //case '%': stack[currentIndex - 2] = stack[currentIndex - 2] % stack[currentIndex - 1]; break; 
	            //case '&': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w > 1) ? 1 : 0; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            //case '|': stack[currentIndex - 2].w = (stack[currentIndex - 2].w + stack[currentIndex - 1].w == 0) ? 0 : 1; stack[currentIndex - 2].t = (stack[currentIndex - 2].t == 'B' && stack[currentIndex - 1].t == 'B') ? 'B' : 'N'; break; 
	            //multiandcase '&': if (stack[currentIndex - 5] > 0 && stack[currentIndex - 4] > 0 && stack[currentIndex - 3] > 0 && stack[currentIndex - 2] > 0 && stack[currentIndex - 1] > 0) {stack[currentIndex - 5] = 1;} else {stack[currentIndex - 5] = -1;}; currentIndex--; currentIndex--; currentIndex--; currentIndex--; break; 
            
            } 
            currentIndex--;
        } 
    } 



	return stack[0];

}

