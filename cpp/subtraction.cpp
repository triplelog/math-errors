#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <math.h>
#include <array>

inline std::string subtractTwoInts(std::string str1, std::string str2){
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
	int borrow = 0;
	int digit = 0;
	for (i=0;i<sz1 || i<sz2;i++){
		digit = borrow;
		if (i< sz1 && i<sz2){
			digit += digits1[i]-digits2[i];
		}
		else if (i< sz1){
			digit += digits1[i];
		}
		else{
			digit -= digits2[i];
		}
			
		if (digit<0){
			digits0.push_back(((digit%10) + 10)%10);
			borrow = -1 + (digit/10);
			
		}
		else {
			digits0.push_back(digit);
			borrow = 0;
		}
	}
	if (borrow < 0){
		//should have subtracted small from big
		return "-"+subtractTwoInts(str2,str1);
	}
	return digitsToString(digits0,false);
}

inline std::string subtractIntsWrong(std::vector<std::string> strs, std::string answer){
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
		
	
	std::vector<short> digits0;
	std::string errors;
	std::string returnString;
	int iii;
	for (iii=0;iii<10000;iii++){
		errors = "";
		digits0.clear();
		bool isPossible = true;
		
		unsigned int i;
		int borrow = 0;
		int digit = 0;
		for (i=0;i<sz;i++){
			digit = borrow;
			if (i< digits[0].size()){
				digit += digits[0][i];
			}
			if (i< digits[1].size()){
				digit -= digits[1][i];
			}
			
					
			if (digit<0){
				digits0.push_back(((digit%10) + 10)%10);
				if (rand() % 1000 > 900){
					borrow = digit/10;
					std::string d(1,i+'2'); //next digit will be wrong, and start at 1 not 0
					errors += "You forgot to borrow on "+d+"rd digit from right.\n";
				}
				else {
					borrow = -1 + (digit/10);
				}
				
			
			}
			else {
				digits0.push_back(digit);
				borrow = 0;
			}
			
			if (answerDigits.size() <= i || digits0[i] !=answerDigits[i]){
				isPossible = false;
				break;
			}
		}
		if (!isPossible){continue;}
		if (borrow < 0){
			//should have subtracted small from big
		}
		if (isPossible && answerDigits.size() == digits0.size()){
			returnString = errors;
			returnString += "The correct answer is " + subtractTwoInts(strs[0],strs[1]);
		}
		
		
	}
	return returnString;
}
