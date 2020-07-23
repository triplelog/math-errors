std::string inputify(std::string input) {

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
	for (i=0;i<pfstr.length();i++){
		std::cout << "i: " << i << " and " << pfstr << "\n";
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
				if (ii=0 && firstChild != ""){
					child = firstChild;
				}
				else if (ii=1 && firstChild == ""){
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
								s += "\\\\left("+listMap[child]+"\\\\right)";
							}
							else {
								s += listMap[child];
							}
						}
						break;
					}
					case -69: {
						if (ii > 0){
							s += listMap[child]+"\\\\right]";
						}
						else {
							s += "\\\\frac{d}{d"+listMap[child]+"}\\\\left[";
						}
						break;
			
					}
					case -85: {
						if (ii > 0){
							s.replace(6,0,listMap[child]+" \\\\text{d");
						}
						else {
							s += "\\\\int "+listMap[child]+"}";
						}
						break;
			
					}
					case -34:
						s += "|"+listMap[child]+"|";
						break;
					case -64:
						s += "\\\\sin\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -63:
						s += "\\\\cos\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -62:
						s += "\\\\tan\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -61:
						s += "\\\\csc\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -60:
						s += "\\\\sec\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -59:
						s += "\\\\cot\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -32:
						s += "\\\\sin^{-1}\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -31:
						s += "\\\\cos^{-1}\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -30:
						s += "\\\\tan^{-1}\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -29:
						s += "\\\\csc^{-1}\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -28:
						s += "\\\\sec^{-1}\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -27:
						s += "\\\\cot^{-1}\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -16:
						s += "\\\\text{sinh}\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -15:
						s += "\\\\text{cosh}\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -14:
						s += "\\\\text{tanh}\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -13:
						s += "\\\\text{csch}\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -12:
						s += "\\\\text{sech}\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -11:
						s += "\\\\text{coth}\\\\left("+listMap[child]+"\\\\right)";
						break;
					case -67:
						s += "\\\\sqrt{"+listMap[child]+"}";
						break;
					case -84: {
						if (ii > 0){
							s += listMap[child]+"}";
						}
						else {
							s += "\\\\sqrt["+listMap[child]+"]{";
						}
						break;
			
					}
					case -93: {
						if (ii > 0){
							if (prec[lastOpMap[child]] < 100){
								s += "\\\\left("+listMap[child]+"\\\\right)";
							}
							else {
								s += listMap[child];
							}
					
						}
						else {
							if (listMap[child] == "e"){
								s += "\\\\ln ";
							}
							else {
								s += "\\\\log_{"+listMap[child]+"} ";
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
						s += "\\\\frac{1}{"+listMap[child]+"}";
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
									s += "\\\\cdot ("+listMap[child]+")";
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
									s += "\\\\cdot "+listMap[child];//want to move this into numerator somehow
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
									s += "\\\\cdot "+listMap[child];
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
			
		}
		else {
			listMap["#@" + std::to_string(idx) + "_"]=originalMap[idx];
			operandMap[i]=std::to_string(idx);
			idx++;
		}
		
	}
	
	
	

	
	return listMap[input];


}
std::vector<std::string> autocomplete(flat_hash_map<std::string,std::vector<std::string>> reverseMap, std::string newPostfix,std::string mpf){
	std::cout << "to input: " << mpf << "\n";
	std::string answerInput = inputify(mpf);
	std::cout << answerInput << "\n";
	//for (flat_hash_map<std::string,std::vector<std::string>>::iterator iter = reverseMap.begin(); iter != reverseMap.end(); ++iter){
		//std::cout << iter->first << "\n";
	//}
}