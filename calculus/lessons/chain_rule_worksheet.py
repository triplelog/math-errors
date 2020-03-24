from any_worksheet import *

def get_question(q_id):
	trig_fns = ['cos(x)','sin(x)','tan(x)','cot(x)','sec(x)','csc(x)']
	trig_fns_l = ['\cos{(x)}','\sin{(x)}','\\tan{(x)}','\cot{(x)}','\sec{(x)}','\csc{(x)}']
	inv_trigs = ['arccos(x)','arcsin(x)','arctan(x)','arccot(x)','arcsec(x)','arccsc(x)']
	polys = ['x^2+1','x^3+x-1','x+3','x^2-2x+3','x^5','x^4-x^2+x','2x^3','2x^2+x+1','x^3+5x^2-3x+2','2x-1']

	if q_id == 'One':
		q_1 = str(get_rand(range(2,11),[.25,.25,.15,.1,.05,.05,.05,.05,.05]))

		in_fs = [get_rand_poly('x'),get_rand_poly('x'),'ln(x)','e^x+'+str(random.randint(1,9)),get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])]
		x_r = random.randint(0,4)
		in_fn = in_fs[x_r]
		if x_r in [2,4]:
			return '('+in_fn+')^('+q_1+')', '(\\'+in_fn+')^{'+q_1+'}'
		else:
			return '('+in_fn+')^('+q_1+')', '('+in_fn+')^{'+q_1+'}'
	elif q_id == 'Two':
		q_1 = get_rand_poly('x')
		return 'ln('+q_1+')', '\ln{('+q_1+')}'
	elif q_id == 'Three':
		q_n = get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])
		q_d = get_rand_poly('x')
		q_1 = q_n.replace('x',q_d)

		return q_1, '\\'+q_1[:3]+'{('+q_1[4:]+'}'
	elif q_id == 'Four':
		in_fs = [get_rand_poly('x'),get_rand_poly('x'),get_rand_poly('x'),get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])]
		xrand = random.randint(0,3)
		q_1 = in_fs[xrand]
		if xrand ==3:
			return 'e^('+q_1+')', 'e^{\\'+q_1+'}'
		else:
			return 'e^('+q_1+')', 'e^{'+q_1+'}'
	elif q_id == 'Five':
		in_fn = get_rand_poly('x')
		f1 = get_rand(range(0,6),[.25,.25,.15,.15,.1,.1])
		f2 = get_rand(range(0,6),[.25,.25,.15,.15,.1,.1])
		f3 = get_rand(range(0,6),[.25,.25,.15,.15,.1,.1])
		f4 = get_rand(range(0,6),[.25,.25,.15,.15,.1,.1])
		out_fns = [trig_fns[f1],'ln(x)','e^(x)','(x)^2']
		mid_fns = ['e^(x)',trig_fns[f2],trig_fns[f3],trig_fns[f4]]
		out_fns_l = [trig_fns_l[f1],'\ln{(x)}','e^{x}','{x}^2']
		mid_fns_l = ['e^{x}',trig_fns_l[f2],trig_fns_l[f3],trig_fns_l[f4]]
		i = random.randint(0,3)
		q_1 = out_fns[i].replace('x',mid_fns[i]).replace('x',in_fn)	
		q_1_l = out_fns_l[i].replace('x',mid_fns_l[i]).replace('x',in_fn)	
				
		return q_1, q_1_l
	elif q_id == 'Six':
		q_idx = get_rand(['Two','Three','Four'],[.4,.3,.3])
		if q_idx == 'Two':
			q_1 = get_rand_poly('x',[.6,1,1])
			if random.random()<.5:
				return 'sin(('+q_1+')ln(x))', '\sin{(('+q_1+')\ln{(x)})}'
			else:
				return 'cos(('+q_1+')ln(x))', '\cos{(('+q_1+')\ln{(x)})}'
		elif q_idx == 'Three':
			q_n = get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])
			q_d = get_rand_poly('x',[.6,1,1])

			return 'ln(('+q_d+')'+q_n+')','\ln{(('+q_d+')\\'+q_n+')}'
		elif q_idx == 'Four':
			if random.random()<.75:
				q_d = get_rand_poly('x',[.6,1,1])
				q_1 = '(e^x('+q_d+'))^'+str(random.randint(2,7))
				q_1_l= q_1
			else:
				q_d = get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])
				q_1 = '(e^x'+q_d+')^'+str(random.randint(2,7))
				q_1_l = '(e^x\\'+q_d+')^'+str(random.randint(2,7))
			return q_1,q_1_l
	elif q_id == 'Seven':
		q_idx = get_rand(['Two','Three','Four'],[.4,.3,.3])
		if q_idx == 'Two':
			q_1 = get_rand_poly('x',[.6,1,1])
			if random.random()<.5:
				return 'sin(('+q_1+')/ln(x))', '\sin{(\\frac{('+q_1+')}{\ln{(x)}})}'
			else:
				return 'cos(('+q_1+')/ln(x))', '\cos{(\\frac{('+q_1+')}{\ln{(x)}})}'
		elif q_idx == 'Three':
			q_n = get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])
			q_d = get_rand_poly('x',[.6,1,1])

			return 'ln(('+q_d+')/'+q_n+')','\ln{(\\frac{('+q_d+')}{\\'+q_n+'})}'
		elif q_idx == 'Four':
			if random.random()<.75:
				q_d = get_rand_poly('x',[.6,1,1])
				q_1 = '(e^x/('+q_d+'))^'+str(random.randint(2,7))
				q_1_l= '(\\frac{e^x}{'+q_d+'})^'+str(random.randint(2,7))
			else:
				q_d = get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])
				q_1 = '(e^x/'+q_d+')^'+str(random.randint(2,7))
				q_1_l = '(\\frac{e^x}{\\'+q_d+'})^'+str(random.randint(2,7))
			return q_1,q_1_l
	elif q_id == 'Eight':
		return get_question('One')
	elif q_id == 'Nine':
		if random.random()<.3:
			return get_question('Two')
		else:
			if random.random()<.4:
				return get_question('Three')
			else:
				return get_question('Four')
	elif q_id == 'Ten':
		if random.random()<.3:
			return get_question('Five')
		else:
			if random.random()<.6:
				return get_question('Six')
			else:
				return get_question('Seven')

class WorksheetForm(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter answer here.','size':'30','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))


def chain_rule_worksheet(request):
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
					return any_worksheet(form,'chain',new_q,my_type)
				except:
					pass
			return any_worksheet(form,'chain','noq','Zero')
		else:
			form = PrintableForm(request.POST)
			if (form.is_valid()):
				your_diff = form.cleaned_data['your_diff']
				title = 'Chain Rule Worksheet'
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
				questions.append(get_question('Ten')[1])
				questions.append(get_question('Nine')[1])
				questions.append(get_question('Ten')[1])
				return any_printable(your_diff,title,questions)
		
	q_id = 'One'; gq = get_question(q_id)
	vsections = [{'title':'The Chain Rule','subsections':[{'title':'Powers','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'}]}]
	q_id = 'Two'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Logarithms','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'})
	q_id = 'Three'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Trigonometry','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'})
	q_id = 'Four'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Exponentials','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'})
	
	q_id = 'Five'; gq = get_question(q_id)
	vsections.append({'title':'Advanced','subsections':[{'title':'Double Chain','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'}]})
	q_id = 'Six'; gq = get_question(q_id)
	vsections[1]['subsections'].append({'title':'Product Rule','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Seven'; gq = get_question(q_id)
	vsections[1]['subsections'].append({'title':'Quotient Rule','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'})

	q_id = 'Eight'; gq = get_question(q_id)
	vsections.append({'title':'Lightning Round','subsections':[{'title':'Easy','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'}]})
	q_id = 'Nine'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Medium','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Ten'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Hard','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	
	num_subsections = 0
	for i in vsections:
		num_subsections = num_subsections+len(i['subsections'])
	frac_q = str(round(1./num_subsections,5))
	rcarr = [{'href':'chain_rule_lesson.html','title':'Chain Rule Lesson'},{'href':'product_rule_worksheet.html','title':'Product Rule Worksheet'},{'href':'quotient_rule_worksheet.html','title':'Quotient Rule Worksheet'},{'href':'#','title':'Chain Rule Video'},{'href':'#','title':'Chain Rule Explained'}]
	meta_title = 'Chain Rule Worksheet - Learn the Chain Rule by working examples with Calculus College.'
	meta_des = "Infinitely many chain rule problems with step-by-step solutions if you make a mistake. Progress through several types of problems that help you improve."
	return render(request,'base_worksheet.html',{'pform':PrintableForm(),'related_content':rcarr,'meta-des':meta_des,'title':meta_title,'header_1':'Chain Rule Worksheet','sections':vsections,'fraction_questions':frac_q})


