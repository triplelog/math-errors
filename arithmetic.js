function addIntsWrong(strs, answer){
	if (strs.length == 1){
		return "size is 1";
	}
	else if (strs.length == 0){
		return "size is 0";
	}

    
    
    
	var answerDigits = [];
	for (var it = answer.length-1;it>= 0;it--){
		answerDigits.push(parseInt(answer[it]));
	}
	var ii;
	var sz = 0;
	
	var digits = [];
	for (ii=0;ii<strs.length;ii++){
		onestr = [];
		for (var it = strs[ii].length-1;it>= 0;it--){
			onestr.push(parseInt(strs[ii][it]));
		}
		if (onestr.length>sz){
			sz = onestr.length;
		}
		digits.push(onestr);
	}
	var dsz = digits.length;
	var adsz = answerDigits.length;
	for (ii=0;ii<dsz;ii++){
		int i;
		for (i = digits[ii].length;i<sz;i++){
			digits[ii].push(0);
		}
	}
	
	
	var digits0 = [0,0,0,0,0];
	var errors = "";
	var returnString = "";
	var iii;
	var isPossible = true;
		
	var i; var di;
	var carry = 0;
	var digit = 0;
	var newdigit = 0;
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
				if (newdigit/10 > digit/10 && iii % 1000 > 970){
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