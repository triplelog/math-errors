from any_worksheet import *

def get_question(q_id):
	trig_fns = ['cos(x)','sin(x)','tan(x)','cot(x)','sec(x)','csc(x)']
	trig_fns_l = ['\cos{(x)}','\sin{(x)}','\\tan{(x)}','\cot{(x)}','\sec{(x)}','\csc{(x)}']
	inv_trigs = ['arccos(x)','arcsin(x)','arctan(x)','arccot(x)','arcsec(x)','arccsc(x)']
	polys = ['x^2+1','x^3+x-1','x+3','x^2-2x+3','x^5','x^4-x^2+x','2x^3','2x^2+x+1','x^3+5x^2-3x+2','2x-1']

	if q_id == 'One':
		x_r = str(random.randint(2,9))
		if random.random()>.5:
			return 'x^('+x_r+'x)','x^{'+x_r+'x}'
		else:
			return 'x^x','x^x'
	elif q_id == 'Two':
		f_1 = ['ln(x)',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1]),get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])]
		f_2 = random.randint(0,2)
		f_3 = f_1[f_2]
		return 'x^'+'('+f_3+')', 'x^'+'{\\'+f_3+'}'
	elif q_id == 'Three':
		in_fs = [get_rand_poly('x',[.8,1,1]),get_rand_poly('x',[.8,1,1]),get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])]
		xrand = random.randint(0,2)
		if xrand==2:
			return '('+in_fs[xrand]+')^x','(\\'+in_fs[xrand]+')^x'
		else:
			return '('+in_fs[xrand]+')^x','('+in_fs[xrand]+')^x'
	elif q_id == 'Four':
		f_1 = ['ln(x)',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1]),get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])]
		f_2 = random.randint(0,2)
		f_3 = f_1[f_2]
		in_fs = [get_rand_poly('x',[.8,1,1]),get_rand_poly('x',[.8,1,1]),get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])]
		xrand = random.randint(0,2)
		if xrand==2:
			return '('+in_fs[xrand]+')^('+f_3+')','(\\'+in_fs[xrand]+')^{\\'+f_3+'}'
		else:
			return '('+in_fs[xrand]+')^('+f_3+')','('+in_fs[xrand]+')^{\\'+f_3+'}'
	elif q_id == 'Five':
		f0 = get_rand_poly('x',[1,1,1])
		f1 = get_rand(range(0,6),[.25,.25,.15,.15,.1,.1])
		f2 = get_rand(range(0,6),[.25,.25,.15,.15,.1,.1])

		in_fs = [trig_fns[f1],trig_fns[f2],'e^(x)',get_rand_poly('x',[1,1,1])]
		in_fs_l =[trig_fns_l[f1],trig_fns_l[f2],'e^{x}',get_rand_poly('x',[1,1,1])]
		xrand = random.randint(0,3)
		if xrand==3:
			return '('+in_fs[xrand]+')('+f0+')','('+in_fs_l[xrand]+')('+f0+')'
		else:
			return '('+in_fs[xrand]+')('+f0+')',in_fs_l[xrand]+'('+f0+')'
	elif q_id == 'Six':
		f0 = get_rand_poly('x',[1,1,1])
		f00 = get_rand_poly('x',[1,1,1])
		f000 = get_rand_poly('x',[1,1,1])
		f1 = get_rand(range(0,6),[.25,.25,.15,.15,.1,.1])
		f2 = get_rand(range(0,6),[.25,.25,.15,.15,.1,.1])

		in_fs = [trig_fns[f1],trig_fns[f2],'e^(x)',get_rand_poly('x',[1,1,1])]
		in_fs_l =[trig_fns_l[f1],trig_fns_l[f2],'e^{x}',get_rand_poly('x',[1,1,1])]
		xrand = random.randint(0,3)
		xr2 = str(random.randint(2,6))
		if xrand==3:
			return '('+in_fs[xrand]+')('+f0+')('+f00+')^'+xr2+'('+f000+')','('+in_fs_l[xrand]+')('+f0+')('+f00+')^'+xr2+'('+f000+')'
		else:
			return '('+in_fs[xrand]+')('+f0+')('+f00+')^'+xr2+'('+f000+')',in_fs_l[xrand]+'('+f0+')('+f00+')^'+xr2+'('+f000+')'
	elif q_id == 'Seven':
		f0 = get_rand_poly('x',[1,1,1])
		f00 = get_rand_poly('x',[1,1,1])
		f000 = get_rand_poly('x',[1,1,1])
		f0000 = get_rand_poly('x',[1,1,1])
		f1 = get_rand(range(0,6),[.25,.25,.15,.15,.1,.1])
		f2 = get_rand(range(0,6),[.25,.25,.15,.15,.1,.1])

		in_fs = [trig_fns[f1],trig_fns[f2],'e^(x)',get_rand_poly('x',[1,1,1])]
		in_fs_l =[trig_fns_l[f1],trig_fns_l[f2],'e^{x}',get_rand_poly('x',[1,1,1])]
		xrand = random.randint(0,3)
		xr2 = str(random.randint(2,6))
		if xrand==3:
			return '('+in_fs[xrand]+')('+f0+')('+f00+')^'+xr2+'/(('+f000+')('+f0000+'))','\\frac{('+in_fs_l[xrand]+')('+f0+')('+f00+')^'+xr2+'}{('+f000+')('+f0000+')}'
		else:
			return '('+in_fs[xrand]+')('+f0+')('+f00+')^'+xr2+'/(('+f000+')('+f0000+'))','\\frac{'+in_fs_l[xrand]+'('+f0+')('+f00+')^'+xr2+'}{('+f000+')('+f0000+')}'
	elif q_id == 'Eight':
		if random.random()<.5:
			return get_question('One')
		else:
			return get_question('Five')
	elif q_id == 'Nine':
		if random.random()<.3:
			return get_question('Two')
		else:
			if random.random()<.4:
				return get_question('Three')
			else:
				return get_question('Six')
	elif q_id == 'Ten':
		if random.random()<.3:
			return get_question('Four')
		else:
			if random.random()<.35:
				return get_question('Six')
			else:
				return get_question('Seven')

class WorksheetForm(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter answer here.','size':'30','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))


def logarithmic_differentiation_worksheet(request):
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
		
	q_id = 'One'; gq = get_question(q_id)
	vsections = [{'title':'Logarithmic Differentiation of Powers','subsections':[{'title':'Basic','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'}]}]
	q_id = 'Two'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Functions as Exponents','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Three'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Functions as Base','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Four'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Functions Everywhere','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'})
	
	q_id = 'Five'; gq = get_question(q_id)
	vsections.append({'title':'Logarithmic Differentiation of Products','subsections':[{'title':'One Product','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'}]})
	q_id = 'Six'; gq = get_question(q_id)
	vsections[1]['subsections'].append({'title':'Multiple Products','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Seven'; gq = get_question(q_id)
	vsections[1]['subsections'].append({'title':'Quotients','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'})

	q_id = 'Eight'; gq = get_question(q_id)
	vsections.append({'title':'Lightning Round','subsections':[{'title':'Easy','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'}]})
	q_id = 'Nine'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Medium','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	q_id = 'Ten'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Hard','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'})
	
	num_subsections = 0
	for i in vsections:
		num_subsections = num_subsections+len(i['subsections'])
	frac_q = str(round(1./num_subsections,5))
	rcarr = [{'href':'logarithmic_differentiation_lesson.html','title':'Logarithmic Differentiation Lesson'},{'href':'product_rule_worksheet.html','title':'Product Rule Worksheet'},{'href':'chain_rule_worksheet.html','title':'Chain Rule Worksheet'},{'href':'#','title':'Chain Rule Video'},{'href':'#','title':'Chain Rule Explained'}]
	meta_title = 'Logarithmic Differentiation Worksheet - Learn Logarithmic Differentiation by working examples with Calculus College.'
	meta_des = "Infinitely many logarithmic differentiation problems with step-by-step solutions if you make a mistake. Progress through several types of problems that help you improve."
	return render(request,'base_worksheet.html',{'related_content':rcarr,'meta-des':meta_des,'title':meta_title,'header_1':'Chain Rule Worksheet','sections':vsections,'fraction_questions':frac_q})


