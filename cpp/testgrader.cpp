void CheckAnswer(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string a(*s);

	std::string mpf = postfixify(a);
	std::cout << "your answer: " << mpf << "\n";
	int ii; int iii; int iiii;
	
	auto a1 = std::chrono::high_resolution_clock::now();
	int ai;
	int k = 500;
	for (ai=0;ai<1000;ai++){
		if (ai%5 > 1){
			mpf = postfixify("7*x^6+5+2*x");
		}
		else {
			mpf = postfixify("7*x^6+5*x+2*x");
		}
		if (answerMap.find(mpf) != answerMap.end()){
			k = 1000 - ai*4;
			if (k < 100){
				k = 100;
			}
			Answer userAnswer = answerMap[mpf];
			//std::cout << "correct? " << userAnswer.correct <<"\n";
			//std::cout << "finished? " << userAnswer.finished <<"\n";
		
		
	
			flat_hash_map<int,std::vector<int>> branches;
			flat_hash_map<int,std::vector<bool>> userData;
			for (ii=0;ii<ridx;ii++){
				userData[ii]={false,false};
			}
			std::vector<Step> v;
			if (userAnswer.correct){
				v = correctSolutionList[mpf];
			}
			else {
				v = incorrectSolutionList[mpf];
			}
			flat_hash_map<int,bool> alreadyApp;
			flat_hash_map<int,bool> alreadyOpp;
			for (iii=0;iii<v.size();iii++){
				if (alreadyApp.find(v[iii].rule) != alreadyApp.end()){
				}
				else {
					//TODO: make the rule match reality
					if (v[iii].rule >= 0){
						userData[v[iii].rule][0]=true;
					}
					alreadyApp[v[iii].rule]=true;
				}
				std::vector<int> allOptions = answerListMapF[v[iii].next];
				for (iiii=0;iiii<allOptions.size();iiii++){
					if (alreadyOpp.find(allOptions[iiii]) != alreadyOpp.end()){
						continue;
					}
					else {
						userData[allOptions[iiii]][1]=true;
						alreadyOpp[allOptions[iiii]]=true;
					}
				}
			}
		
			int apc = probCorrect();
		
			for (ii=0;ii<ridx;ii++){
				if (userData[ii][1]){
					branches[ii]={0,0};
				}
			}
	
			for (ii=0;ii<correctAnswers.size()+finishedErrors.size();ii++){
				std::vector<Step> v;
				if (ii<correctAnswers.size()){
					v = correctSolutionList[correctAnswers[ii]];
				}
				else {
					v = incorrectSolutionList[finishedErrors[ii-correctAnswers.size()]];
				}
			
				flat_hash_map<int,bool> alreadyApp;
				flat_hash_map<int,bool> alreadyOpp;
				for (iii=0;iii<v.size();iii++){
					if (branches.find(v[iii].rule) != branches.end()){
						if (alreadyApp.find(v[iii].rule) != alreadyApp.end()){
						}
						else {
							//TODO: make the rule match reality
							if (v[iii].rule >= 0){
								branches[v[iii].rule][0]++;
							}
							alreadyApp[v[iii].rule]=true;
						}
					}
					std::vector<int> allOptions = answerListMapF[v[iii].next];
					for (iiii=0;iiii<allOptions.size();iiii++){
						if (branches.find(allOptions[iiii]) != branches.end()){
							if (alreadyOpp.find(allOptions[iiii]) != alreadyOpp.end()){
								continue;
							}
							else {
								branches[allOptions[iiii]][1]++;
								alreadyOpp[allOptions[iiii]]=true;
							}
						}
					}
				}
			}
		
			for (flat_hash_map<int,std::vector<int>>::iterator iter = branches.begin(); iter != branches.end(); ++iter){
				int rr = (branches[iter->first][0]*2 + 1)*100/(branches[iter->first][1]*2+2);

				if (rr < 1){
					rr = 1;
				}
				if (rr > 99){
					rr = 99;
				}
				int r = eloMap[rr];
				//std::cout << iter->first << " and " << branches[iter->first][0] << " and "<< branches[iter->first][1] << " and " << r << "\n";
				//std::cout << iter->first << " and " << userData[iter->first][0] << " and "<< userData[iter->first][1] << "\n";
				int score = ruleIndex[iter->first].score;
				int d = r - score;
				int ei;
				int pyes = eloToProb(d);
				int pno = eloToProb(-1*d);

				if (userData[iter->first][0]){
					ruleIndex[iter->first].score = score + k*pno/100;
				}
				else{
					ruleIndex[iter->first].score = score - k*pyes/100;
				}
				//std::cout << iter->first << " new score: " << ruleIndex[iter->first].score << " and pyes:" << pyes << "\n";
			}
			int ppc = probCorrect();
		
			int aelo;
			if (apc <= 100){
				aelo = eloMap[1];
			}
			else if (apc >= 9900){
				aelo = eloMap[99];
			}
			else {
				aelo = eloMap[apc/100]*(100-(apc%100))+eloMap[apc/100+1]*(apc%100);
				aelo /= 100;
			}
			int pelo;
			if (ppc <= 100){
				pelo = eloMap[1];
			}
			else if (ppc >= 9900){
				pelo = eloMap[99];
			}
			else {
				pelo = eloMap[ppc/100]*(100-(ppc%100))+eloMap[ppc/100+1]*(ppc%100);
				pelo /= 100;
			}
			overallScore += aelo - pelo;
			if (ai%19==0){
				std::cout << " apc: " << apc << " ppc: " << ppc << " ovscore: " << overallScore << "\n";
			}
			
		}
		else {
			std::cout << "unknown answer" << "\n";
		}
	}
	
	auto a2 = std::chrono::high_resolution_clock::now();
	std::cout << "grade time: " << std::chrono::duration_cast<std::chrono::microseconds>( a2 - a1 ).count() << "\n";

	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(a);

	
	info.GetReturnValue().Set(h.ToLocalChecked());
}