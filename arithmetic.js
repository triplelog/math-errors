function addIntsWrong(std::vector<std::string> strs, std::string answer){
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
				if (newdigit/10 > digit/10 && rand() % 1000 > 970){
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
			returnString += "The correct answer is " + addInts(strs);
		}
		
	}
	return returnString;
	//return "done";
}