#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <chrono>

#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <math.h>
#include <limits.h>
#include <time.h>
#include <string.h> 
#include <ctype.h>
#include <iostream>
#include <variant>
#include <map>
#include <numeric>
#include <chrono>
#include <thread>
#include <sstream>
#include <iostream>
#include <dlfcn.h>
#include <math.h>
#include <vector>
#include <array>


inline std::string digitsToString(std::vector<short> digits, bool order){
	int sz = digits.size();
	int i;
	std::string out = "";
	if (order){
		for (i=0;i<sz;i++){
			out += std::string(1,digits[i]+'0');
		}
	}
	else {
		for (i=sz-1;i>=0;i--){
			out += std::string(1,digits[i]+'0');
		}
	}
	return out;
}
inline std::string addTwoInts(std::string str1, std::string str2){
	std::vector<short> digits1;
	std::vector<short> digits2;
	std::vector<short> digits0;
	auto it = str1.cend();
	for (it = str1.cend()-1;it>= str1.cbegin();it--){
		digits1.push_back(*it- '0');
	}
	for (it = str2.cend()-1;it>= str2.cbegin();it--){
		digits2.push_back(*it- '0');
	}
	int i;
	int sz1 = digits1.size();
	int sz2 = digits2.size();
	int carry = 0;
	int digit = 0;
	for (i=0;i<sz1 || i<sz2;i++){
		if (i< sz1 && i<sz2){
			digit = digits1[i]+digits2[i]+carry;
		}
		else if (i< sz1){
			digit = digits1[i]+carry;
		}
		else{
			digit = digits2[i]+carry;
		}
			
		if (digit>9){
			digits0.push_back(digit%10);
			carry = digit/10;
		}
		else {
			digits0.push_back(digit);
			carry = 0;
		}
	}
	while (carry > 0){
		if (carry>9){
			digits0.push_back(carry%10);
			carry = carry/10;
		}
		else {
			digits0.push_back(carry);
			carry = 0;
		}
	}
	return digitsToString(digits0,false);
}
inline std::string addInts(std::vector<std::string> strs){
	if (strs.size() == 1){
		return strs[0];
	}
	else if (strs.size() == 0){
		return "";
	}
	
	
    
	std::vector<std::vector<short>> digits;
	std::vector<short> digits0;
	auto it = strs[0].cend();
	unsigned int ii;
	unsigned int sz = 0;
	for (ii=0;ii<strs.size();ii++){
		std::vector<short> onestr;
		for (it = strs[ii].cend()-1;it>= strs[ii].cbegin();it--){
			onestr.push_back(*it- '0');
		}
		if (onestr.size()>sz){
			sz = onestr.size();
		}
		digits.push_back(onestr);
	}
	
	unsigned int i;
	unsigned int carry = 0;
	unsigned int digit = 0;
	for (i=0;i<sz;i++){
		digit = carry;
		for (ii=0;ii<digits.size();ii++){
			if (i < digits[ii].size()){
				digit += digits[ii][i];
			}
		}
			
		if (digit>9){
			digits0.push_back(digit%10);
			carry = digit/10;
		}
		else {
			digits0.push_back(digit);
			carry = 0;
		}
	}
	while (carry > 0){
		if (carry>9){
			digits0.push_back(carry%10);
			carry = carry/10;
		}
		else {
			digits0.push_back(carry);
			carry = 0;
		}
	}
	return digitsToString(digits0,false);
}

extern "C" std::string addIntsWrong(std::vector<std::string> strs, std::string answer){
	if (strs.size() == 1){
		return "size is 1";
	}
	else if (strs.size() == 0){
		return "size is 0";
	}

    
    
    
	std::vector<short> answerDigits;
	auto it = answer.cend();
	for (it = answer.cend()-1;it>= answer.cbegin();it--){
		answerDigits.push_back(*it- '0');
	}
	unsigned int ii;
	unsigned int sz = 0;
	
	std::vector<std::vector<short>> digits;
	for (ii=0;ii<strs.size();ii++){
		std::vector<short> onestr;
		for (it = strs[ii].cend()-1;it>= strs[ii].cbegin();it--){
			onestr.push_back(*it- '0');
		}
		if (onestr.size()>sz){
			sz = onestr.size();
		}
		digits.push_back(onestr);
	}
	unsigned int dsz = digits.size();
	unsigned int adsz = answerDigits.size();
	for (ii=0;ii<dsz;ii++){
		int i;
		for (i = digits[ii].size();i<sz;i++){
			digits[ii].push_back(0);
		}
	}
	
	
	std::vector<short> digits0 = {0,0,0,0,0};
	std::string errors;
	std::string returnString;
	int iii;
	bool isPossible = true;
		
	unsigned int i; unsigned int di;
	unsigned int carry = 0;
	unsigned int digit = 0;
	unsigned int newdigit = 0;
	unsigned int r = rand() % 100000;
	for (iii=0;iii<100000;iii++){
		errors = "";
		di = 0;
		isPossible = true;
		carry = 0;
		digit = 0;
		newdigit = 0;
		
		for (i=0;i<sz;i++){
			digit = carry;
			for (ii=0;ii<dsz;ii++){
				newdigit = digit + digits[ii][i];
				if (newdigit/10 > digit/10 && (r*iii) % 1000 > 970){
					digit = newdigit - 10;
					//std::string d(1,i+'2'); //next digit will be wrong, and start at 1 not 0 -- only up to 9th digit
					//errors += "You missed a carry on "+d+"rd digit from right.\n";
					errors += "You missed a carry.\n";
				}
				else {
					digit = newdigit;
				}
			}
			if (digit>9){
				digits0[di] = digit%10;
				di++;
				carry = digit/10;
			}
			else {
				digits0[di] = digit;
				di++;
				carry = 0;
			}
			
			if (adsz <= i || digits0[i] !=answerDigits[i]){
				isPossible = false;
				break;
			}
		}
		if (!isPossible){continue;}
		while (carry > 0){
			if (carry>9){
				digits0[di] = carry%10;
				di++;
				carry = carry/10;
			}
			else {
				digits0[di] = carry;
				di++;
				carry = 0;
			}
			if (adsz <= i || digits0[i] !=answerDigits[i]){
				isPossible = false;
				break;
			}
			i++;
		}
		if (isPossible && adsz == di){
			returnString = errors;
			//returnString += "The correct answer is " + addInts(strs);
		}
		
	}
	return returnString;
	//return "done";
}
