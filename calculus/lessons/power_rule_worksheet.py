from any_worksheet import *
def get_question(q_id):
	if q_id == 'One':
		q_1 = str(get_rand(range(2,11),[.25,.25,.15,.1,.05,.05,.05,.05,.05]))
		return 'x^('+q_1+')', 'x^{'+q_1+'}'
	elif q_id == 'Two':
		q_1 = str(-1*get_rand(range(1,11),[.25,.2,.15,.1,.05,.05,.05,.05,.05,.05]))
		return 'x^('+q_1+')', 'x^{'+q_1+'}'
	elif q_id == 'Three':
		q_n = get_rand(range(1,10),[.25,.25,.15,.1,.05,.05,.05,.05,.05])
		q_d = get_rand_a(range(2,11),[.25,.25,.15,.1,.05,.05,.05,.05,.05],q_n)
		q_gcd = gcd(q_n,q_d)
		if q_gcd != q_d:
			q_1 = str(int(q_n/q_gcd))+'/'+str(int(q_d/q_gcd))
		else:
			q_1 = str(int(q_n))+'/'+str(int(q_d+1))
		return 'x^('+q_1+')', 'x^{'+q_1+'}'
	elif q_id == 'Four':
		q_n = get_rand(range(1,10),[.25,.25,.15,.1,.05,.05,.05,.05,.05])
		q_d = get_rand_a(range(2,11),[.25,.25,.15,.1,.05,.05,.05,.05,.05],q_n)
		q_gcd = gcd(q_n,q_d)
		if q_gcd != q_d:
			q_1 = str(int(-1*q_n/q_gcd))+'/'+str(int(q_d/q_gcd))
		else:
			q_1 = str(int(-1*q_n))+'/'+str(int(q_d+1))
		return 'x^('+q_1+')', 'x^{'+q_1+'}'
	elif q_id == 'Five':
		q_c = get_rand(range(1,10),[.25,.25,.15,.1,.05,.05,.05,.05,.05])
		q_e = get_rand(range(1,18,2),[.25,.25,.15,.1,.05,.05,.05,.05,.05])
		if random.random()<.5:
			if q_c >1:
				q_1 = 'x^('+str(q_c)+')*'+'sqrt(x)'
				q_1_l = 'x^{'+str(q_c)+'}'+'\sqrt{x}'
			else:
				q_1 = 'x*sqrt(x)'
				q_1_l = 'x\sqrt{x}'
		else:
			if q_e>1:
				if random.random()<.5:
					q_1 = 'x*sqrt(x^('+str(q_e)+'))'
					q_1_l = 'x\sqrt{x^{'+str(q_e)+'}}'
				else:
					q_1 = 'sqrt(x^('+str(q_e)+'))'
					q_1_l = '\sqrt{x^{'+str(q_e)+'}}'
			else:
				if random.random()<.5:
					q_1 = 'x*sqrt(x)'
					q_1_l = 'x\sqrt{x}'
				else:
					q_1 = 'sqrt(x)'
					q_1_l = '\sqrt{x}'
		return q_1, q_1_l
	elif q_id == 'Six':
		q_d = get_rand(range(1,10),[.25,.25,.15,.1,.05,.05,.05,.05,.05])
		if q_d > 1:
			q_1 = '1/x^('+str(q_d)+')'
		else:
			q_1 = '1/x'
		if q_d > 1:
			q_1_l = '\\frac{1}{x^{'+str(q_d)+'}}'
		else:
			q_1_l = '\\frac{1}{x}'
		return q_1, q_1_l
	elif q_id == 'Seven':
		if random.random()<.6:
			return get_question('One')
		else:
			return get_question('Two')
	elif q_id == 'Eight':
		if random.random()<.5:
			return get_question('Three')
		else:
			if random.random()<.5:
				return get_question('Two')
			else:
				return get_question('Four')
	elif q_id == 'Nine':
		if random.random()<.6:
			return get_question('Five')
		else:
			return get_question('Six')

class WorksheetForm(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter answer here.','size':'30','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))

def power_rule_worksheet(request):
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
					return any_worksheet(form,'power',new_q,my_type)
				except:
					pass
			return any_worksheet(form,'power','noq','Zero')
		else:
			form = PrintableForm(request.POST)
			if (form.is_valid()):
				your_diff = form.cleaned_data['your_diff']
				title = 'Power Rule Worksheet'
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
	vsections = [{'title':'The Power Rule','subsections':[{'title':'Positive Exponents','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'}]}]
	q_id = 'Two'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Negative Exponents','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Three'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Fractional Exponents','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Four'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Negative Fractional Exponents','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})

	q_id = 'Five'; gq = get_question(q_id)
	vsections.append({'title':'Rewriting Functions','subsections':[{'title':'Radicals','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'}]})
	q_id = 'Six'; gq = get_question(q_id)
	vsections[1]['subsections'].append({'title':'Fractions','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'})

	q_id = 'Seven'; gq = get_question(q_id)
	vsections.append({'title':'Lightning Round','subsections':[{'title':'Easy','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'}]})
	q_id = 'Eight'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Medium','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Nine'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Hard','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	num_subsections = 0
	for i in vsections:
		num_subsections = num_subsections+len(i['subsections'])
	frac_q = str(round(1./num_subsections,3))
	rcarr = [{'href':'power_rule_lesson.html','title':'Power Lesson'},{'href':'exponentials_logarithms_worksheet.html','title':'Exp/Logs Worksheet'},{'href':'trigonometric_functions_worksheet.html','title':'Trig Worksheet'},{'href':'#','title':'Power Rule Video'},{'href':'#','title':'Power Rule Explained'}]
	meta_title = 'Power Rule Worksheet - Learn the Power Rule by working examples with Calculus College.'
	meta_des = "Infinitely many power rule problems with step-by-step solutions if you make a mistake. Progress through several types of problems that help you improve."
	return render(request,'base_worksheet.html',{'pform':PrintableForm(),'related_content':rcarr,'title':meta_title,'meta_des':meta_des,'header_1':'Power Rule Worksheet','sections':vsections,'fraction_questions':frac_q})

