from any_worksheet import *

def get_question(q_id):
	trig_fns = ['cos(x)','sin(x)','tan(x)','cot(x)','sec(x)','csc(x)']
	trig_fns_l = ['\cos{(x)}','\sin{(x)}','\\tan{(x)}','\cot{(x)}','\sec{(x)}','\csc{(x)}']
	inv_trigs = ['arccos(x)','arcsin(x)','arctan(x)','arccot(x)','arcsec(x)','arccsc(x)']
	polys = ['x^2+1','x^3+x-1','x+3','x^2-2x+3','x^5','x^4-x^2+x','2x^3','2x^2+x+1','x^3+5x^2-3x+2','2x-1']

	if q_id == 'One':
		q_1 = str(get_rand(range(2,11),[.25,.25,.15,.1,.05,.05,.05,.05,.05]))
		in_fs = [get_rand_poly('x'),get_rand_poly('x'),'ln(x)','e^x',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])]
		ch_x = random.randint(0,4)
		in_fn = in_fs[ch_x]
		if ch_x in [2,4]:
			return 'x^'+str(q_1)+'/('+in_fn+')','\\frac{x^{'+str(q_1)+'}}{\\'+in_fn+'}'
		else:
			return 'x^'+str(q_1)+'/('+in_fn+')','\\frac{x^{'+str(q_1)+'}}{('+in_fn+')}'
	elif q_id == 'Two':
		q_1 = get_rand_poly('x')
		return '('+q_1+')/ln(x)', '\\frac{('+q_1+')}{\ln{(x)}}'
	elif q_id == 'Three':
		q_n = get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])
		q_d = get_rand_poly('x')

		return '('+q_d+')/'+q_n,'\\frac{('+q_d+')}{\\'+q_n+'}'
	elif q_id == 'Four':
		if random.random()<.75:
			q_d = get_rand_poly('x')
			q_1 = 'e^x/('+q_d+')'
			q_1_l= '\\frac{e^x}{('+q_d+')}'
		else:
			q_d = get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])
			q_1 = 'e^x/'+q_d
			q_1_l = '\\frac{e^x}{\\'+q_d+'}'
		

		return q_1,q_1_l
	elif q_id == 'Five':
		if random.random()<.4:
			q_1 = get_rand(range(0,6),[.25,.25,.15,.15,.1,.1])
			q_2 = get_rand_a(range(0,6),[.25,.25,.15,.15,.1,.1],q_1)
			q_p = str(random.randint(2,8))
			q_3 = '('+trig_fns[q_1]+'+'+trig_fns[q_2]+')/x^'+q_p
			q_3_l = '\\frac{(\\'+trig_fns[q_1]+'+\\'+trig_fns[q_2]+')}{x^'+q_p+'}'
			return q_3, q_3_l
		else:
			if random.random()<.5:
				q_p = str(random.randint(2,8))
				q_3 = '(e^x+x^'+q_p+')/ln(x)'
				q_3_l = '\\frac{(e^x+x^'+q_p+')}{\ln(x)}'
				return q_3,q_3_l
			else:
				q_p = str(random.randint(2,8))
				q_3 = '(ln(x)+x^'+q_p+')/e^x'
				q_3_l = '\\frac{(\ln(x)+x^'+q_p+')}{e^x}'
				return q_3,q_3_l
	elif q_id == 'Six':
		ntarr = [.75,1,0]
		xr = random.random()
		if xr < .25:
			q_p = 'x^'+str(random.randint(2,6))
			q_t = get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])
			q_elr = random.random()
			if q_elr < .5:
				q_1 = q_p+q_t+'/e^x'
				q_1_l = '\\frac{'+q_p+'\\'+q_t+'}{e^x}'
			else:
				q_1 = q_p+q_t+'/ln(x)'
				q_1_l = '\\frac{'+q_p+'\\'+q_t+'}{\ln(x)}'
		elif xr < .5:
			q_p = 'x^'+str(random.randint(2,6))
			q_d = '('+get_rand_poly('x',ntarr)+')'
			q_elr = random.random()
			if q_elr < .34:
				q_1 = q_p+q_d+'/e^x'
				q_1_l = '\\frac{'+q_p+q_d+'}{e^x}'
			if q_elr < .67:
				q_t = get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])
				q_1 = q_p+q_d+'/'+q_t
				q_1_l = '\\frac{'+q_p+q_d+'}{\\'+q_t+'}'
			else:
				q_1 = q_p+q_d+'/ln(x)'
				q_1_l = '\\frac{'+q_p+q_d+'}{\ln(x)}'
		elif xr < .75:
			q_p = 'x^'+str(random.randint(2,6))
			q_d = get_rand_poly('x',ntarr)
			q_d2 = get_rand_poly('x',ntarr)
			q_1 = q_p+'('+q_d+')/('+q_d2+')'
			q_1_l= '\\frac{'+q_p+'('+q_d+')}{('+q_d2+')}'
		else:
			q_p = 'x^'+str(random.randint(2,6))
			q_t = get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])
			q_t2 = get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])
			q_1 = q_p+q_t+'/'+q_t2
			q_1_l= '\\frac{'+q_p+'\\'+q_t+'}{\\'+q_t2+'}'
				
		return q_1, q_1_l

	elif q_id == 'Seven':
		in_fs = ['ln(x)','e^x',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])]
		ch_x = random.randint(0,2)
		in_fn = in_fs[ch_x]
		if ch_x in [0,2]:
			return 'x/('+in_fn+')','\\frac{x}{\\'+in_fn+'}'
		else:
			return 'x/('+in_fn+')','\\frac{x}{'+in_fn+'}'
	elif q_id == 'Eight':
		if random.random()<.4:
			return get_question('Four')
		else:
			if random.random()<.5:
				return get_question('Three')
			else:
				return get_question('Two')
	elif q_id == 'Nine':
		return get_question('Six')

class WorksheetForm(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter answer here.','size':'30','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))

def quotient_rule_worksheet(request):
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
					return any_worksheet(form,'quotient',new_q,my_type)
				except:
					pass
			return any_worksheet(form,'quotient','noq','Zero')
		else:
			form = PrintableForm(request.POST)
			if (form.is_valid()):
				your_diff = form.cleaned_data['your_diff']
				title = 'Quotient Rule Worksheet'
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
	vsections = [{'title':'The Quotient Rule','subsections':[{'title':'Powers','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'}]}]
	q_id = 'Two'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Logarithms','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Three'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Trigonometry','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Four'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Exponentials','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	
	q_id = 'Five'; gq = get_question(q_id)
	vsections.append({'title':'Advanced','subsections':[{'title':'Sums','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'}]})
	q_id = 'Six'; gq = get_question(q_id)
	vsections[1]['subsections'].append({'title':'Products','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'})


	q_id = 'Seven'; gq = get_question(q_id)
	vsections.append({'title':'Lightning Round','subsections':[{'title':'Easy','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'}]})
	q_id = 'Eight'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Medium','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'})
	q_id = 'Nine'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Hard','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'})
	
	num_subsections = 0
	for i in vsections:
		num_subsections = num_subsections+len(i['subsections'])
	frac_q = str(round(1./num_subsections,5))
	rcarr = [{'href':'quotient_rule_lesson.html','title':'Quotient Rule Lesson'},{'href':'product_rule_worksheet.html','title':'Product Rule Worksheet'},{'href':'chain_rule_worksheet.html','title':'Chain Rule Worksheet'},{'href':'#','title':'Quotient Rule Video'},{'href':'#','title':'Quotient Rule Explained'}]
	meta_title = 'Quotient Rule Worksheet - Learn the Quotient Rule by working examples with Calculus College.'
	meta_des = "Infinitely many quotient rule problems with step-by-step solutions if you make a mistake. Progress through several types of problems that help you improve."

	return render(request,'base_worksheet.html',{'pform':PrintableForm(),'related_content':rcarr,'title':meta_title,'meta_des':meta_des,'header_1':'Quotient Rule Worksheet','sections':vsections,'fraction_questions':frac_q})

