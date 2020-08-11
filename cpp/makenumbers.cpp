

Range unionTwo(Range a, Range b) {
	int i; int ii;
	int bLast = b.left.size()-1;
	Number temp;
	for (ii=0;ii<a.left.size();ii++){
		if (b.left[bLast] < a.left[ii]){
			if (b.right[bLast] > a.left[ii]){
				temp = a.left[ii];
				a.left[ii] = b.left[bLast];
				if (b.incexc[bLast] >= 2 && a.incexc[ii] < 2){
					a.incexc[ii] += 2;
					b.incexc[ii] -= 2;
				}
				else if (b.incexc[bLast] < 2 && a.incexc[ii] >= 2) {
					a.incexc[ii] -= 2;
					b.incexc[ii] += 2;
				}
				b.left[bLast] = temp;
				return unionTwo(a,b);
			}
			else if ((b.right[bLast] == a.left[ii] && (b.incexc[bLast]%2==0) && (a.incexc[ii] <2)) || (b.right[bLast] < a.left[ii])){
				a.left.insert(a.left.begin()+ii,b.left[bLast]);
				a.right.insert(a.right.begin()+ii,b.right[bLast]);
				a.incexc.insert(a.incexc.begin()+ii,b.incexc[bLast]);
				
				if (bLast>0){
					b.left.pop_back();
					b.right.pop_back();
					b.incexc.pop_back();
					return unionTwo(a,b);
				}
				else {
					return a;
				}
			}
			else {
				a.left[ii] = b.left[bLast];
				if (b.incexc[bLast] >= 2 && a.incexc[ii] < 2){
					a.incexc[ii] += 2;
				}
				else if (b.incexc[bLast] < 2 && a.incexc[ii] >= 2) {
					a.incexc[ii] -= 2;
				}
				
				if (bLast>0){
					b.left.pop_back();
					b.right.pop_back();
					b.incexc.pop_back();
					return unionTwo(a,b);
				}
				else {
					return a;
				}
				
			}
		}
		else if (b.left[bLast] == a.left[ii]){
			if (b.incexc[bLast] >= 2 && a.incexc[ii] < 2){
				a.incexc[ii] += 2;
			}
			if (b.right[bLast] < a.right[ii]){
				if (bLast>0){
					b.left.pop_back();
					b.right.pop_back();
					b.incexc.pop_back();
					return unionTwo(a,b);
				}
				else {
					return a;
				}
			}
			else if (b.right[bLast] == a.right[ii]){
				if (b.incexc[bLast]%2 > a.incexc[ii]%2){
					a.incexc[ii] += 1;
				}
				if (bLast>0){
					b.left.pop_back();
					b.right.pop_back();
					b.incexc.pop_back();
					return unionTwo(a,b);
				}
				else {
					return a;
				}
			}
			else {
				b.left[bLast]=a.right[ii];
				if (b.incexc[bLast]%2 == 0){
					b.incexc[bLast]++;
				}
				return unionTwo(a,b);
			}
		}
		else if (b.left[bLast] < a.right[ii]){
			if (b.right[bLast] < a.right[ii]){
				if (bLast>0){
					b.left.pop_back();
					b.right.pop_back();
					b.incexc.pop_back();
					return unionTwo(a,b);
				}
				else {
					return a;
				}
			}
			else if (b.right[bLast] == a.right[ii]){
				if (b.incexc[bLast]%2 > a.incexc[ii]%2){
					a.incexc[ii] += 1;
				}
				if (bLast>0){
					b.left.pop_back();
					b.right.pop_back();
					b.incexc.pop_back();
					return unionTwo(a,b);
				}
				else {
					return a;
				}
			}
			else {
				b.left[bLast]=a.right[ii];
				if (b.incexc[bLast]%2 == 0){
					b.incexc[bLast]++;
				}
				return unionTwo(a,b);
			}
		}
		else if (b.left[bLast] == a.right[ii]){
			if (b.incexc[bLast]<2 && a.incexc[ii]%2 == 0){
				continue;
			}
			if (ii == a.left.size()-1){
				a.right[ii] = b.right[bLast];
				if (b.incexc[bLast]%2 ==1 && a.incexc[ii]%2 ==0){
					a.incexc[ii]++;
				}
				else if (b.incexc[bLast]%2 ==0 && a.incexc[ii]%2 ==1){
					a.incexc[ii]--;
				}
				if (bLast>0){
					b.left.pop_back();
					b.right.pop_back();
					b.incexc.pop_back();
					return unionTwo(a,b);
				}
				else {
					return a;
				}
			}
			
			if (b.right[bLast] > a.left[ii+1]){

				a.left[ii+1] = a.left[ii];
				if (a.incexc[ii+1]>= 2 && a.incexc[ii]<2){
					a.incexc[ii+1]-=2;
				}
				else if (a.incexc[ii+1]<2 && a.incexc[ii]>=2){
					a.incexc[ii+1]+=2;
				}
				a.left.erase(a.left.begin()+ii);
				a.right.erase(a.right.begin()+ii);
				a.incexc.erase(a.incexc.begin()+ii);
				return unionTwo(a,b);
			}
			else if (b.right[bLast] == a.left[ii+1] && !(b.incexc[bLast]%2 == 0 && a.incexc[ii+1] < 2) ){

				a.left[ii+1] = a.left[ii];
				if (a.incexc[ii+1]>= 2 && a.incexc[ii]<2){
					a.incexc[ii+1]-=2;
				}
				else if (a.incexc[ii+1]<2 && a.incexc[ii]>=2){
					a.incexc[ii+1]+=2;
				}
				a.left.erase(a.left.begin()+ii);
				a.right.erase(a.right.begin()+ii);
				a.incexc.erase(a.incexc.begin()+ii);
				return unionTwo(a,b);
			}
			else {
				a.right[ii] = b.right[bLast];
				if (b.incexc[bLast]%2 ==1 && a.incexc[ii]%2 ==0){
					a.incexc[ii]++;
				}
				else if (b.incexc[bLast]%2 ==0 && a.incexc[ii]%2 ==1){
					a.incexc[ii]--;
				}
				if (bLast>0){
					b.left.pop_back();
					b.right.pop_back();
					b.incexc.pop_back();
					return unionTwo(a,b);
				}
				else {
					return a;
				}
			}
		}
	}
	a.left.push_back(b.left[bLast]);
	a.right.push_back(b.right[bLast]);
	a.incexc.push_back(b.incexc[bLast]);
	return a;
}
Range intersectionTwo(Range a, Range b) {
	//TODO: add intersection logic
	return a;
}
Range solveRange(std::string postfix, std::vector<Range> rangeArray) {
	int i;
  	int currentIndex = 0;
  	int arrayIndex = 0;
  	std::vector<Range> stack = rangeArray;

    for (i=0; i<postfix.length(); i++) 
    { 
        if (postfix.at(i) == '#') {
        	stack[currentIndex] = rangeArray[arrayIndex];
        	currentIndex++;
        	arrayIndex++;
  
        } 
        else if (postfix.at(i) == '@') {
        	break;
        }
        else 
        { 
            switch (postfix.at(i)) 
            { 
	            case -91: {
	            	stack[currentIndex-2] = unionTwo(stack[currentIndex-2],stack[currentIndex-1]); break;
	            }  
	            case -92: {
	            	stack[currentIndex-2] = intersectionTwo(stack[currentIndex-2],stack[currentIndex-1]); break;
	            }          
            } 
            currentIndex--;
        } 
    } 



	return stack[0];
}
Range makeRange(std::string input){
	std::vector<std::string> rangeList;
	std::vector<Range> rangeArray;
	int n =0;
	int i; int ii;
	bool inRange = false;
	bool openPar = 0;
	int rangeStart = 0;
	int rangeEnd = 0;
	char unionc{-91};
	char intc{-92};
	std::string unions = "";
	unions += unionc;
	std::string ints = "";
	ints += intc;
	std::string ns = "";
	for (i=0;i<input.length();i++){
		switch (input.at(i)){
			case '[':{
				inRange = true;
				rangeStart = i;
				break;
			}
			case ']':{
				if (inRange){
					inRange = false;
					rangeEnd = i;
					rangeList.push_back(input.substr(rangeStart,rangeEnd+1-rangeStart));
					ns = std::to_string(n);
					input.replace(rangeStart,rangeEnd+1-rangeStart,ns);
					i-=rangeEnd+1-rangeStart-ns.length();
					n++;
				}
				break;
			}
			case '(':{
				inRange = true;
				rangeStart = i;
				break;
			}
			case ')':{
				if (inRange){
					inRange = false;
					rangeEnd = i;
					rangeList.push_back(input.substr(rangeStart,rangeEnd+1-rangeStart));
					ns = std::to_string(n);
					input.replace(rangeStart,rangeEnd+1-rangeStart,ns);
					i-=rangeEnd+1-rangeStart-ns.length();
					n++;
				}
				break;
			}
			case '{':{
				inRange = true;
				rangeStart = i;
				break;
			}
			case '}':{
				if (inRange){
					inRange = false;
					rangeEnd = i;
					rangeList.push_back(input.substr(rangeStart,rangeEnd+1-rangeStart));
					ns = std::to_string(n);
					input.replace(rangeStart,rangeEnd+1-rangeStart,ns);
					i-=rangeEnd+1-rangeStart-ns.length();
					n++;
				}
				break;
			}
			case 'U':{
				input.replace(i,1,unions);
				break;
			}
			case 'N':{
				input.replace(i,1,ints);
				break;
			}
			case 'I':{
				input.replace(i,1,ints);
				break;
			}
			default:{
			
			}
		}
	}

	std::string postfixed = postfixify(input);
	//std::cout << postfixed << "\n";
	for (i=0;i<rangeList.size();i++){
		Range r;
		std::string left = "";
		std::string right = "";
		bool isRight = false;
		for (ii=1;ii<rangeList[i].length()-1;ii++){
			if (rangeList[i].at(ii) == ','){
				isRight = true;
			}
			else if (isRight){
				right += rangeList[i].at(ii);
			}
			else {
				left += rangeList[i].at(ii);
			}
		}
		if (numbers.find(left) == numbers.end()){
			if (numberType(left) == "string"){
				std::cout << "is string: " << left << "\n";
			}
		}
		if (numbers.find(left) == numbers.end()){
			std::cout << "is string: " << left << "\n";
		}
		if (numbers.find(right) == numbers.end()){
			if (numberType(right) == "string"){
				std::cout << "is string: " << right << "\n";
			}
		}
		if (numbers.find(right) == numbers.end()){
			std::cout << "is string: " << right << "\n";
		}
		r.left.push_back(numbers[left]);
		r.right.push_back(numbers[right]);
		char incexc{0};
		if (rangeList[i].at(0)=='['){
			incexc += 2;
		}
		if (rangeList[i].at(rangeList[i].length()-1)==']'){
			incexc += 1;
		}
		r.incexc.push_back(incexc);
		//std::cout << r.left[0].top << "\n";
		//std::cout << r.right[0].top << "\n";
		rangeArray.push_back(r);
	}
	
	return solveRange(postfixed,rangeArray);
}
std::string makeInt(std::string input){
	Range outRange = makeRange(input);
	int n =0;
	int i;
	for (i=0;i<outRange.left.size();i++){
		n += (std::stoi(outRange.right[i].top) - std::stoi(outRange.left[i].top));
		//TODO: make this work for numbers outside of int range
		if (outRange.incexc[i] == 3){
			n++;
		}
		else if (outRange.incexc[i] ==0){
			n--;
		}
		std::cout << outRange.left[i].top << " and " << outRange.right[i].top << " and " << outRange.incexc[i] << "\n";
	}
	std::string out = "";
	//for (ii=0;ii<100;ii++){
		int x = rand() % n;
		std::cout << "x: " << x << " and n: " << n << "\n";
		int nn = 0;
		int nnn = 0;
		for (i=0;i<outRange.left.size();i++){
			nnn = 0;
			nnn += (std::stoi(outRange.right[i].top) - std::stoi(outRange.left[i].top));
			//TODO: make this work for numbers outside of int range
			if (outRange.incexc[i] == 3){
				nnn++;
			}
			else if (outRange.incexc[i] ==0){
				nnn--;
			}
			if (nn+nnn>x){
				if (outRange.incexc[i] >= 2){
					out = std::to_string(std::stoi(outRange.left[i].top) + x-nn);
					//std::cout << (std::stoi(outRange.left[i].top) + x-nn) << "  ";
					break;
				}
				else {
					out = std::to_string(std::stoi(outRange.left[i].top) + 1 + x-nn);
					//std::cout << (std::stoi(outRange.left[i].top) + 1 + x-nn) << "  ";
					break;
				}
			}
			nn += nnn;
			//std::cout << outRange.left[i].top << " and " << outRange.right[i].top << " and " << outRange.incexc[i] << "\n";
		}
	//}
	//std::cout << "\n";
	

	return out;
}