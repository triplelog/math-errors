#include <stdio.h>
#include <string>
#include <iostream>
#include <algorithm>

using namespace std;

struct MathExpression
{
	char operation;
	int location;
};
struct TermDouble
{
	double dvalue;
	int ivalue;
	string type;
};

int fullparen(string inputexp) {
	int numparen = 0;
	int i;
	for (i=0; i<inputexp.length(); i++ ) {
	   	if (inputexp[i]=='(') {
	   		numparen++;
	   	}
	   	else if (inputexp[i]==')') {
	   		numparen--;
	   	}
	}

	return numparen;
}

struct MathExpression BreakUp(string inputexp, char ChkOperation) {
	int i;
	for (i=1; i<inputexp.length(); i++ ) {
		if (inputexp[i]==ChkOperation){
			string dest;
			dest = inputexp.substr(0,i);
			if 	(fullparen(dest)==0) {
				struct MathExpression ToReturn;
				ToReturn.operation = ChkOperation;
				ToReturn.location = i;
				return ToReturn;
			}
		}
	}
	struct MathExpression FailedReturn;
	char failedvar;
	failedvar='f';
	FailedReturn.operation = failedvar;
	FailedReturn.location = -1;
	return FailedReturn;
}

struct MathExpression ChkOrigin(struct MathExpression origin0, struct MathExpression origin1){
	struct MathExpression origin;
	if (origin0.location==-1){
		if (origin1.location==-1){
			origin = origin1;

		}
		else {
			origin = origin1;
		}
	}
	else {
		if (origin1.location==-1){
			origin = origin0;
			
		}
		else {
			if (origin1.location < origin0.location) {
				origin = origin1;
			}
			else {
				origin = origin0;
			}
		}
	}
	return origin;
}
struct Equation
{
	string LHS;
	string RHS; 
	int haseq;
};
struct Equation GetLR(string source){
	int i;
	int breakeq = -1;
	for (i=0;i<source.length();i++){
		if (source[i]=='='){
			breakeq = i;
		}
	}
	struct Equation equation;
	equation.haseq = 0;
	if (breakeq!=-1){
		equation.LHS=source.substr(0,breakeq);
		equation.RHS=source.substr(breakeq+1,source.length()-breakeq-1);
		equation.haseq=1;
	}
	else{
		equation.LHS = source.substr(0,0);
		equation.RHS = source.substr(0,0);
		equation.haseq=1;
	}

	return equation;
}

struct MathExpression DivideUp(string source0,int StartPoint) {
	string source;
	int i;
	int stl = source0.length();
	source=source0.substr(StartPoint,stl+1-StartPoint);

	struct MathExpression origin0 = BreakUp(source,'+');
	struct MathExpression origin1 = BreakUp(source,'-');
	struct MathExpression origin = ChkOrigin(origin0,origin1);
	if (origin.location ==-1){
		struct MathExpression origin0 = BreakUp(source,'*');
		struct MathExpression origin1 = BreakUp(source,'/');
		origin = ChkOrigin(origin0,origin1);
	}
	if (origin.location ==-1){
		origin = BreakUp(source,'^');
	}
	return origin;
}

string RemovePar(string source){
	int i;
	int breakeq = -1;
	int slength = source.length();
	string source0 = source;
	source = " ";
	while (source != source0){
		source = source0;
		slength = source.length();
		for (i=0;i<slength-1;i++){
			if (source[i]=='('){
				if (source[i+1]=='('){
					int ii;
					for (ii=i+1;ii<slength-1;ii++){
						if (fullparen(source.substr(i+1,ii-i))==0){
							if (source[ii+1]==')'){
								source0=source.substr(0,i)+source.substr(i+1,ii-i)+source.substr(ii+2,source.length()-ii-2);
							}
							break;
						}
					}
				}
				else{
					int ii;
					for (ii=i;ii<slength;ii++){
						if (fullparen(source.substr(i,ii-i+1))==0){
							if (i>0){
								if (source[i-1]=='+' || source[i-1]=='('){
									source0=source.substr(0,i)+source.substr(i+1,ii-i-1)+source.substr(ii+1,source.length()-ii-1);
								}
								break;
							}
							else{
								source0=source.substr(1,ii-1)+source.substr(ii+1,source.length()-ii-1);
								break;
							}
						}
					}
				}
			}
		}
	}

	return source0;
}
struct TermDouble ChkDouble(string source){
	std::string::size_type sz;
	try{
		double nTerm = std::stod (source,&sz);
		if (sz==source.length()){
			struct TermDouble ToReturn;
			if (nTerm==floorf(nTerm)){
				ToReturn.ivalue = nTerm;
				ToReturn.type = "int";
			}
			else{
				ToReturn.dvalue = nTerm;
				ToReturn.type = "double";
			}
			return ToReturn;
		}
	}
	catch(std::exception& e){
	}
	struct TermDouble ToReturn;
	ToReturn.dvalue = 0;
	ToReturn.type = "Not";
	return ToReturn;
}
string RemoveExtra(string source){
	int i;
	int strlength = source.length();
	for (i=0;i<strlength-1;i++){
		if (source.substr(i,2)=="+-"){
			source = source.substr(0,i)+source.substr(i+1);
			break;
		}
	}
	return source;
}
string CombineFloats(string source){
	struct MathExpression origin;
	origin.location = 0;
	int SPoint = 0;
	string NewSource;
	while (origin.location != -1){
		origin = DivideUp(source,SPoint);
		if (origin.operation=='+' || origin.operation=='-'){
			struct TermDouble ChkTerm;
			struct TermDouble ChkNTerm;
			ChkTerm = ChkDouble(source.substr(SPoint,origin.location));
			struct MathExpression originn;
			originn = DivideUp(source,SPoint+origin.location+1);
			if (originn.operation=='+' || originn.operation=='-'){
				ChkNTerm = ChkDouble(source.substr(SPoint+origin.location+1,originn.location));
			}
			else{
				ChkNTerm = ChkDouble(source.substr(SPoint+origin.location+1));
			}

			if (ChkTerm.type=="int"){
				if (ChkNTerm.type=="int"){
					int cvalue = ChkTerm.ivalue;
					int nvalue = ChkNTerm.ivalue;
					if (SPoint>0){
						if (source.substr(SPoint-1,1)=="-"){
							if (source.substr(SPoint+origin.location,1)=="-"){
								if (originn.location != -1){
									NewSource = source.substr(0,SPoint-1)+source.substr(SPoint+origin.location+1+originn.location)+"+"+to_string(-1*cvalue-nvalue);
									return NewSource;
								}
								else{
									NewSource = source.substr(0,SPoint-1)+"+"+to_string(-1*cvalue-nvalue);
									return NewSource;
								}
							}
							else{
								if (originn.location != -1){
									NewSource = source.substr(0,SPoint-1)+source.substr(SPoint+origin.location+1+originn.location)+"+"+to_string(-1*cvalue+nvalue);
									return NewSource;
								}
								else{
									NewSource = source.substr(0,SPoint-1)+"+"+to_string(-1*cvalue+nvalue);
									return NewSource;
								}

							}
						}
						else{
							if (source.substr(SPoint+origin.location,1)=="-"){
								if (originn.location != -1){
									NewSource = source.substr(0,SPoint-1)+source.substr(SPoint+origin.location+1+originn.location)+"+"+to_string(cvalue-nvalue);
									return NewSource;
								}
								else{
									NewSource = source.substr(0,SPoint-1)+"+"+to_string(cvalue-nvalue);
									return NewSource;
								}
							}
							else{
								if (originn.location != -1){
									NewSource = source.substr(0,SPoint-1)+source.substr(SPoint+origin.location+1+originn.location)+"+"+to_string(cvalue+nvalue);
									return NewSource;
								}
								else{
									NewSource = source.substr(0,SPoint-1)+"+"+to_string(cvalue+nvalue);
									return NewSource;
								}

							}
						}
					}
					else{
						if (source.substr(0,1)=="-"){
							if (origin.operation=='-'){
								NewSource = source.substr(origin.location)+source.substr(0,origin.location);
								return NewSource;
							}
							else{
								NewSource = source.substr(origin.location+1)+source.substr(0,origin.location);
								return NewSource;
							}
						}
						else{
							if (origin.operation=='-'){
								NewSource = source.substr(origin.location)+"+"+source.substr(0,origin.location);
								return NewSource;
							}
							else{
								NewSource = source.substr(origin.location+1)+"+"+source.substr(0,origin.location);
								return NewSource;
							}
						}
					}
				}
				else{
					if (SPoint>0){
						if (source.substr(SPoint-1,1)=="-"){
							NewSource = source.substr(0,SPoint-1)+source.substr(SPoint+origin.location)+"-"+source.substr(SPoint,origin.location);
							return NewSource;
						}
						else{
							NewSource = source.substr(0,SPoint-1)+source.substr(SPoint+origin.location)+"+"+source.substr(SPoint,origin.location);
							return NewSource;
						}
					}
					else{
						if (source.substr(0,1)=="-"){
							if (origin.operation=='-'){
								NewSource = source.substr(origin.location)+source.substr(0,origin.location);
								return NewSource;
							}
							else{
								NewSource = source.substr(origin.location+1)+source.substr(0,origin.location);
								return NewSource;
							}
						}
						else{
							if (origin.operation=='-'){
								NewSource = source.substr(origin.location)+"+"+source.substr(0,origin.location);
								return NewSource;
							}
							else{
								NewSource = source.substr(origin.location+1)+"+"+source.substr(0,origin.location);
								return NewSource;
							}
						}
					}
				}
				
			}
		}
		else{
			struct TermDouble ChkTerm;
			ChkTerm = ChkDouble(source.substr(SPoint));
			if (ChkTerm.type=="int"){
				if (SPoint>0){
					if (source.substr(SPoint-1,1)=="-"){
						cout << -1*ChkTerm.ivalue;
					}
					else{
						cout << ChkTerm.ivalue;
					}
				}
				else{
					cout << ChkTerm.ivalue;
				}
				
			}
			break;
		}
		SPoint=SPoint+origin.location+1;
	}

	return source;
}
int main(void) {

	string source;
	cout << "Enter Equation: ";
	char variable;
	variable='x';
	cin >> source;
	source = RemovePar(source);
	cout << source;
	cout << "HH";
	source = CombineFloats(source);
	cout << source;
	cout << "AA";
	source = RemoveExtra(source);
	cout << source;

	return 0;
}
