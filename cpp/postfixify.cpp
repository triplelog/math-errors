std::string replaceFunctions(std::string input_str){
	flat_hash_map<std::string,std::string> replacements2;
	flat_hash_map<std::string,std::string> replacements3;
	flat_hash_map<std::string,std::string> replacements4;
	flat_hash_map<std::string,std::string> replacements5;
	flat_hash_map<std::string,std::string> replacements6;
	flat_hash_map<std::string,std::string> replacements7;
	flat_hash_map<std::string,std::string> replacements8;
	
	flat_hash_map<std::string,std::string> query4;
	flat_hash_map<std::string,std::string> query3;
	flat_hash_map<std::string,std::string> query2;
	
	char ddx{-69};
	char idx{-85};
	int i; int ii;
	replacements3["ddx"]="x";
	replacements3["ddx"]+=ddx;

	query3["dd?"]="";
	query3["dd?"]+=ddx;
	query3["der"]="";
	query3["der"]+=ddx;
	replacements3["idx"]="x";
	replacements3["idx"]+=idx;

	query3["id?"]="";
	query3["id?"]+=idx;
	query3["int"]="";
	query3["int"]+=idx;
	
	std::vector<std::string> trigFunctions;
	trigFunctions.push_back("sin");
	trigFunctions.push_back("cos");
	trigFunctions.push_back("tan");
	trigFunctions.push_back("csc");
	trigFunctions.push_back("sec");
	trigFunctions.push_back("cot");

	for (i=0;i<6;i++){
		char c{-64};
		c += i;
		char ci{-32};
		ci += i;
		char ch{-16};
		ch += i;
		replacements3[trigFunctions[i]]="";
		replacements3[trigFunctions[i]]+=c;
		replacements4[trigFunctions[i]+"h"]="";
		replacements4[trigFunctions[i]+"h"]+=ch;
		replacements6["arc"+trigFunctions[i]]="";
		replacements6["arc"+trigFunctions[i]]+=ci;
		replacements6[trigFunctions[i]+"^-1"]="";
		replacements6[trigFunctions[i]+"^-1"]+=ci;
		replacements8[trigFunctions[i]+"^(-1)"]="";
		replacements8[trigFunctions[i]+"^(-1)"]+=ci;
		replacements8[trigFunctions[i]+"^{-1}"]="";
		replacements8[trigFunctions[i]+"^{-1}"]+=ci;
		replacements5[trigFunctions[i]+"-1"]="";
		replacements5[trigFunctions[i]+"-1"]+=ci;
		query4[trigFunctions[i]+"^"]="";
		query4[trigFunctions[i]+"^"]+=c;
	}
	
	
	char sqrt{-67};
	char root{-84};
	replacements4["sqrt"]="";
	replacements4["sqrt"]+=sqrt;
	replacements4["root"]="";
	replacements4["root"]+=sqrt;
	//TODO: add nth roots
	
	
	
	char log{-93};
	replacements3["log"]="e";
	replacements3["log"]+=log;
	replacements2["ln"]="e";
	replacements2["ln"]+=log;
	query3["log"]="";
	query3["log"]+=log;
	query2["ln"]="";
	query2["ln"]+=log;
	//TODO: add other bases
	
	char abs{-34};
	replacements3["abs"]="";
	replacements3["abs"]+=abs;
	
	
	std::string twoChars = "..";
	std::string threeChars = "...";
	std::string fourChars = "....";
	std::string fiveChars = ".....";
	std::string sixChars = "......";
	std::string sevenChars = ".......";
	std::string eightChars = "........";
	
	for (i=0;i<input_str.length()-1;i++){
		twoChars.replace(0,1,"");
		twoChars += input_str.at(i);
		threeChars.replace(0,1,"");
		threeChars += input_str.at(i);
		fourChars.replace(0,1,"");
		fourChars += input_str.at(i);
		fiveChars.replace(0,1,"");
		fiveChars += input_str.at(i);
		sixChars.replace(0,1,"");
		sixChars += input_str.at(i);
		sevenChars.replace(0,1,"");
		sevenChars += input_str.at(i);
		eightChars.replace(0,1,"");
		eightChars += input_str.at(i);
		
		if (input_str.at(i+1) == '('){
			std::cout << i << " : " << input_str << " 3chars: " << threeChars << '\n';
			if (replacements8.find(eightChars) != replacements8.end()){
				input_str.replace(i-7,8,replacements8[eightChars]);
				eightChars = "...";
				i+= replacements8[eightChars].length() - 8;
			}
			else if (replacements7.find(sevenChars) != replacements7.end()){
				input_str.replace(i-6,7,replacements7[sevenChars]);
				sevenChars = "...";
				i+= replacements7[sevenChars].length() - 7;
			}
			else if (replacements6.find(sixChars) != replacements6.end()){
				input_str.replace(i-5,6,replacements6[sixChars]);
				sixChars = "...";
				i+= replacements6[sixChars].length() - 6;
			}
			else if (replacements5.find(fiveChars) != replacements5.end()){
				input_str.replace(i-4,5,replacements5[fiveChars]);
				fiveChars = "...";
				i+= replacements5[fiveChars].length() - 5;
			}
			else if (replacements4.find(fourChars) != replacements4.end()){
				input_str.replace(i-3,4,replacements4[fourChars]);
				fourChars = "...";
				i+= replacements4[fourChars].length() - 4;
			}
			else if (replacements3.find(threeChars) != replacements3.end()){
				input_str.replace(i-2,3,replacements3[threeChars]);
				threeChars = "...";
				i+= replacements3[threeChars].length() - 3;
			}
			else if (replacements2.find(twoChars) != replacements2.end()){
				input_str.replace(i-1,2,replacements2[twoChars]);
				twoChars = "..";
				i+= replacements2[twoChars].length() - 2;
			}
		

			else if (query3.find(threeChars) != query3.end()){
				if (query3[threeChars].at(0) == ddx){ //is a derivative with respect to something
					//std::cout << i << " : " << input_str << " 3chars: " << threeChars << '\n';
					std::string inside = "";
					std::string var = "";
					int openPar = 0;
					bool isVar = false;
					int repLen = 3;
					for (ii=i+1;ii<input_str.length();ii++){
						repLen++;
						if (input_str.at(ii) == '('){
							openPar++;
						}
						else if (input_str.at(ii) == ')'){
							openPar--;
						}
						else if (input_str.at(ii) == ';'){
							isVar = true;
						}
						else if (isVar){
							var += input_str.at(ii);
						}
						else {
							inside += input_str.at(ii);
						}
				
						if (openPar == 0){
							break;
						}
					}
					input_str.replace(i-2,repLen,"("+var+")"+ddx+"("+inside+")");
					threeChars = "...";
					i += -3;
					//std::cout << i << " : " << input_str << " 3chars: " << threeChars << '\n';
				}
				else if (query3[threeChars].at(0) == idx){ //is a derivative with respect to something
					//std::cout << i << " : " << input_str << " 3chars: " << threeChars << '\n';
					std::string inside = "";
					std::string var = "";
					int openPar = 0;
					bool isVar = false;
					int repLen = 3;
					for (ii=i+1;ii<input_str.length();ii++){
						repLen++;
						if (input_str.at(ii) == '('){
							openPar++;
						}
						else if (input_str.at(ii) == ')'){
							openPar--;
						}
						else if (input_str.at(ii) == ';'){
							isVar = true;
						}
						else if (isVar){
							var += input_str.at(ii);
						}
						else {
							inside += input_str.at(ii);
						}
				
						if (openPar == 0){
							break;
						}
					}
					input_str.replace(i-2,repLen,"("+var+")"+idx+"("+inside+")");
					threeChars = "...";
					i += -3;
					//std::cout << i << " : " << input_str << " 3chars: " << threeChars << '\n';
				}
			
			}
			//std::cout << i << " : " << input_str << " 3chars: " << threeChars << '\n';
		}
		else if (query4.find(fourChars) != query4.end() && input_str.length() > i+2 && input_str.at(i+1)!='-' && input_str.at(i+2)!='-'){
			
			if (input_str.at(i)=='^'){ //is trig function to a power--unless add more
				std::cout << i << " : " << input_str << " 4chars: " << fourChars << '\n';
				std::string inside = "";
				std::string var = "";
				int openPar = 0;
				bool isVar = true;
				int repLen = 4;
				for (ii=i+1;ii<input_str.length();ii++){
					repLen++;
					if (input_str.at(ii) == '('){
						openPar++;
						isVar = false;
					}
					else if (input_str.at(ii) == ')'){
						openPar--;
					}
					else if (isVar){
						var += input_str.at(ii);
					}
					else {
						inside += input_str.at(ii);
					}
			
					if (openPar == 0 && !isVar){
						break;
					}
				}
				input_str.replace(i-3,repLen,"("+query4[fourChars]+"("+inside+"))^("+var+")");
				fourChars = "....";
				i += -4;
				std::cout << i << " : " << input_str << " char: " << query4[fourChars] << '\n';
			}
			
		
		}
		else if (query3.find(threeChars) != query3.end()){
			if (query3[threeChars].at(0) == log){
				if (input_str.at(i+1)=='^'){
					std::string inside = "";
					std::string var = "";
					int openPar = 0;
					bool isVar = true;
					int repLen = 4;
					for (ii=i+2;ii<input_str.length();ii++){
						repLen++;
						if (input_str.at(ii) == '('){
							openPar++;
							isVar = false;
						}
						else if (input_str.at(ii) == ')'){
							openPar--;
						}
						else if (isVar){
							var += input_str.at(ii);
						}
						else {
							inside += input_str.at(ii);
						}
			
						if (openPar == 0 && !isVar){
							break;
						}
					}
					input_str.replace(i-2,repLen,"(e"+query3[threeChars]+"("+inside+"))^("+var+")");
					fourChars = "....";
					i += -3;
					std::cout << i << " : " << input_str << " char: " << query3[threeChars] << '\n';
				}
				else if (input_str.at(i+1)=='_'){
					std::string inside = "";
					std::string var = "";
					int openPar = 0;
					bool isVar = true;
					int repLen = 4;
					for (ii=i+2;ii<input_str.length();ii++){
						repLen++;
						if (input_str.at(ii) == '('){
							openPar++;
							isVar = false;
						}
						else if (input_str.at(ii) == ')'){
							openPar--;
						}
						else if (isVar){
							var += input_str.at(ii);
						}
						else {
							inside += input_str.at(ii);
						}
			
						if (openPar == 0 && !isVar){
							break;
						}
					}
					input_str.replace(i-2,repLen,var+query3[threeChars]+"("+inside+")");
					threeChars = "...";
					i += -3;
					std::cout << i << " : " << input_str << " char: " << query3[threeChars] << '\n';
				}
				else if (input_str.length()>i+3 && input_str.at(i+1) == 'l' && input_str.at(i+2) == 'o' && input_str.at(i+3) == 'g'){
					std::string inside = "";
					std::string var = "";
					int openPar = 0;
					bool isVar = false;
					bool isInside = false;
					int repLen = 3;
					std::cout << i << " : " << input_str << " char: " << query3[threeChars] << '\n';
					for (ii=i+1;ii<input_str.length();ii++){
						repLen++;
						inside += input_str.at(ii);
						if (input_str.at(ii) == '('){
							openPar++;
							isInside = true;
							isVar = false;
						}
						else if (input_str.at(ii) == ')'){
							openPar--;
						}
						else if (input_str.at(ii) == '_'){
							isVar = true;
						}
						else if (isVar){
							var += input_str.at(ii);
						}
						
			
						if (openPar == 0 && isInside){
							break;
						}
					}
					std::cout << var << " : " << inside << " char: " << query3[threeChars] << '\n';
					if (var == ""){var = "e";}
					input_str.replace(i-2,repLen,var+log+"("+inside+")");
					threeChars = "...";
					i += -3;
					std::cout << i << " : " << input_str << " char: " << query3[threeChars] << '\n';
				}
				else {
					std::string inside = "";
					std::string var = "";
					int openPar = 0;
					bool isVar = true;
					int repLen = 3;
					for (ii=i+1;ii<input_str.length();ii++){
						repLen++;
						if (input_str.at(ii) == '('){
							openPar++;
							isVar = false;
						}
						else if (input_str.at(ii) == ')'){
							openPar--;
						}
						else if (isVar){
							var += input_str.at(ii);
						}
						else {
							inside += input_str.at(ii);
						}
			
						if (openPar == 0 && !isVar){
							break;
						}
					}
					input_str.replace(i-2,repLen,var+query3[threeChars]+"("+inside+")");
					threeChars = "...";
					i += -3;
					std::cout << i << " : " << input_str << " char: " << query3[threeChars] << '\n';
				}
			}
		}
		else if (query2.find(twoChars) != query2.end()){
			if (query2[twoChars].at(0) == log){
				if (input_str.at(i+1)=='^'){
					std::string inside = "";
					std::string var = "";
					int openPar = 0;
					bool isVar = true;
					int repLen = 3;
					for (ii=i+2;ii<input_str.length();ii++){
						repLen++;
						if (input_str.at(ii) == '('){
							openPar++;
							isVar = false;
						}
						else if (input_str.at(ii) == ')'){
							openPar--;
						}
						else if (isVar){
							var += input_str.at(ii);
						}
						else {
							inside += input_str.at(ii);
						}
			
						if (openPar == 0 && !isVar){
							break;
						}
					}
					input_str.replace(i-1,repLen,"(e"+query2[twoChars]+"("+inside+"))^("+var+")");
					twoChars = "..";
					i += -2;
					std::cout << i << " : " << input_str << " char: " << query2[twoChars] << '\n';
				}
				else if (input_str.length()>i+2 && input_str.at(i+1) == 'l' && input_str.at(i+2) == 'n'){
					std::string inside = "";
					std::string var = "";
					int openPar = 0;
					bool isVar = false;
					bool isInside = false;
					int repLen = 2;
					for (ii=i+1;ii<input_str.length();ii++){
						repLen++;
						inside += input_str.at(ii);
						if (input_str.at(ii) == '('){
							openPar++;
							isInside = true;
							isVar = false;
						}
						else if (input_str.at(ii) == ')'){
							openPar--;
						}
						else if (input_str.at(ii) == '_'){
							isVar = true;
						}
						
			
						if (openPar == 0 && isInside){
							break;
						}
					}
					input_str.replace(i-1,repLen,"e" + query2[twoChars] +"("+inside+")");
					twoChars = "..";
					i += -2;
					std::cout << i << " : " << input_str << " char: " << query2[twoChars] << '\n';
				}
			}
			
		}
	}
	return input_str;
}

std::vector<std::string> postfixifyVector(std::string input_str){

	input_str = replaceFunctions(input_str);
	
	char infixexpr[input_str.length() + 1]; 
    strcpy(infixexpr, input_str.c_str()); 

	infixexpr[input_str.length()] = '\0';
	std::cout << makePost(infixexpr) << '\n';
	

	return makePostVector(infixexpr);
}

std::string postfixify(std::string input_str) {
	/*input_str = input_str.toUpperCase();
	input_str = input_str.replace(/AND/g,'&');
	input_str = input_str.replace(/OR/g,'|');
	input_str = input_str.replace(/\[/g,'(');
	input_str = input_str.replace(/]/g,')');
	input_str = input_str.replace(/{/g,'(');
	input_str = input_str.replace(/}/g,')');
	input_str = input_str.replace(/>=/g,']');
	input_str = input_str.replace(/<=/g,'[');
	input_str = input_str.replace(/==/g,'=');
	input_str = input_str.replace(/!=/g,'!');
	input_str = input_str.replace(/\+-/g,'-');
	input_str = input_str.replace(/--/g,'+');*/
	
	input_str = replaceFunctions(input_str);
	
	char infixexpr[input_str.length() + 1]; 
    strcpy(infixexpr, input_str.c_str()); 

	infixexpr[input_str.length()] = '\0';
	std::cout << makePost(infixexpr) << '\n';
	

	return makePost(infixexpr);
}