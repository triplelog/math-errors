from any_worksheet import *

def get_question(q_id):
	trig_fns = ['cos(x)','sin(x)','tan(x)','cot(x)','sec(x)','csc(x)']
	trig_fns_l = ['\cos{(x)}','\sin{(x)}','\\tan{(x)}','\cot{(x)}','\sec{(x)}','\csc{(x)}']
	inv_trigs = ['arccos(x)','arcsin(x)','arctan(x)','arccot(x)','arcsec(x)','arccsc(x)']
	polys = ['x^2+1','x^3+x-1','x+3','x^2-2x+3','x^5','x^4-x^2+x','2x^3','2x^2+x+1','x^3+5x^2-3x+2','2x-1']

	if q_id == 'One':
		return 'e^x','e^x'
	elif q_id == 'Two':
		q_1 = get_rand(['2','3','4','5','6','7','a','b','c','1/2'],[.1,.1,.1,.1,.1,.1,.1,.1,.1,.1])
		if q_1 == '1/2':
			return '('+q_1+')^x', '('+q_1+')^x'
		else:
			return '('+q_1+')^x', q_1+'^x'
	elif q_id == 'Three':
		q_1 = get_rand(['2','3','4','5','6','7','k','c'],[.15,.15,.1,.1,.1,.1,.2,.1])
		q_2 = get_rand(['2','3','5','e','b'],[.1,.1,.1,.6,.1])
		
		return '('+q_2+')^('+q_1+'x)', q_2+'^{'+q_1+'x}'
	elif q_id == 'Four':
		return 'ln(x)','\ln(x)'
	elif q_id == 'Five':
		q_1 = get_rand(['2','3','5','10','b'],[.25,.15,.15,.25,.2])
				
		return 'ln(x)/ln('+q_1+')', '\log_{'+q_1+'}{(x)}'
	elif q_id == 'Six':
		q_1 = get_rand(['2','3','5','k','4'],[.25,.15,.15,.25,.2])

		return 'ln(x^'+q_1+')', '\ln(x^'+q_1+')'
	elif q_id == 'Seven':
		q_d = get_rand([0,1],[.5,.5])
		if q_d==0:
			return 'e^x','e^x'
		else:
			return 'ln(x)','\ln(x)'
	elif q_id == 'Eight':
		if random.random()<.5:
			q_1 = get_rand(['2','3','4','5','6','7','a','b','c','1/2'],[.1,.1,.1,.1,.1,.1,.1,.1,.1,.1])
			if q_1 == '1/2':
				return '('+q_1+')^x', '('+q_1+')^x'
			else:
				return '('+q_1+')^x', q_1+'^x'
		else:
			q_1 = get_rand(['2','3','5','10','b'],[.25,.15,.15,.25,.2])
					
			return 'ln(x)/ln('+q_1+')', '\log_{'+q_1+'}{(x)}'

	elif q_id == 'Nine':
		if random.random()<.6:
			if random.random()<.5:
				q_1 = get_rand(['2','3','4','5','6','7','k','c'],[.15,.15,.1,.1,.1,.1,.2,.1])
				q_2 = get_rand(['2','3','5','e','b'],[.1,.1,.1,.6,.1])
				
				return '('+q_2+')^('+q_1+'x)', q_2+'^{'+q_1+'x}'
			else:

				q_1 = get_rand(['2','3','5','k','4'],[.25,.15,.15,.25,.2])

				return 'ln(x^'+q_1+')', '\ln(x^'+q_1+')'
		else:
			q_0 = get_rand(['2','3','4','5','6','7','a','b','c','1/2'],[.1,.1,.1,.1,.1,.1,.05,.05,.05,.25])
			q_2 = get_rand(['2','3','4','5','6','7','a','b','c','8'],[.15,.15,.15,.1,.1,.1,.05,.05,.05,.1])
			q_1 = '('+q_0+')^x*('+q_2+')^x'
			if q_0 == '1/2':
				q_1_l = '('+q_0+')^x\cdot '+q_2+'^x'
			else:
				q_1_l = q_0+'^x\cdot '+q_2+'^x' 
			return q_1, q_1_l

class WorksheetForm(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter answer here.','size':'30','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))

def exponentials_logarithms_worksheet(request):
	if request.method == "POST":
		form = WorksheetForm(request.POST)
		if (form.is_valid()):
			new_data = form.cleaned_data['your_name'].replace('\\','||')
			send_message = json.loads(new_data)
			my_question = send_message['yq']
			if my_question != 'LATEX':
				try:
					my_type = send_message['yt']
					new_q = get_question(my_type)
					for i in range(0,10):
						if new_q[0]==my_question:
							new_q = get_question(my_type)
						else:
							break
					return any_worksheet(form,'exponentials_logarithms',new_q,my_type)
				except:
					pass
			return any_worksheet(form,'exponentials_logarithms','noq','Zero')
		else:
			form = PrintableForm(request.POST)
			if (form.is_valid()):
				your_diff = form.cleaned_data['your_diff']
				title = 'Exponentials and Logarithms Worksheet'
				questions = []
				questions.append(get_question('One')[1])
				questions.append(get_question('Two')[1])
				questions.append(get_question('Three')[1])
				questions.append(get_question('Four')[1])
				questions.append(get_question('Five')[1])
				questions.append(get_question('Six')[1])
				questions.append(get_question('Seven')[1])
				questions.append(get_question('Eight')[1])
				questions.append(get_question('Nine')[1])
				questions.append(get_question('Seven')[1])
				questions.append(get_question('Eight')[1])
				questions.append(get_question('Nine')[1])
				return any_printable(your_diff,title,questions)
	q_id = 'One'; gq = get_question(q_id)
	vsections = [{'title':'Exponential Functions','subsections':[{'title':'Base e','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'}]}]
	q_id = 'Two'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Other Bases','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Three'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Properties Of Exponents','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	
	q_id = 'Four'; gq = get_question(q_id)
	vsections.append({'title':'Logarithmic Functions','subsections':[{'title':'Base e','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'}]})
	q_id = 'Five'; gq = get_question(q_id)
	vsections[1]['subsections'].append({'title':'Other Bases','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Six'; gq = get_question(q_id)
	vsections[1]['subsections'].append({'title':'Properties of Logarithms','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})

	q_id = 'Seven'; gq = get_question(q_id)
	vsections.append({'title':'Lightning Round','subsections':[{'title':'Easy','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'}]})
	q_id = 'Eight'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Medium','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Nine'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Hard','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'})
	
	num_subsections = 0
	for i in vsections:
		num_subsections = num_subsections+len(i['subsections'])
	frac_q = str(round(1./num_subsections,5))
	rcarr = [{'href':'exponentials_logarithms_lesson.html','title':'Exponentials/Logarithms Lesson'},{'href':'power_rule_worksheet.html','title':'Power Rule Worksheet'},{'href':'trigonometric_functions_worksheet.html','title':'Trig Functions Worksheet'},{'href':'#','title':'Logarithms Video'},{'href':'#','title':'Exponentials Explained'}]
	meta_title = 'Exponentials and Logarithms Derivatives Worksheet - Learn to differentiate exponential and logarithmic functions by working examples with Calculus College.'
	meta_des = "Infinitely many exponential and logarithmic functions to differentiate with step-by-step solutions if you make a mistake. Practice is the best way to improve."

	return render(request,'base_worksheet.html',{'pform':PrintableForm(),'related_content':rcarr,'title':meta_title,'meta_des':meta_des,'header_1':'Exponentials and Logarithms','sections':vsections,'fraction_questions':frac_q})

