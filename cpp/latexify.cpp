

flat_hash_map<std::string,std::string> toLatex(std::vector<std::string> input){
	int i; int ii;
	flat_hash_map<std::string,std::string> latexMap;
	flat_hash_map<std::string,char> lastOpMap;
	flat_hash_map<std::string,std::vector<std::string>> childMap;
	childMap[""]={};
	for (i=0;i<input.size()/3;i++){
		//std::cout << input[i*3] << "\n";
		//std::cout << input[i*3+1] << "\n";
		//std::cout << input[i*3+2] << "\n";
		char lastOp = '#';
		bool foundAt = false;
		std::string firstOperand = "";
		for (ii=0;ii<input[i*3+2].size();ii++){
			if (input[i*3+2].at(ii) == '@'){
				foundAt = true;
			}
			else if (!foundAt){
				lastOp = input[i*3+2].at(ii);
			}
			else if (input[i*3+2].at(ii) == '_'){
				break;
			}
			else {
				firstOperand += input[i*3+2].at(ii);
			}
		}
		latexMap[input[i*3]]="";
		childMap[input[i*3]]={};
		childMap[input[i*3+1]].push_back(input[i*3]);
		if (lastOp == '#'){
			latexMap[input[i*3]]=firstOperand;
			lastOpMap[input[i*3]]='#';
			//std::cout << firstOperand << " is first s of: " << input[i*3] <<"\n";
		}
		else {
			lastOpMap[input[i*3]]=lastOp;
		}
	}
	int newLatex = 1;
	int count =0;
	while (newLatex>0 && count < 1000){
		newLatex = 0;
		for (i=0;i<input.size()/3;i++){
			bool allChildren = true;
			std::string s = "";
			for (ii=0;ii<childMap[input[i*3]].size();ii++){
				std::string child = childMap[input[i*3]][ii]; //is name of child
				//std::cout << "child: " << child << " latex of child: " << latexMap[child] << " and s: " << s << "\n";
				if (latexMap[child] == ""){
					allChildren = false;
					break;
				}
				else {
					switch (lastOpMap[input[i*3]]){
						case '^': {
							if (ii > 0){
								s += "^{";
								s += latexMap[child]+"}";
							}
							else {
								if (prec[lastOpMap[child]] < 100){
									s += "("+latexMap[child]+")";
								}
								else {
									s += latexMap[child];
								}
							}
							break;
						}
						case -69: {
							if (ii > 0){
								s += latexMap[child]+"]";
							}
							else {
								s += "\\frac{d}{d"+latexMap[child]+"}[";
							}
							break;
			
						}
						case -85: {
							if (ii > 0){
								s.replace(6,0,latexMap[child]+" \\text{d");
							}
							else {
								s += "\\int "+latexMap[child]+"}";
							}
							break;
			
						}
						case -34:
							s += "|"+latexMap[child]+"|";
							break;
						case -64:
							s += "\\sin("+latexMap[child]+")";
							break;
						case -63:
							s += "\\cos("+latexMap[child]+")";
							break;
						case -62:
							s += "\\tan("+latexMap[child]+")";
							break;
						case -61:
							s += "\\csc("+latexMap[child]+")";
							break;
						case -60:
							s += "\\sec("+latexMap[child]+")";
							break;
						case -59:
							s += "\\cot("+latexMap[child]+")";
							break;
						case -32:
							s += "\\sin^{-1}("+latexMap[child]+")";
							break;
						case -31:
							s += "\\cos^{-1}("+latexMap[child]+")";
							break;
						case -30:
							s += "\\tan^{-1}("+latexMap[child]+")";
							break;
						case -29:
							s += "\\csc^{-1}("+latexMap[child]+")";
							break;
						case -28:
							s += "\\sec^{-1}("+latexMap[child]+")";
							break;
						case -27:
							s += "\\cot^{-1}("+latexMap[child]+")";
							break;
						case -16:
							s += "\\text{sinh}("+latexMap[child]+")";
							break;
						case -15:
							s += "\\text{cosh}("+latexMap[child]+")";
							break;
						case -14:
							s += "\\text{tanh}("+latexMap[child]+")";
							break;
						case -13:
							s += "\\text{csch}("+latexMap[child]+")";
							break;
						case -12:
							s += "\\text{sech}("+latexMap[child]+")";
							break;
						case -11:
							s += "\\text{coth}("+latexMap[child]+")";
							break;
						case -67:
							s += "\\sqrt{"+latexMap[child]+"}";
							break;
						case -84: {
							if (ii > 0){
								s += latexMap[child]+"}";
							}
							else {
								s += "\\sqrt["+latexMap[child]+"]{";
							}
							break;
			
						}
						case -93: {
							if (ii > 0){
								if (prec[lastOpMap[child]] < 100){
									s += "("+latexMap[child]+")";
								}
								else {
									s += latexMap[child];
								}
					
							}
							else {
								if (latexMap[child] == "e"){
									s += "\\ln ";
								}
								else {
									s += "\\log_{"+latexMap[child]+"} ";
								}
							}
							break;
			
						}
						case '-': {
							if (prec['-'] >= prec[lastOpMap[child]]){
								s += "-("+latexMap[child]+")";
							}
							else {
								s += "-"+latexMap[child];
							}
							break;
						}
						case '/': {
							s += "\\frac{1}{"+latexMap[child]+"}";
							/*
							if (prec['/'] >= prec[lastOpMap[child]]){
								s += "/("+latexMap[child]+")";
							}
							else {
								s += "/"+latexMap[child];
							}*/
							break;
						}
						default: {
							char thisChar = lastOpMap[input[i*3]];
							if (prec[thisChar] > prec[lastOpMap[child]]){
								if (ii > 0){
									if (thisChar == '*'){
										if (s.length()>0 && (s.at(s.length()-1) >= '0' && s.at(s.length()-1) <= '9')){
											s += "("+latexMap[child]+")";
										}
										else {
											s += "\\cdot ("+latexMap[child]+")";//want to move this into numerator somehow
										}
									
									}
									else {
										s += thisChar+"("+latexMap[child]+")";
									}
								}
								else {
									s += "("+latexMap[child]+")";
								}
							}
							else if (prec[thisChar] == prec[lastOpMap[child]] && thisChar != lastOpMap[child]){
								if (ii > 0){
									if (thisChar == '*'){
										if (s.length()>0 && (s.at(s.length()-1) >= '0' && s.at(s.length()-1) <= '9')){
											if (latexMap[child].length()>0 && (latexMap[child].at(0) >= '0' && latexMap[child].at(0) <= '9')){
												//digit followed by digit
												s += "\\cdot "+latexMap[child];
											}
											else{
												//digit followed by not a digit
												s += latexMap[child];
											}
										}
										else {
											s += "\\cdot "+latexMap[child];//want to move this into numerator somehow
										}
									
									}
									else if (thisChar == '+'){
										s += latexMap[child];
									}
									else {
										s += thisChar+"("+latexMap[child]+")";
									}
								}
								else {
									if (thisChar == '*'){
										s += latexMap[child];
									}
									else if (thisChar == '+'){
										s += latexMap[child];
									}
									else {
										s += "("+latexMap[child]+")";
									}
								}
							}
							else {
								if (ii > 0){
									if (thisChar == '*'){
										if (s.length()>0 && (s.at(s.length()-1) >= '0' && s.at(s.length()-1) <= '9')){
											if (latexMap[child].length()>0 && (latexMap[child].at(0) >= '0' && latexMap[child].at(0) <= '9')){
												//digit followed by digit
												s += "\\cdot "+latexMap[child];
											}
											else{
												//digit followed by not a digit
												s += latexMap[child];
											}
										}
										else {
											s += "\\cdot "+latexMap[child];//want to move this into numerator somehow
										}
									}
									else {
										s += thisChar+latexMap[child];
									}
								}
								else {
									s += latexMap[child];
								}
							}
						}
					}
					
				}
			}
			if (allChildren && latexMap[input[i*3]]=="" && s != ""){
				newLatex++;
				latexMap[input[i*3]]=s;
				//std::cout << "\ns: "<< s << " is s for " << input[i*3] << "\n";
			}
		}
		count++;
	}

	
	return latexMap;
}

std::string latexOne(std::string input) {
	std::vector<std::string> inputs = {"node","",input};
	flat_hash_map<std::string,std::string> latexMap = toLatex(inputs);
	return latexMap["node"];
	
	int i; int ii; int iii; int idx = 0;
	bool startOperands = false;
	std::string currentOperator = "";
	flat_hash_map<int,std::string> originalMap;
	int iidx = 0;
	std::string pfstr = input;
	
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
	
	flat_hash_map<std::string,std::string> listMap;
	flat_hash_map<std::string,char> lastOpMap;
	
	flat_hash_map<int,std::string> operandMap;
	std::string lastInput = "";
	for (i=0;i<pfstr.length();i++){
		if (pfstr.at(i) == '@'){
			break;
		}
		else if (pfstr.at(i) != '#'){
			std::string secondStr = "";
			std::string secondTtr = "";
			std::string secondChild = "";
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
					secondChild = s + '@' + t;
					maxi = ii;
					break;
				}
			}
			std::string firstStr = "";
			std::string firstTtr = "";
			std::string firstChild = "";
			std::vector<std::string> fullTrees;
			
			if (pfstr.at(i) != '-' && pfstr.at(i) != '/' && (pfstr.at(i) >= 0 || pfstr.at(i) <= -69 )){ // Is at least binary function
				
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
						firstChild = s + '@' + t;
						break;
					}
				}
				
				
			}
			std::string fullStr = firstStr + secondStr + pfstr.at(i) + '@' + firstTtr + secondTtr;
			
			std::string s = "";
			for (ii=0;ii<2;ii++){
				std::string child = secondChild;
				if (ii==0 && firstChild != ""){
					child = firstChild;
				}
				else if (ii==1 && firstChild == ""){
					break;
				}
				switch (pfstr.at(i)){
					case '^': {
						if (ii > 0){
							s += "^{";
							s += listMap[child]+"}";
						}
						else {
							if (prec[lastOpMap[child]] < 100){
								s += "("+listMap[child]+")";
							}
							else {
								s += listMap[child];
							}
						}
						break;
					}
					case -69: {
						if (ii > 0){
							s += listMap[child]+"]";
						}
						else {
							s += "\\frac{d}{d"+listMap[child]+"}[";
						}
						break;
			
					}
					case -85: {
						if (ii > 0){
							s.replace(6,0,listMap[child]+" \\text{d");
						}
						else {
							s += "\\int "+listMap[child]+"}";
						}
						break;
			
					}
					case -34:
						s += "|"+listMap[child]+"|";
						break;
					case -64:
						s += "\\sin("+listMap[child]+")";
						break;
					case -63:
						s += "\\cos("+listMap[child]+")";
						break;
					case -62:
						s += "\\tan("+listMap[child]+")";
						break;
					case -61:
						s += "\\csc("+listMap[child]+")";
						break;
					case -60:
						s += "\\sec("+listMap[child]+")";
						break;
					case -59:
						s += "\\cot("+listMap[child]+")";
						break;
					case -32:
						s += "\\sin^{-1}("+listMap[child]+")";
						break;
					case -31:
						s += "\\cos^{-1}("+listMap[child]+")";
						break;
					case -30:
						s += "\\tan^{-1}("+listMap[child]+")";
						break;
					case -29:
						s += "\\csc^{-1}("+listMap[child]+")";
						break;
					case -28:
						s += "\\sec^{-1}("+listMap[child]+")";
						break;
					case -27:
						s += "\\cot^{-1}("+listMap[child]+")";
						break;
					case -16:
						s += "\\text{sinh}("+listMap[child]+")";
						break;
					case -15:
						s += "\\text{cosh}("+listMap[child]+")";
						break;
					case -14:
						s += "\\text{tanh}("+listMap[child]+")";
						break;
					case -13:
						s += "\\text{csch}("+listMap[child]+")";
						break;
					case -12:
						s += "\\text{sech}("+listMap[child]+")";
						break;
					case -11:
						s += "\\text{coth}("+listMap[child]+")";
						break;
					case -67:
						s += "\\sqrt{"+listMap[child]+"}";
						break;
					case -84: {
						if (ii > 0){
							s += listMap[child]+"}";
						}
						else {
							s += "\\sqrt["+listMap[child]+"]{";
						}
						break;
			
					}
					case -93: {
						if (ii > 0){
							if (prec[lastOpMap[child]] < 100){
								s += "("+listMap[child]+")";
							}
							else {
								s += listMap[child];
							}
					
						}
						else {
							if (listMap[child] == "e"){
								s += "\\ln ";
							}
							else {
								s += "\\log_{"+listMap[child]+"} ";
							}
						}
						break;
			
					}
					case '-': {
						if (prec[pfstr.at(i)] >= prec[lastOpMap[child]]){
							s += "-("+listMap[child]+")";
						}
						else {
							s += "-"+listMap[child];
						}
						break;
					}
					case '/': {
						s += "\\frac{1}{"+listMap[child]+"}";
						/*
						if (prec[pfstr.at(i)] >= prec[lastOpMap[child]]){
							s += "/("+listMap[child]+")";
						}
						else {
							s += "/"+listMap[child];
						}*/
						break;
					}
					default: {
						if (prec[pfstr.at(i)] > prec[lastOpMap[child]]){
							if (ii > 0){
								if (pfstr.at(i) == '*'){
									if (s.length()>0 && (s.at(s.length()-1) >= '0' && s.at(s.length()-1) <= '9')){
										s += "("+listMap[child]+")";
									}
									else {
										s += "\\cdot ("+listMap[child]+")";//want to move this into numerator somehow
									}
									
								}
								else {
									s += pfstr.at(i)+"("+listMap[child]+")";
								}
							}
							else {
								s += "("+listMap[child]+")";
							}
						}
						else if (prec[pfstr.at(i)] == prec[lastOpMap[child]] && pfstr.at(i) != lastOpMap[child]){
							if (ii > 0){
								if (pfstr.at(i) == '*'){
									if (s.length()>0 && (s.at(s.length()-1) >= '0' && s.at(s.length()-1) <= '9')){
										if (listMap[child].length()>0 && (listMap[child].at(0) >= '0' && listMap[child].at(0) <= '9')){
											//digit followed by digit
											s += "\\cdot "+listMap[child];
										}
										else{
											//digit followed by not a digit
											s += listMap[child];
										}
									}
									else {
										s += "\\cdot "+listMap[child];//want to move this into numerator somehow
									}
									
								}
								else if (pfstr.at(i) == '+'){
									s += listMap[child];
								}
								else {
									s += pfstr.at(i)+"("+listMap[child]+")";
								}
							}
							else {
								if (pfstr.at(i) == '*'){
									s += listMap[child];
								}
								else if (pfstr.at(i) == '+'){
									s += listMap[child];
								}
								else {
									s += "("+listMap[child]+")";
								}
							}
						}
						else {
							if (ii > 0){
								if (pfstr.at(i) == '*'){
									if (s.length()>0 && (s.at(s.length()-1) >= '0' && s.at(s.length()-1) <= '9')){
										if (listMap[child].length()>0 && (listMap[child].at(0) >= '0' && listMap[child].at(0) <= '9')){
											//digit followed by digit
											s += "\\cdot "+listMap[child];
										}
										else{
											//digit followed by not a digit
											s += listMap[child];
										}
									}
									else {
										s += "\\cdot "+listMap[child];//want to move this into numerator somehow
									}
								}
								else {
									s += pfstr.at(i)+listMap[child];
								}
							}
							else {
								s += listMap[child];
							}
						}
					}
				}
			}
			
			listMap[fullStr]=s;
			lastOpMap[fullStr]=pfstr.at(i);
			lastInput = s;
			
		}
		else {
			listMap["#@" + std::to_string(idx) + "_"]=originalMap[idx];
			lastOpMap["#@" + std::to_string(idx) + "_"]='#';
			operandMap[i]=std::to_string(idx);
			lastInput = originalMap[idx];
			idx++;
		}
		
	}
	
	//std::cout << lastInput << "\n";
	return lastInput;
	

}

std::string latexBoxed(std::string input,int startNode,flat_hash_map<int,bool> bMap) {

	int i; int ii; int iii; int idx = 0;
	bool startOperands = false;
	std::string currentOperator = "";
	flat_hash_map<int,std::string> originalMap;
	int iidx = 0;
	std::string pfstr = input;
	int startAt =0;
	for (i=0;i<pfstr.length();i++){
		if (pfstr.at(i) == '@'){
			startOperands = true;
			startAt = i;
		}
		else if (pfstr.at(i) == '('){
			flat_hash_map<int,int> m = removeParList({},pfstr);
			pfstr = removeParOne(pfstr);
			
			int offset = 0;
			flat_hash_map<int,bool> mm;
			for (iii=0;iii<startAt;iii++){
				if (m.find(iii+offset) != m.end()){
					offset += m[iii+offset]-1;
					mm[iii+offset]=true;
				}
			}
					
			return latexBoxed(pfstr,-1,mm);
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
	
	flat_hash_map<std::string,std::string> listMap;
	flat_hash_map<std::string,char> lastOpMap;
	
	flat_hash_map<int,std::string> operandMap;
	std::string lastInput = "";
	for (i=0;i<pfstr.length();i++){
		if (pfstr.at(i) == '@'){
			break;
		}
		else if (pfstr.at(i) != '#'){
			std::string secondStr = "";
			std::string secondTtr = "";
			std::string secondChild = "";
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
					secondChild = s + '@' + t;
					maxi = ii;
					break;
				}
			}
			std::string firstStr = "";
			std::string firstTtr = "";
			std::string firstChild = "";
			std::vector<std::string> fullTrees;
			
			if (pfstr.at(i) != '-' && pfstr.at(i) != '/' && (pfstr.at(i) >= 0 || pfstr.at(i) <= -69 )){ // Is at least binary function
				
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
						firstChild = s + '@' + t;
						break;
					}
				}
				
				
			}
			std::string fullStr = firstStr + secondStr + pfstr.at(i) + '@' + firstTtr + secondTtr;
			
			std::string s = "";
			for (ii=0;ii<2;ii++){
				std::string child = secondChild;
				if (ii==0 && firstChild != ""){
					child = firstChild;
				}
				else if (ii==1 && firstChild == ""){
					break;
				}
				switch (pfstr.at(i)){
					case '^': {
						if (ii > 0){
							s += "^{";
							s += listMap[child]+"}";
						}
						else {
							if (prec[lastOpMap[child]] < 100){
								s += "("+listMap[child]+")";
							}
							else {
								s += listMap[child];
							}
						}
						break;
					}
					case -69: {
						if (ii > 0){
							s += listMap[child]+"]";
						}
						else {
							s += "\\frac{d}{d"+listMap[child]+"}[";
						}
						break;
			
					}
					case -85: {
						if (ii > 0){
							s.replace(6,0,listMap[child]+" \\text{d");
						}
						else {
							s += "\\int "+listMap[child]+"}";
						}
						break;
			
					}
					case -34:
						s += "|"+listMap[child]+"|";
						break;
					case -64:
						s += "\\sin("+listMap[child]+")";
						break;
					case -63:
						s += "\\cos("+listMap[child]+")";
						break;
					case -62:
						s += "\\tan("+listMap[child]+")";
						break;
					case -61:
						s += "\\csc("+listMap[child]+")";
						break;
					case -60:
						s += "\\sec("+listMap[child]+")";
						break;
					case -59:
						s += "\\cot("+listMap[child]+")";
						break;
					case -32:
						s += "\\sin^{-1}("+listMap[child]+")";
						break;
					case -31:
						s += "\\cos^{-1}("+listMap[child]+")";
						break;
					case -30:
						s += "\\tan^{-1}("+listMap[child]+")";
						break;
					case -29:
						s += "\\csc^{-1}("+listMap[child]+")";
						break;
					case -28:
						s += "\\sec^{-1}("+listMap[child]+")";
						break;
					case -27:
						s += "\\cot^{-1}("+listMap[child]+")";
						break;
					case -16:
						s += "\\text{sinh}("+listMap[child]+")";
						break;
					case -15:
						s += "\\text{cosh}("+listMap[child]+")";
						break;
					case -14:
						s += "\\text{tanh}("+listMap[child]+")";
						break;
					case -13:
						s += "\\text{csch}("+listMap[child]+")";
						break;
					case -12:
						s += "\\text{sech}("+listMap[child]+")";
						break;
					case -11:
						s += "\\text{coth}("+listMap[child]+")";
						break;
					case -67:
						s += "\\sqrt{"+listMap[child]+"}";
						break;
					case -84: {
						if (ii > 0){
							s += listMap[child]+"}";
						}
						else {
							s += "\\sqrt["+listMap[child]+"]{";
						}
						break;
			
					}
					case -93: {
						if (ii > 0){
							if (prec[lastOpMap[child]] < 100){
								s += "("+listMap[child]+")";
							}
							else {
								s += listMap[child];
							}
					
						}
						else {
							if (listMap[child] == "e"){
								s += "\\ln ";
							}
							else {
								s += "\\log_{"+listMap[child]+"} ";
							}
						}
						break;
			
					}
					case '-': {
						if (prec[pfstr.at(i)] >= prec[lastOpMap[child]]){
							s += "-("+listMap[child]+")";
						}
						else {
							s += "-"+listMap[child];
						}
						break;
					}
					case '/': {
						s += "\\frac{1}{"+listMap[child]+"}";
						/*
						if (prec[pfstr.at(i)] >= prec[lastOpMap[child]]){
							s += "/("+listMap[child]+")";
						}
						else {
							s += "/"+listMap[child];
						}*/
						break;
					}
					default: {
						if (prec[pfstr.at(i)] > prec[lastOpMap[child]]){
							if (ii > 0){
								if (pfstr.at(i) == '*'){
									if (s.length()>0 && (s.at(s.length()-1) >= '0' && s.at(s.length()-1) <= '9')){
										s += "("+listMap[child]+")";
									}
									else {
										s += "\\cdot ("+listMap[child]+")";//want to move this into numerator somehow
									}
									
								}
								else {
									s += pfstr.at(i)+"("+listMap[child]+")";
								}
							}
							else {
								s += "("+listMap[child]+")";
							}
						}
						else if (prec[pfstr.at(i)] == prec[lastOpMap[child]] && pfstr.at(i) != lastOpMap[child]){
							if (ii > 0){
								if (pfstr.at(i) == '*'){
									if (s.length()>0 && (s.at(s.length()-1) >= '0' && s.at(s.length()-1) <= '9')){
										if (listMap[child].length()>0 && (listMap[child].at(0) >= '0' && listMap[child].at(0) <= '9')){
											//digit followed by digit
											s += "\\cdot "+listMap[child];
										}
										else{
											//digit followed by not a digit
											s += listMap[child];
										}
									}
									else {
										s += "\\cdot "+listMap[child];//want to move this into numerator somehow
									}
									
								}
								else if (pfstr.at(i) == '+'){
									s += listMap[child];
								}
								else {
									s += pfstr.at(i)+"("+listMap[child]+")";
								}
							}
							else {
								if (pfstr.at(i) == '*'){
									s += listMap[child];
								}
								else if (pfstr.at(i) == '+'){
									s += listMap[child];
								}
								else {
									s += "("+listMap[child]+")";
								}
							}
						}
						else {
							if (ii > 0){
								if (pfstr.at(i) == '*'){
									if (s.length()>0 && (s.at(s.length()-1) >= '0' && s.at(s.length()-1) <= '9')){
										if (listMap[child].length()>0 && (listMap[child].at(0) >= '0' && listMap[child].at(0) <= '9')){
											//digit followed by digit
											s += "\\cdot "+listMap[child];
										}
										else{
											//digit followed by not a digit
											s += listMap[child];
										}
									}
									else {
										s += "\\cdot "+listMap[child];//want to move this into numerator somehow
									}
								}
								else {
									s += pfstr.at(i)+listMap[child];
								}
							}
							else {
								s += listMap[child];
							}
						}
					}
				}
			}
			
			if (i == startNode){
				s = "\\boxed{"+s+"}";
			}
			else if (bMap.find(i) != bMap.end()){
				s = "\\{\\{"+s+"\\}\\}";
			}
			listMap[fullStr]=s;
			lastOpMap[fullStr]=pfstr.at(i);
			lastInput = s;
			
		}
		else {
			std::string s = originalMap[idx];
			if (i == startNode){
				s = "\\boxed{"+s+"}";
			}
			else if (bMap.find(i) != bMap.end()){
				s = "\\{\\{"+s+"\\}\\}";
			}
			listMap["#@" + std::to_string(idx) + "_"]=s;
			lastOpMap["#@" + std::to_string(idx) + "_"]='#';
			operandMap[i]=std::to_string(idx);
			lastInput = s;
			idx++;
		}
		
	}
	
	//std::cout << lastInput << "\n";
	return lastInput;


}