std::string makeInt(std::string input){
	std::vector<std::string> union;
	std::vector<std::string> rangeList;
	int n =0;
	int i;
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
					ns = std::to_string(n)''
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
					ns = std::to_string(n)''
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
					ns = std::to_string(n)''
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
	//TODO: postfix the new input
	std::string postfixed = postfixify(input);
	std::cout << postfixed << "\n";
	//TODO: solve the postfix to create disjoint union
	return postfixed;
}