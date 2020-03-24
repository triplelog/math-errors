from any_worksheet import *

def get_question(q_id):
	trig_fns = ['cos(x)','sin(x)','tan(x)','cot(x)','sec(x)','csc(x)']
	trig_fns_l = ['\cos{(x)}','\sin{(x)}','\\tan{(x)}','\cot{(x)}','\sec{(x)}','\csc{(x)}']
	inv_trigs = ['arccos(x)','arcsin(x)','arctan(x)','arccot(x)','arcsec(x)','arccsc(x)']
	inv_trigs_l = ['\\arccos(x)','\\arcsin(x)','\\tan^{-1}(x)','\\cot^{-1}(x)','\\sec^{-1}(x)','\\csc^{-1}(x)']
	polys = ['x^2+1','x^3+x-1','x+3','x^2-2x+3','x^5','x^4-x^2+x','2x^3','2x^2+x+1','x^3+5x^2-3x+2','2x-1']

	if q_id == 'One':
		x_r = get_rand_poly('x',[1,1,1])
		return x_r, x_r
	elif q_id == 'Two':
		f_1 = ['ln(x)','e^x',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])]
		f_2 = random.randint(0,2)
		f_0 = get_rand([-4,-3,-2,'-',2,3,4,5,6,7],[.1,.1,.1,.1,.1,.1,.1,.1,.1,.1])
		if f_2==1:
			if random.random()<.25:
				return str(f_0)+f_1[f_2],str(f_0)+f_1[f_2]
			else:
				if random.random()<.5:
					xint = str(random.randint(-5,-1))
					return str(f_0)+f_1[f_2]+xint,str(f_0)+f_1[f_2]+xint
				else:
					xpoly = get_rand_poly('x',[1,1,1])
					if xpoly[0]!='-':
						xpoly='+'+xpoly
					return str(f_0)+f_1[f_2]+xpoly,str(f_0)+f_1[f_2]+xpoly
		else:
			if random.random()<.25:
				return str(f_0)+f_1[f_2],str(f_0)+'\\'+f_1[f_2]
			else:
				if random.random()<.5:
					xint = '+'+str(random.randint(1,7))
					return str(f_0)+f_1[f_2]+xint,str(f_0)+'\\'+f_1[f_2]+xint
				else:
					xpoly = get_rand_poly('x',[1,1,1])
					if xpoly[0]!='-':
						xpoly='+'+xpoly
					return str(f_0)+f_1[f_2]+xpoly,str(f_0)+'\\'+f_1[f_2]+xpoly
	elif q_id == 'Three':
		if random.random()<.5:
			in_fs = ['ln(x)','e^x',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])]
			ch_x = random.randint(0,2)
			in_fn = in_fs[ch_x]
			xr =str(random.randint(2,9))
			if ch_x in [0,2]:
				return xr+'x('+in_fn+')',xr+'x\\'+in_fn
			else:
				return xr+'x('+in_fn+')',xr+'x'+in_fn
		else:
			in_fs = ['ln(x)','e^x',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])]
			ch_x = random.randint(0,2)
			in_fn = in_fs[ch_x]
			xr = str(random.randint(2,9))
			if ch_x in [0,2]:
				return xr+'x/('+in_fn+')','\\frac{'+xr+'x}{\\'+in_fn+'}'
			else:
				return xr+'x/('+in_fn+')','\\frac{'+xr+'x}{'+in_fn+'}'
	elif q_id == 'Four':
		if random.random()<.62:
			in_fn = get_rand_poly('x',[.8,1,1])
			f_1 = ['ln(x)','e^(x)',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1]),'(x)^2','(x)^3']
			f_2 = random.randint(0,4)
			f_3 = f_1[f_2]
			f_3 = f_3.replace('x',in_fn)
			f_r = str(random.randint(2,9))
			if f_2 in [0,2]:
				return f_r+f_3,f_r+'\\'+f_3
			elif f_2 in [3,4]:
				return f_r+f_3,f_r+f_3
			else:
				return f_r+f_3,f_r+f_3.replace('(','{').replace(')','}')
		else:
			in_fn = get_rand([0,1,2,3,4,5],[.25,.25,.15,.15,.1,.1])
			return inv_trigs[in_fn],inv_trigs_l[in_fn]

	elif q_id == 'Five':
		if random.random()<.4:
			f4 = get_question('Four')
			f2 = get_question('Two')
			f= '('+f2[0]+')('+f4[0]+')'
			if f4[1][0]!='\\':
				f_l = '('+f2[1]+')'+f4[1][1:]
			else:
				f_l = '('+f2[1]+')'+f4[1]
			return f, f_l
		else:
			if random.random()<.5:
				f4 = get_question('Four')
				f1 = get_question('One')
				f = f4[0]+'('+f1[0]+')'
				f_l = f4[1]+'('+f1[1]+')'
				return f,f_l
			else:
				f3 = get_question('Three')
				f1 = get_question('One')
				f = f3[0]+'('+f1[0]+')'
				f_l = f3[1]+'('+f1[1]+')'
				return f,f_l
	elif q_id == 'Six':
		if random.random()<.4:
			in_fn = get_question('Three')
			f_1 = ['ln(x)','e^(x)',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1]),'(x)^2','(x)^3']
			f_2 = random.randint(0,4)
			f_3 = f_1[f_2]
			f_3_n = f_3.replace('x',in_fn[0])
			f_r = str(random.randint(2,9))
			if f_2 in [0,2]:
				f_3_l = f_3.replace('x',in_fn[1])
				return f_r+f_3_n,f_r+'\\'+f_3_l
			elif f_2 in [3,4]:
				f_3_l = f_3.replace('x',in_fn[1])
				return f_r+f_3_n,f_r+f_3_l
			else:
				f_3_l = f_3.replace('(','{').replace(')','}').replace('x',in_fn[1])
				return f_r+f_3_n,f_r+f_3_l
		else:
			if random.random()<.5:
				f40=get_question('Four')
				f41=get_question('Four')
				if f41[1][0]!='\\':
					f=f40[0]+f41[0][1:]
					f_l = f40[1]+f41[1][1:]
					return f, f_l
				else:
					f=f40[0]+f41[0]
					f_l = f40[1]+f41[1]
					return f, f_l
			else:
				f30=get_question('Three')
				f41=get_question('Four')
				if f41[1][0]!='\\':
					f=f30[0]+f41[0][1:]
					f_l = f30[1]+f41[1][1:]
					return f, f_l
				else:
					f=f30[0]+f41[0]
					f_l = f30[1]+f41[1]
					return f, f_l

	elif q_id == 'Seven':
		if random.random()<.4:
			in_fn = get_question('Four')
			f_1 = ['ln(x)','e^(x)',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1]),'(x)^2','(x)^3']
			f_2 = random.randint(0,4)
			f_3 = f_1[f_2]
			f_3_n = f_3.replace('x',in_fn[0])
			f_r = str(random.randint(2,9))
			if f_2 in [0,2]:
				f_3_l = f_3.replace('x',in_fn[1])
				return f_r+f_3_n,f_r+'\\'+f_3_l
			elif f_2 in [3,4]:
				f_3_l = f_3.replace('x',in_fn[1])
				return f_r+f_3_n,f_r+f_3_l
			else:
				f_3_l = f_3.replace('(','{').replace(')','}').replace('x',in_fn[1])
				return f_r+f_3_n,f_r+f_3_l
		else:
			if random.random()<.5:
				in_fn = get_question('Three')
				f_1 = ['ln(x)','e^(x)',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1]),'(x)^2','(x)^3']
				f_2 = random.randint(0,4)
				f_3 = f_1[f_2]
				f_3_n = f_3.replace('x',in_fn[0])
				f_r = '('+get_rand_poly('x',[.8,1,1])+')'
				if f_2 in [0,2]:
					f_3_l = f_3.replace('x',in_fn[1])
					return f_r+f_3_n,f_r+'\\'+f_3_l
				elif f_2 in [3,4]:
					f_3_l = f_3.replace('x',in_fn[1])
					return f_r+f_3_n,f_r+f_3_l
				else:
					f_3_l = f_3.replace('(','{').replace(')','}').replace('x',in_fn[1])
					return f_r+f_3_n,f_r+f_3_l
			else:
				in_fn = get_question('Two')
				f_1 = ['ln(x)','e^(x)',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1]),'(x)^2','(x)^3']
				f_2 = random.randint(0,4)
				f_3 = f_1[f_2]
				f_3_n = f_3.replace('x',in_fn[0])
				xpro = get_question('Two')
				f_r = '('+xpro[0]+')'
				f_rl = '('+xpro[1]+')'
				if f_2 in [0,2]:
					f_3_l = f_3.replace('x',in_fn[1])
					return f_r+f_3_n,f_rl+'\\'+f_3_l
				elif f_2 in [3,4]:
					f_3_l = f_3.replace('x',in_fn[1])
					return f_r+f_3_n,f_rl+f_3_l
				else:
					f_3_l = f_3.replace('(','{').replace(')','}').replace('x',in_fn[1])
					return f_r+f_3_n,f_rl+f_3_l
	elif q_id == 'Eight':
		
		if random.random()<.5:
			f5 = get_question('Five')
			f55 = get_question('Five')
			return f5[0]+'+'+f55[0],f5[1]+'+'+f55[1]
		else:
			in_fn = get_rand([0,1,2,3,4,5],[.25,.25,.15,.15,.1,.1])
			f_1 = ['ln(x)','e^(x)',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1]),'(x)^2','(x)^3']
			f_2 = random.randint(0,4)
			f_3 = f_1[f_2]
			f_3_n = f_3.replace('x',inv_trigs[in_fn])
			f_r = str(random.randint(2,9))
			if f_2 in [0,2]:
				f_3_l = f_3.replace('x',inv_trigs_l[in_fn])
				return f_r+f_3_n,f_r+'\\'+f_3_l
			elif f_2 in [3,4]:
				f_3_l = f_3.replace('x',inv_trigs_l[in_fn])
				return f_r+f_3_n,f_r+f_3_l
			else:
				f_3_l = f_3.replace('(','{').replace(')','}').replace('x',inv_trigs_l[in_fn])
				return f_r+f_3_n,f_r+f_3_l
			return 
	elif q_id == 'Nine':
		if random.random()<.5:
			f5 = get_question('Five')
			f55 = get_question('Five')
			return f5[0]+'+'+f55[0],f5[1]+'+'+f55[1]
		else:
			out_fn = get_rand([0,1,2,3,4,5],[.25,.25,.15,.15,.1,.1])
			f_1 = ['ln(x)','e^x',get_rand_poly('x',[1,1,1])]
			f_2 = random.randint(0,2)
			f_3 = f_1[f_2]
			in_fn = f_3
			f = inv_trigs[out_fn].replace('x',in_fn)
			if f_2 in [0]:
				in_fn_l = '\ln(x)'
				f_l = inv_trigs_l[out_fn].replace('x',in_fn_l)
				return f,f_l
			elif f_2 in [1]:
				in_fn_l = f_3
				f_l = inv_trigs_l[out_fn].replace('x',in_fn_l)
				return f,f_l
			else:
				in_fn_l = f_3
				f_l = inv_trigs_l[out_fn].replace('x',in_fn_l)
				return f,f_l
	elif q_id == 'Ten':
		if random.random()<.3:
			in_fn = get_question('Four')
			f_1 = ['ln(x)','e^(x)',get_rand(trig_fns,[.25,.25,.15,.15,.1,.1]),'(x)^2','(x)^3']
			f_2 = random.randint(0,4)
			f_3 = f_1[f_2]
			f_3_n = f_3.replace('x',in_fn[0])
			if f_2 in [0,2]:
				f_3_l = f_3.replace('x',in_fn[1])
				inside = [f_3_n,'\\'+f_3_l]
				f_0 = random.randint(0,4)
				f = f_1[f_0].replace('x',inside[0])
				if f_0 in [0,2]:
					f_l = '\\'+f_1[f_0].replace('x',inside[1])
				elif f_0 in [3,4]:
					f_l = f_1[f_0].replace('x',inside[1])
				else:
					f_l = f_1[f_0].replace('(','{').replace(')','}').replace('x',inside[1])
			elif f_2 in [3,4]:
				f_3_l = f_3.replace('x',in_fn[1])
				inside = [f_3_n,f_3_l]
				f_0 = random.randint(0,2)
				f = f_1[f_0].replace('x',inside[0])
				if f_0 in [0,2]:
					f_l = '\\'+f_1[f_0].replace('x',inside[1])
				elif f_0 in [3,4]:
					f_l = f_1[f_0].replace('x',inside[1])
				else:
					f_l = f_1[f_0].replace('(','{').replace(')','}').replace('x',inside[1])
			else:
				f_3_l = f_3.replace('(','{').replace(')','}').replace('x',in_fn[1])
				inside = [f_3_n,f_3_l]
				f_0 = random.randint(1,4)
				f = f_1[f_0].replace('x',inside[0])
				if f_0 in [0,2]:
					f_l = '\\'+f_1[f_0].replace('x',inside[1])
				elif f_0 in [3,4]:
					f_l = f_1[f_0].replace('x',inside[1])
				else:
					f_l = f_1[f_0].replace('(','{').replace(')','}').replace('x',inside[1])
			return f,f_l

		else:
			if random.random()<.35:
				gq8 = get_question('Eight')
				gq9 = get_question('Nine')
				return gq8[0]+'+'+gq9[0],gq8[1]+'+'+gq9[1]
			else:
				gq8 = get_question('Eight')
				gq7 = get_question('Seven')
				return gq8[0]+'-'+gq7[0],gq8[1]+'-'+gq7[1]

class WorksheetForm(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter answer here.','size':'30','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))


def all_derivatives_worksheet(request):
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
					return any_worksheet(form,'any',new_q,my_type)
				except:
					pass
			return any_worksheet(form,'any','noq','Zero')
		else:
			form = PrintableForm(request.POST)
			if (form.is_valid()):
				your_diff = form.cleaned_data['your_diff']
				title = 'All Derivatives Worksheet'
				questions = []
				questions.append(get_question('One')[1])
				questions.append(get_question('Two')[1])
				questions.append(get_question('Three')[1])
				questions.append(get_question('Four')[1])
				questions.append(get_question('Five')[1])
				questions.append(get_question('Six')[1])
				questions.append(get_question('Five')[1])
				questions.append(get_question('Six')[1])
				questions.append(get_question('Seven')[1])
				questions.append(get_question('Eight')[1])
				questions.append(get_question('Nine')[1])
				questions.append(get_question('Ten')[1])
				return any_printable(your_diff,title,questions)
		
	q_id = 'One'; gq = get_question(q_id)
	vsections = [{'title':'Normal','subsections':[{'title':'Level 1','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BB'}]}]
	q_id = 'Two'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Level 2','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'})
	q_id = 'Three'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Level 3','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'})
	q_id = 'Four'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Level 4','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'BBB'})
	
	q_id = 'Five'; gq = get_question(q_id)
	vsections.append({'title':'Hard','subsections':[{'title':'Level 5','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'}]})
	q_id = 'Six'; gq = get_question(q_id)
	vsections[1]['subsections'].append({'title':'Level 6','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'})
	q_id = 'Seven'; gq = get_question(q_id)
	vsections[1]['subsections'].append({'title':'Level 7','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'})

	q_id = 'Eight'; gq = get_question(q_id)
	vsections.append({'title':'Diabolical','subsections':[{'title':'Level 8','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'}]})
	q_id = 'Nine'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Level 9','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'})
	q_id = 'Ten'; gq = get_question(q_id)
	vsections[2]['subsections'].append({'title':'Level 10','id':q_id,'form':WorksheetForm(),'question_python':gq[0],'question_latex':gq[1],'classinit':'B'})
	
	num_subsections = 0
	for i in vsections:
		num_subsections = num_subsections+len(i['subsections'])
	frac_q = str(round(1./num_subsections,5))
	rcarr = [{'href':'how_to_take_derivatives_lesson.html','title':'How to take Derivatives Lesson'},{'href':'product_rule_worksheet.html','title':'Product Rule Worksheet'},{'href':'chain_rule_worksheet.html','title':'Chain Rule Worksheet'},{'href':'#','title':'Chain Rule Video'},{'href':'#','title':'Chain Rule Explained'}]
	meta_title = 'All Derivatives Worksheet - Learn Differentiation by working examples with Calculus College.'
	meta_des = "Infinitely many differentiation problems with step-by-step solutions if you make a mistake. Progress through several types of problems that help you improve."
	return render(request,'base_worksheet.html',{'pform':PrintableForm(),'related_content':rcarr,'meta-des':meta_des,'title':meta_title,'header_1':'All Derivatives Worksheet','sections':vsections,'fraction_questions':frac_q})


