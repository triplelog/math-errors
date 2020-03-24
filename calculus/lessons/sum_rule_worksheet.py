from any_worksheet import *

def get_question(q_id):
	trig_fns = ['cos(x)','sin(x)','tan(x)','cot(x)','sec(x)','csc(x)']
	trig_fns_l = ['\cos{(x)}','\sin{(x)}','\\tan{(x)}','\cot{(x)}','\sec{(x)}','\csc{(x)}']
	inv_trigs = ['arccos(x)','arcsin(x)','arctan(x)','arccot(x)','arcsec(x)','arccsc(x)']
	polys = ['x^2+1','x^3+x-1','x+3','x^2-2x+3','x^5','x^4-x^2+x','2x^3','2x^2+x+1','x^3+5x^2-3x+2','2x-1']

	if q_id == 'One':
		q_1 = str(get_rand(range(2,10),[.3,.25,.15,.1,.05,.05,.05,.05]))
		x_tf = get_rand(range(0,6),[.25,.25,.15,.15,.1,.1])
		in_fs = ['x^'+q_1,'x^'+q_1,'x^'+q_1,'ln(x)','e^x',trig_fns[x_tf]]
		in_f_ls = ['x^'+q_1,'x^'+q_1,'x^'+q_1,'\ln(x)','e^x',trig_fns_l[x_tf]]
		ch_x = random.randint(0,5)
		in_fn = in_fs[ch_x]
		in_fn_l = in_f_ls[ch_x]
		if random.random()<.26:
			q_c = str(random.randint(-7,-2))
		else:
			if random.random()<.2:
				q_c = '-'
			else:
				q_c = str(random.randint(2,12))
		return q_c+in_fn,q_c+in_fn_l
	elif q_id == 'Two':
		q_1 = get_rand_poly('x')
		return q_1,q_1
	elif q_id == 'Three':
		if random.random()<.5:
			q_1a = get_question('One')
			q_2a = get_question('One')
			q_1 = q_1a[0]
			q_2=q_2a[0]

			q_0 = q_1
			if q_2[0]=='-':
				q_0=q_0+q_2
			else:
				q_0=q_0+'+'+q_2

			q_1 = q_1a[1]
			q_2=q_2a[1]

			q_0l = q_1
			if q_2[0]=='-':
				q_0l=q_0l+q_2
			else:
				q_0l=q_0l+'+'+q_2
			return q_0,q_0l
		else:
			if random.random()<.8:
				q_1a = get_question('One')
				q_2a = get_question('One')
				q_3a = get_question('One')
				q_1 = q_1a[0]
				q_2=q_2a[0]
				q_3=q_3a[0]

				q_0 = q_1
				if q_2[0]=='-':
					q_0=q_0+q_2
				else:
					q_0=q_0+'+'+q_2
				if q_3[0]=='-':
					q_0=q_0+q_3
				else:
					q_0=q_0+'+'+q_3

				q_1 = q_1a[1]
				q_2=q_2a[1]
				q_3=q_3a[1]
				q_0l = q_1
				if q_2[0]=='-':
					q_0l=q_0l+q_2
				else:
					q_0l=q_0l+'+'+q_2
				if q_3[0]=='-':
					q_0l=q_0l+q_3
				else:
					q_0l=q_0l+'+'+q_3
				return q_0,q_0l
			else:
				q_1a = get_question('One')
				q_2a = get_question('One')
				q_3a = get_question('One')
				q_4a = get_question('One')
				q_1 = q_1a[0]
				q_2=q_2a[0]
				q_3=q_3a[0]
				q_4=q_4a[0]

				q_0 = q_1
				if q_2[0]=='-':
					q_0=q_0+q_2
				else:
					q_0=q_0+'+'+q_2
				if q_3[0]=='-':
					q_0=q_0+q_3
				else:
					q_0=q_0+'+'+q_3
				if q_4[0]=='-':
					q_0=q_0+q_4
				else:
					q_0=q_0+'+'+q_4

				q_1 = q_1a[1]
				q_2=q_2a[1]
				q_3=q_3a[1]
				q_4=q_4a[1]
				q_0l = q_1
				if q_2[0]=='-':
					q_0l=q_0l+q_2
				else:
					q_0l=q_0l+'+'+q_2
				if q_3[0]=='-':
					q_0l=q_0l+q_3
				else:
					q_0l=q_0l+'+'+q_3
				if q_4[0]=='-':
					q_0l=q_0l+q_4
				else:
					q_0l=q_0l+'+'+q_4
				return q_0,q_0l


	elif q_id == 'Four':
		q_1a = get_question('One')
		q_2a = get_question('One')
		q_1 = q_1a[0]
		q_2=q_2a[0]

		q_0 = q_1
		if q_2[0]=='-':
			q_0=q_0+q_2
		else:
			q_0=q_0+'+'+q_2

		q_1 = q_1a[1]
		q_2=q_2a[1]

		q_0l = q_1
		if q_2[0]=='-':
			q_0l=q_0l+q_2
		else:
			q_0l=q_0l+'+'+q_2
		return q_0,q_0l
	elif q_id == 'Five':
		q_1a = get_question('One')
		q_2a = get_question('One')
		q_3a = get_question('One')
		q_1 = q_1a[0]
		q_2=q_2a[0]
		q_3=q_3a[0]

		q_0 = q_1
		if q_2[0]=='-':
			q_0=q_0+q_2
		else:
			q_0=q_0+'+'+q_2
		if q_3[0]=='-':
			q_0=q_0+q_3
		else:
			q_0=q_0+'+'+q_3

		q_1 = q_1a[1]
		q_2=q_2a[1]
		q_3=q_3a[1]
		q_0l = q_1
		if q_2[0]=='-':
			q_0l=q_0l+q_2
		else:
			q_0l=q_0l+'+'+q_2
		if q_3[0]=='-':
			q_0l=q_0l+q_3
		else:
			q_0l=q_0l+'+'+q_3
		return q_0,q_0l
	elif q_id == 'Six':
		q_1a = get_question('One')
		q_2a = get_question('One')
		q_3a = get_question('One')
		q_4a = get_question('One')
		q_1 = q_1a[0]
		q_2=q_2a[0]
		q_3=q_3a[0]
		q_4=q_4a[0]

		q_0 = q_1
		if q_2[0]=='-':
			q_0=q_0+q_2
		else:
			q_0=q_0+'+'+q_2
		if q_3[0]=='-':
			q_0=q_0+q_3
		else:
			q_0=q_0+'+'+q_3
		if q_4[0]=='-':
			q_0=q_0+q_4
		else:
			q_0=q_0+'+'+q_4

		q_1 = q_1a[1]
		q_2=q_2a[1]
		q_3=q_3a[1]
		q_4=q_4a[1]
		q_0l = q_1
		if q_2[0]=='-':
			q_0l=q_0l+q_2
		else:
			q_0l=q_0l+'+'+q_2
		if q_3[0]=='-':
			q_0l=q_0l+q_3
		else:
			q_0l=q_0l+'+'+q_3
		if q_4[0]=='-':
			q_0l=q_0l+q_4
		else:
			q_0l=q_0l+'+'+q_4
		return q_0,q_0l


class WorksheetForm(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter answer here.','size':'30','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))

def sum_rule_worksheet(request):
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
					return any_worksheet(form,'sum',new_q,my_type)
				except:
					pass
			return any_worksheet(form,'sum','noq','Zero')
		else:
			form = PrintableForm(request.POST)
			if (form.is_valid()):
				your_diff = form.cleaned_data['your_diff']
				title = 'Sum Rule Worksheet'
				questions = []
				questions.append(get_question('One')[1])
				questions.append(get_question('Two')[1])
				questions.append(get_question('Three')[1])
				questions.append(get_question('Four')[1])
				questions.append(get_question('Five')[1])
				questions.append(get_question('Six')[1])
				questions.append(get_question('One')[1])
				questions.append(get_question('Two')[1])
				questions.append(get_question('Three')[1])
				questions.append(get_question('Four')[1])
				questions.append(get_question('Five')[1])
				questions.append(get_question('Six')[1])
				return any_printable(your_diff,title,questions)
	q_id = 'One'; gq = get_question(q_id)
	vsections = [{'title':'The Sum Rule','subsections':[{'title':'Constant Multiples','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'}]}]
	q_id = 'Two'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Polynomials','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'})
	q_id = 'Three'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Other Sums','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'})


	q_id = 'Four'; gq = get_question(q_id)
	vsections.append({'title':'Lightning Round','subsections':[{'title':'Easy','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'}]})
	q_id = 'Five'; gq = get_question(q_id)
	vsections[1]['subsections'].append({'title':'Medium','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Six'; gq = get_question(q_id)
	vsections[1]['subsections'].append({'title':'Hard','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'})
	
	num_subsections = 0
	for i in vsections:
		num_subsections = num_subsections+len(i['subsections'])
	frac_q = str(round(1./num_subsections,5))
	rcarr = [{'href':'sum_rule_lesson.html','title':'Sum Rule Lesson'},{'href':'product_rule_worksheet.html','title':'Product Rule Worksheet'},{'href':'power_rule_worksheet.html','title':'Power Rule Worksheet'},{'href':'#','title':'Sum Rule Video'},{'href':'#','title':'Sum Rule Explained'}]
	meta_title = 'Sum Rule Worksheet - Learn the Sum Rule by working examples with Calculus College.'
	meta_des = "Infinitely many sum rule problems with step-by-step solutions if you make a mistake. Progress through several types of problems that help you improve."

	return render(request,'base_worksheet.html',{'pform':PrintableForm(),'related_content':rcarr,'title':meta_title,'meta_des':meta_des,'header_1':'Sum Rule Worksheet','sections':vsections,'fraction_questions':frac_q})

