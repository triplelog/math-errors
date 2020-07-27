struct Range {
	std::vector<Number> left;
	std::vector<Number> right;
	std::vector<char> incexc;
};



std::string makeInt(std::string input){
	std::vector<std::string> stack;
	std::vector<std::string> rangeList;
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
		std::cout << "newInput:" << input << " @ " << i << "\n";
	}
	//TODO: postfix the new input
	std::cout << "newInput:" << input << "\n";
	std::string postfixed = postfixify(input);
	std::cout << postfixed << "\n";
	for (i=0;i<rangeList;i++){
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
		std::cout << r.left[0].top << "\n";
		std::cout << r.right[0].top << "\n";
	}
	//TODO: solve the postfix to create disjoint union
	return postfixed;
}