from any_worksheet import *

class WorksheetForm0(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter answer here.','size':'30','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))

class WorksheetForm1(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': '1,4,...,10','size':'20','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))

class WorksheetForm2(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': '','size':'5','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))

class WorksheetForm3(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': '','size':'5','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))

def increasing_decreasing_worksheet(request):

	rcarr = [{'href':'product_rule_lesson.html','title':'Product Rule Lesson'},{'href':'quotient_rule_worksheet.html','title':'Quotient Rule Worksheet'},{'href':'chain_rule_worksheet.html','title':'Chain Rule Worksheet'},{'href':'#','title':'Product Rule Video'},{'href':'#','title':'Product Rule Explained'}]
	meta_title = 'Product Rule Worksheet - Learn the Product Rule by working examples with Calculus College.'
	meta_des = "Infinitely many product rule problems with step-by-step solutions if you make a mistake. Progress through several types of problems that help you improve."
	frac_q = '.5'
	form0 = WorksheetForm0()
	form1 = WorksheetForm1()
	form2 = WorksheetForm2()
	form3 = WorksheetForm3()
	subsection ={'classinit':'hold_for_class','id':'One','title':'Increasing','function':'x^2+2','function_python':'x^2+2','answer1':'2x','form0':form0,'form1':form1,'form2':form2,'form3':form3}
	return render(request,'complex_worksheet.html',{'related_content':rcarr,'title':meta_title,'meta_des':meta_des,'header_1':'Product Rule Worksheet','fraction_questions':frac_q,'subsection':subsection})

