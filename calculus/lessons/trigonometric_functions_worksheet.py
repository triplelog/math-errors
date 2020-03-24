from any_worksheet import *

def get_question(q_id):
	trig_fns = ['cos(x)','sin(x)','tan(x)','cot(x)','sec(x)','csc(x)']
	trig_fns_l = ['\cos{(x)}','\sin{(x)}','\\tan{(x)}','\cot{(x)}','\sec{(x)}','\csc{(x)}']
	inv_trigs = ['arccos(x)','arcsin(x)','arctan(x)','arccot(x)','arcsec(x)','arccsc(x)']
	inv_trig_ls = ['\cos^{-1}(x)','\sin^{-1}(x)','\\tan^{-1}(x)','\cot^{-1}(x)','\sec^{-1}(x)','\csc^{-1}(x)']
	polys = ['x^2+1','x^3+x-1','x+3','x^2-2x+3','x^5','x^4-x^2+x','2x^3','2x^2+x+1','x^3+5x^2-3x+2','2x-1']

	if q_id == 'One':
		q_1 = str(get_rand(['cos(x)','sin(x)'],[.5,.5]))
		return q_1,'\\'+q_1
	elif q_id == 'Two':
		q_1 = str(get_rand(['tan(x)','cot(x)','sec(x)','csc(x)'],[.25,.25,.25,.25]))
		return q_1,'\\'+q_1
	elif q_id == 'Three':
		q_1s = ['sin(x)','cos(x)','tan(x)','cot(x)','sec(x)','csc(x)']
		q_1_ls = ['2\sin(\\frac{1}{2}x)\cos(\\frac{1}{2}x)','\cot(x)\sin(x)','\sec(x)\sin(x)','\csc(x)\cos(x)','\\frac{\\tan(x)}{\sin(x)}','\\frac{\cot(x)}{\cos(x)}']
		q_n = get_rand(range(0,6),[.2,.2,.15,.15,.15,.15])

		return q_1s[q_n],q_1_ls[q_n]
	elif q_id == 'Four':
		q_1 = str(get_rand(['arccos(x)','arcsin(x)'],[.5,.5]))
		return q_1,'\\'+q_1
	elif q_id == 'Five':
		q_1 = get_rand(range(2,6),[.25,.25,.25,.25])
		return inv_trigs[q_1],inv_trig_ls[q_1]
	elif q_id == 'Six':
		q_1 = str(get_rand(['sin(x)','cos(x)','tan(x)','cot(x)','sec(x)','csc(x)'],[.2,.2,.15,.15,.15,.15]))
		return q_1,'\\'+q_1
	elif q_id == 'Seven':
		q_1 = get_rand(range(0,6),[.2,.2,.15,.15,.15,.15])
		return inv_trigs[q_1],inv_trig_ls[q_1]
	elif q_id == 'Eight':
		if random.random()<.5:
			if random.random()<.5:
				return get_question('Six')
			else:
				return get_question('Seven')
		else:
			return get_question('Three')


class WorksheetForm(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter answer here.','size':'30','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))

def trigonometric_functions_worksheet(request):
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
					return any_worksheet(form,'trigonometric',new_q,my_type)
				except:
					pass
			return any_worksheet(form,'trigonometric','noq','Zero')
		else:
			form = PrintableForm(request.POST)
			if (form.is_valid()):
				your_diff = form.cleaned_data['your_diff']
				title = 'Trigonometric Functions Worksheet'
				questions = []
				questions.append(get_question('One')[1])
				questions.append(get_question('Two')[1])
				questions.append(get_question('Three')[1])
				questions.append(get_question('Four')[1])
				questions.append(get_question('Five')[1])
				questions.append(get_question('Six')[1])
				questions.append(get_question('Seven')[1])
				questions.append(get_question('Eight')[1])
				questions.append(get_question('One')[1])
				questions.append(get_question('Six')[1])
				questions.append(get_question('Seven')[1])
				questions.append(get_question('Eight')[1])
				return any_printable(your_diff,title,questions)
	q_id = 'One'; gq = get_question(q_id)
	vsections = [{'title':'Basic Trigonometric Functions','subsections':[{'title':'Sine and Cosine','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'}]}]
	q_id = 'Two'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Others','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Three'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Trig Identities','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	
	q_id = 'Four'; gq = get_question(q_id)
	vsections.append({'title':'Inverse Trigonometric Functions','subsections':[{'title':'Arcsine and Arccosine','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'}]})
	q_id = 'Five'; gq = get_question(q_id)
	vsections[1]['subsections'].append({'title':'Others','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})

	q_id = 'Six'; gq = get_question(q_id)
	vsections.append({'title':'Lightning Round','subsections':[{'title':'Easy','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'}]})
	q_id = 'Seven'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Medium','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Eight'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Hard','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	
	num_subsections = 0
	for i in vsections:
		num_subsections = num_subsections+len(i['subsections'])
	frac_q = str(round(1./num_subsections,5))
	rcarr = [{'href':'trigonometric_functions_lesson.html','title':'Trig Derivatives Lesson'},{'href':'exponentials_logarithms_worksheet.html','title':'Exp/Logs Worksheet'},{'href':'product_rule_worksheet.html','title':'Product Rule Worksheet'},{'href':'#','title':'Trigonometry Video'},{'href':'#','title':'Trigonometry Explained'}]
	meta_title = 'Trigonometric Derivatives Worksheet - Learn how to differentiate trigonometric functions by working examples with Calculus College.'
	meta_des = "Infinitely many power rule problems with step-by-step solutions if you make a mistake. Progress through several types of problems that help you improve."
	return render(request,'base_worksheet.html',{'pform':PrintableForm(),'related_content':rcarr,'title':meta_title,'meta_des':meta_des,'header_1':'Trigonometric Derivatives','sections':vsections,'fraction_questions':frac_q})
