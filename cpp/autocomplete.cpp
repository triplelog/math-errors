
int lev(std::string ss, std::string st){
    int i,j,m,n,temp,tracker;
    
	m = ss.length(); 
    char s[m + 1]; 
    strcpy(s, ss.c_str());
    n = st.length(); 
    char t[n + 1]; 
    strcpy(t, st.c_str());
    
    int d[n+1][m+1];

    for(i=0;i<=m;i++){
    	d[0][i] = i;
    }

    for(j=0;j<=n;j++){
    	d[j][0] = j;
    }


    for (j=1;j<=m;j++) {

        for(i=1;i<=n;i++) {

            if(s[i-1] == t[j-1])

            {

                tracker = 0;

            }

            else

            {

                tracker = 1;

            }

            temp = MIN((d[i-1][j]+1),(d[i][j-1]+1));

            d[i][j] = MIN(temp,(d[i-1][j-1]+tracker));

        }

    }
    return d[n][m];

}

int autoDistance(std::string ss, std::string control) {
	int d = lev(ss,control)*1000;
	int ssl = ss.length();
	int cl = control.length();
	if (ssl == 0 || cl == 0){return 2000;}
	if (cl < ssl){
		ss.replace(cl,ssl-cl,"");
		d /= (ssl+3);
		d += lev(ss,control)*1000/(cl+3);
	}
	else {
		d /= (ssl+3);
		d += lev(ss,control)*1000/(cl+3);
	}
	return d;
}

void inputify() {
	int i; int ii; int iii;
	flat_hash_map<std::string,std::string> listMap;
	flat_hash_map<std::string,char> lastOpMap;
	for (flat_hash_map<std::string,Answer>::iterator iter = answerMap.begin(); iter != answerMap.end(); ++iter){
		std::string pfstr = iter->first;
		int idx = 0;
		bool startOperands = false;
		std::string currentOperator = "";
		flat_hash_map<int,std::string> originalMap;
		int iidx = 0;
		if (listMap.find(pfstr) != listMap.end()){
			answerMap[pfstr].input = listMap[pfstr];
			continue;
		}
	
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
	
	
	
		flat_hash_map<int,std::string> operandMap;
		std::string lastInput = "";
		std::string soFarLeft = "";
		std::string soFarRight = "";
		for (i=0;i<pfstr.length();i++){
			soFarLeft += pfstr.at(i);
			
			if (pfstr.at(i) == '@'){
				break;
			}
			else if (pfstr.at(i) != '#'){
				
				bool foundFull = false;
				std::string fullStr = "";
				for (ii=0;ii<i+1;ii++){
					std::string s = "";
					std::string t = "";
					for (iii=ii;iii<i+1;iii++){
						s += pfstr.at(iii);
						if (pfstr.at(iii) == '#'){
							t += operandMap[iii] + '_';
						}
					}
					if (listMap.find(s + '@' + t) != listMap.end()){
						foundFull = true;
						fullStr = s + '@' + t;
						break;
					}
				}
				if (foundFull){
					lastInput = listMap[fullStr];
					continue;
				}
				
				
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
				fullStr = firstStr + secondStr + pfstr.at(i) + '@' + firstTtr + secondTtr;
				
				std::string s = "";
				if (listMap.find(fullStr) != listMap.end()){
					lastInput = listMap[fullStr];
					continue;
				}
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
								s += "^";
								if (prec[lastOpMap[child]] < 100){
									s += "("+listMap[child]+")";
								}
								else {
									s += listMap[child];
								}
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
								s += "d/d"+listMap[child]+"[";
							}
							break;
			
						}
						case -85: {
							if (ii > 0){
								s.replace(6,0,listMap[child]+" d");
							}
							else {
								s += "int "+listMap[child]+"}";
							}
							break;
			
						}
						case -89: {
							if (ii > 0){
								s += listMap[child]+")";
							}
							else {
								s += listMap[child]+"(";
							}
							break;
			
						}
						case -34:
							s += "|"+listMap[child]+"|";
							break;
						case -64:
							s += "sin("+listMap[child]+")";
							break;
						case -63:
							s += "cos("+listMap[child]+")";
							break;
						case -62:
							s += "tan("+listMap[child]+")";
							break;
						case -61:
							s += "csc("+listMap[child]+")";
							break;
						case -60:
							s += "sec("+listMap[child]+")";
							break;
						case -59:
							s += "cot("+listMap[child]+")";
							break;
						case -32:
							s += "sin^(-1)("+listMap[child]+")";
							break;
						case -31:
							s += "cos^(-1)("+listMap[child]+")";
							break;
						case -30:
							s += "tan^(-1)("+listMap[child]+")";
							break;
						case -29:
							s += "csc^(-1)("+listMap[child]+")";
							break;
						case -28:
							s += "sec^(-1)("+listMap[child]+")";
							break;
						case -27:
							s += "cot^(-1)("+listMap[child]+")";
							break;
						case -16:
							s += "sinh("+listMap[child]+")";
							break;
						case -15:
							s += "cosh("+listMap[child]+")";
							break;
						case -14:
							s += "tanh("+listMap[child]+")";
							break;
						case -13:
							s += "csch("+listMap[child]+")";
							break;
						case -12:
							s += "sech("+listMap[child]+")";
							break;
						case -11:
							s += "coth("+listMap[child]+")";
							break;
						case -67:
							s += "sqrt("+listMap[child]+")";
							break;
						case -84: {
							if (ii > 0){
								s += listMap[child]+")";
							}
							else {
								s += "sqrt["+listMap[child]+"](";
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
									s += "ln";
								}
								else {
									s += "log_{"+listMap[child]+"}";
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
							s += "1/("+listMap[child]+")";
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
										s += "*("+listMap[child]+")";
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
										s += "*"+listMap[child];//want to move this into numerator somehow
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
										s += "*"+listMap[child];
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
				soFarRight += originalMap[idx] + '_';
				listMap["#@" + originalMap[idx] + "_"]=originalMap[idx];
				lastOpMap["#@" + originalMap[idx] + "_"]='#';
				operandMap[i]=originalMap[idx];
				lastInput = originalMap[idx];
				idx++;
			}
		
		}
		answerMap[iter->first].input = lastInput;
	}



}

struct Autocomplete {
	int d = 2000;
	std::string answer = "";
	//inline Cppdata operator+=(Cppdata const &b);
};
inline bool operator<(const Autocomplete a, const Autocomplete b){
	if (a.d < b.d){return true;}
	return false;
}

std::vector<std::string> autocomplete(std::string newPostfix,std::string rawAnswer){

	std::vector<Autocomplete> answers;
	std::vector<Autocomplete> shortAnswers;
	int i;
	int ias = 0;
	for (flat_hash_map<std::string,Answer>::iterator iter = answerMap.begin(); iter != answerMap.end(); ++iter){
		
		ias++;
	}
	//std::cout << "ias: " << ias << "\n";
	answers.resize(ias);
	//shortAnswers.resize(ias);
	
	i = 0;
	for (flat_hash_map<std::string,Answer>::iterator iter = answerMap.begin(); iter != answerMap.end(); ++iter){
	
		
		std::string ca = iter->second.input;
		
		Autocomplete answer;
		answer.d = autoDistance(ca,rawAnswer);
		answer.answer = iter->first;
		answers[i] = answer;
		i++;
		//std::cout << "distance: " << autoDistance(ca,rawAnswer) << " of "<< iter->first << "\n";
		
	}
	if (ias > 12){
		ias = 12;
	}

	std::partial_sort(answers.begin(),answers.begin()+ias,answers.end());

	
	std::vector<std::string> returnAnswers;
	returnAnswers.resize(ias);
	for (i=0;i<ias;i++){
		returnAnswers[i] = answers[i].answer;
		//std::cout << answers[i].answer << " with d="<< answers[i].d <<"\n";
	}
	return returnAnswers;
	
	//std::cout << "question: " << inputify(newPostfix) << "with " << answers.size() << "\n";
	//std::cout << "user answer: " << rawAnswer << "\n";
	
}