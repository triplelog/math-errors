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

struct Equation MoveLtoR(struct Equation equation, struct MathExpression originL,char variable,int StartPoint, char ChkOperation,char InvOperation){
	string FirstTerm;
	string OtherTerm;
	if (originL.operation==ChkOperation || originL.operation==InvOperation){
		FirstTerm = equation.LHS.substr(StartPoint,originL.location);
		OtherTerm = equation.LHS.substr(StartPoint+originL.location+1,equation.LHS.length()-originL.location-1-StartPoint);
		int i;
		int BreakVar = -1;
		int slft = FirstTerm.length();
		for (i=0;i<slft;i++){
			if (FirstTerm[i]==variable){
				BreakVar = i;
			}
		}
		string StrOper;
		StrOper = InvOperation;
		string COper;
		COper = ChkOperation;
		if (BreakVar==-1){
			if (StartPoint > 0){
				if (equation.LHS.substr(StartPoint-1,1)==StrOper){
					equation.RHS="("+equation.RHS+")"+COper+"("+FirstTerm+")";
				}
				else {
					if (ChkOperation=='^'){
						if (OtherTerm.find(variable)!=-1){
							equation.RHS="ln("+equation.RHS+")";
							equation.LHS = "("+OtherTerm+")*ln("+equation.LHS.substr(0,StartPoint-1)+"^"+FirstTerm+")";
						}
					}
					else{
						equation.RHS="("+equation.RHS+")"+StrOper+"("+FirstTerm+")";	
					}
				}
				if (ChkOperation !='^'){
					if (originL.operation==ChkOperation){
						equation.LHS = equation.LHS.substr(0,StartPoint-1)+COper+OtherTerm;
					}
					else {
						equation.LHS = equation.LHS.substr(0,StartPoint-1)+StrOper+OtherTerm;	
					}
				}
			}
			else{

				if (equation.LHS.substr(0,1)==StrOper){
					equation.RHS="("+equation.RHS+")"+COper+"("+FirstTerm.substr(1,FirstTerm.length()-1)+")";
				}
				else {
					if (ChkOperation=='^'){
						if (OtherTerm.find(variable)!=-1){
							equation.RHS="ln("+equation.RHS+")";
							equation.LHS = "("+OtherTerm+")*ln("+FirstTerm+")";
						}
					}
					else{
						equation.RHS="("+equation.RHS+")"+StrOper+"("+FirstTerm+")";
					}	
				}
				if (originL.operation==ChkOperation){
					if (ChkOperation !='^'){
						equation.LHS = OtherTerm;
					}
				}
				else {
					if (InvOperation=='-'){
						equation.LHS = StrOper+OtherTerm;	
					}
					else if (InvOperation=='/'){
						equation.LHS = "1"+StrOper+OtherTerm;	
					}
				}
			}

		}
		else {
			if (ChkOperation=='^'){
				cout << equation.LHS;
				cout << "HH";
				cout << equation.RHS;
				cout << "KK";
				cout << FirstTerm;
				cout << "JJ";
				cout << OtherTerm;
				cout << "II";
				equation.LHS=FirstTerm;
				equation.RHS="("+equation.RHS+")^(1/("+OtherTerm+"))";
			}
			else {
				if (BreakUp(OtherTerm,ChkOperation).location==-1 && BreakUp(OtherTerm,InvOperation).location==-1){
					int i;
					int BreakVar = -1;
					int slft = OtherTerm.length();
					for (i=0;i<slft;i++){
						if (OtherTerm[i]==variable){
							BreakVar = i;
						}
					}
					if (BreakVar==-1){
						if (StartPoint > 0){
							equation.LHS = equation.LHS.substr(0,StartPoint)+FirstTerm;
							if (equation.LHS.substr(originL.location+StartPoint,1)==StrOper){
								equation.RHS="("+equation.RHS+")"+COper+"("+OtherTerm+")";
							}
							else {
								equation.RHS="("+equation.RHS+")"+StrOper+"("+OtherTerm+")";	
							}
						}
						else{

							equation.LHS=FirstTerm;
							if (equation.LHS.substr(originL.location+StartPoint,1)==StrOper){
								equation.RHS="("+equation.RHS+")"+COper+"("+OtherTerm+")";
							}
							else {
								equation.RHS="("+equation.RHS+")"+StrOper+"("+OtherTerm+")";	
							}
							
						}
					}
					else{
						
					}
				}
				else{
					int SPoint=StartPoint+FirstTerm.length()+1;
					struct MathExpression originLp = BreakUp(equation.LHS.substr(SPoint,equation.LHS.length()-SPoint),ChkOperation);
					struct MathExpression originLm = BreakUp(equation.LHS.substr(SPoint,equation.LHS.length()-SPoint),InvOperation);
					if (originLp.location!=-1){
						if (originLm.location!=-1){
							if (originLp.location<originLm.location){
								originL=originLp;
							}
							else{
								originL=originLm;
							}
						}
						else{
							originL=originLp;
						}
					}
					else{
						originL=originLm;
					}
					equation = MoveLtoR(equation, originL,variable,SPoint,ChkOperation,InvOperation);
				}
			}

		}
	}
	else if (DivideUp(equation.LHS,0).location==-1){
		int i;
		int BreakVar = -1;
		int slft = equation.LHS.length();
		for (i=0;i<slft;i++){
			if (equation.LHS[i]==variable){
				BreakVar = i;
			}
		}
		if (BreakVar==-1){
			if (equation.LHS!="0"){
				equation.LHS = "0";
				equation.RHS = "("+equation.RHS+")-("+equation.LHS+")";
			}
		}
	}
	return equation;
}

struct Equation MoveRtoL(struct Equation equation, struct MathExpression originL,char variable,int StartPoint, char ChkOperation,char InvOperation){
	string FirstTerm;
	string OtherTerm;
	if (originL.operation==ChkOperation || originL.operation==InvOperation){
		FirstTerm = equation.RHS.substr(StartPoint,originL.location);
		OtherTerm = equation.RHS.substr(StartPoint+originL.location+1,equation.RHS.length()-originL.location-1-StartPoint);
		int i;
		int BreakVar = -1;
		int slft = FirstTerm.length();
		for (i=0;i<slft;i++){
			if (FirstTerm[i]==variable){
				BreakVar = i;
			}
		}
		string StrOper;
		StrOper = InvOperation;
		string COper;
		COper = ChkOperation;
		if (BreakVar!=-1){
			if (StartPoint > 0){
				if (equation.RHS.substr(StartPoint-1,1)==StrOper){
					equation.LHS="("+equation.LHS+")"+COper+"("+FirstTerm+")";
				}
				else {
					equation.LHS="("+equation.LHS+")"+StrOper+"("+FirstTerm+")";	
				}
			}
			else{

				if (equation.RHS.substr(0,1)==StrOper){
					equation.LHS="("+equation.LHS+")"+COper+"("+FirstTerm.substr(1,FirstTerm.length()-1)+")";
				}
				else {
					equation.LHS="("+equation.LHS+")"+StrOper+"("+FirstTerm+")";	
				}
			}
			if (StartPoint>0){
				if (originL.operation==ChkOperation){
					equation.RHS = equation.RHS.substr(0,StartPoint-1)+COper+OtherTerm;
				}
				else {
					equation.RHS = equation.RHS.substr(0,StartPoint-1)+StrOper+OtherTerm;	
				}
			}
			else{
				if (originL.operation==ChkOperation){
					equation.RHS = OtherTerm;
				}
				else {
					if (InvOperation=='-'){
						equation.RHS = StrOper+OtherTerm;	
					}
					else if (InvOperation=='/'){
						equation.RHS = "1"+StrOper+OtherTerm;	
					}
				}
					
			}
		}
		else {
			if (BreakUp(OtherTerm,ChkOperation).location==-1 && BreakUp(OtherTerm,InvOperation).location==-1){
				int i;
				int BreakVar = -1;
				int slft = OtherTerm.length();
				for (i=0;i<slft;i++){
					if (OtherTerm[i]==variable){
						BreakVar = i;
					}
				}
				if (BreakVar!=-1){
					if (StartPoint > 0){
						if (equation.RHS.substr(originL.location+StartPoint,1)==StrOper){
							equation.LHS="("+equation.LHS+")"+COper+"("+OtherTerm+")";
						}
						else {
							equation.LHS="("+equation.LHS+")"+StrOper+"("+OtherTerm+")";	
						}
					}
					else{
						if (equation.RHS.substr(originL.location+StartPoint,1)==StrOper){
							equation.LHS="("+equation.LHS+")"+COper+"("+OtherTerm+")";
						}
						else {
							equation.LHS="("+equation.LHS+")"+StrOper+"("+OtherTerm+")";	
						}
					}
					if (StartPoint>0){
						equation.RHS = equation.RHS.substr(0,StartPoint)+FirstTerm;
					}
					else{
						equation.RHS = FirstTerm;	
					}
				}
				else{
					
				}
			}
			else{
				int SPoint=StartPoint+FirstTerm.length()+1;
				struct MathExpression originLp = BreakUp(equation.RHS.substr(SPoint,equation.RHS.length()-SPoint),ChkOperation);
				struct MathExpression originLm = BreakUp(equation.RHS.substr(SPoint,equation.RHS.length()-SPoint),InvOperation);
				if (originLp.location!=-1){
					if (originLm.location!=-1){
						if (originLp.location<originLm.location){
							originL=originLp;
						}
						else{
							originL=originLm;
						}
					}
					else{
						originL=originLp;
					}
				}
				else{
					originL=originLm;
				}
				equation = MoveRtoL(equation, originL,variable,SPoint,ChkOperation,InvOperation);
			}

		}
	}
	else if (DivideUp(equation.RHS,0).location==-1){
		int i;
		int BreakVar = -1;
		int slft = equation.RHS.length();
		for (i=0;i<slft;i++){
			if (equation.RHS[i]==variable){
				BreakVar = i;
			}
		}
		if (BreakVar!=-1){
			equation.RHS = "0";
			equation.LHS = "("+equation.LHS+")-("+equation.RHS+")";
		}
	}
	return equation;
}

int main(void) {

	string source;
	cout << "Enter Equation: ";
	char variable;
	variable='x';
	cin >> source;
	struct Equation equation = GetLR(source);
	
	struct MathExpression originL;
	struct MathExpression originR;
	if (equation.haseq==1){
		struct Equation oldequation = equation;
		struct Equation newequation;
		newequation.RHS="FAKE";
		newequation.LHS="FAKE";
		while (oldequation.LHS != newequation.LHS || oldequation.RHS!= newequation.RHS) {
			oldequation=equation;
			originL = DivideUp(equation.LHS,0);
			equation = MoveLtoR(equation, originL,variable,0,'+','-');
			newequation=equation;
			if (oldequation.LHS == newequation.LHS && oldequation.RHS== newequation.RHS) {
				oldequation=equation;
				originL = DivideUp(equation.LHS,0);
				equation = MoveLtoR(equation, originL,variable,0,'*','/');
				newequation=equation;
			}
			if (oldequation.LHS == newequation.LHS && oldequation.RHS== newequation.RHS) {
				oldequation=equation;
				originL = DivideUp(equation.LHS,0);
				equation = MoveLtoR(equation, originL,variable,0,'^','p');
				newequation=equation;
			}
		}

		oldequation = equation;
		newequation.RHS="FAKE";
		newequation.LHS="FAKE";
		while (oldequation.LHS != newequation.LHS || oldequation.RHS!= newequation.RHS) {
			oldequation=equation;
			originR = DivideUp(equation.RHS,0);
			equation = MoveRtoL(equation, originR,variable,0,'+','-');
			newequation=equation;
			if (oldequation.LHS == newequation.LHS && oldequation.RHS== newequation.RHS) {
				oldequation=equation;
				originR = DivideUp(equation.RHS,0);
				equation = MoveRtoL(equation, originR,variable,0,'*','/');
				newequation=equation;
			}
			if (oldequation.LHS == newequation.LHS && oldequation.RHS== newequation.RHS) {
				oldequation=equation;
				originR = DivideUp(equation.RHS,0);
				equation = MoveRtoL(equation, originR,variable,0,'^','p');
				newequation=equation;
			}
		}


	}


	


	cout << equation.LHS;
	cout << "\n";
	cout << equation.RHS;
	cout << "\n";
	return 0;
}
