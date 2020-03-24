from any_worksheet import *
from sumrule import sumrule

def solve_for_2d(my_question):
	c_my_q = cleanpar(my_question,'x')
	ycount = []
	for i in range(0,38):
		ycount.append(0)
	fdsl = fullderivative_y(c_my_q,'x',ycount,'y')
	ycount = fdsl[1]
	ycount_intl = ''
	for i in range(0,38):
		ycount_intl = ycount_intl+str(ycount[i])
	fdsl = fdsl[0]

	ycount = []
	for i in range(0,38):
		ycount.append(0)
	fdsr = fullderivative_y(fdsl,'x',ycount,'y')
	ycount = fdsr[1]
	ycount_intr = ''
	for i in range(0,38):
		ycount_intr = ycount_intr+str(ycount[i])
	fdsr = fdsr[0]

	return fdsr,ycount_intl,ycount_intr

def get_question(q_id):
	trig_fns = ['cos(x)','sin(x)','tan(x)','cot(x)','sec(x)','csc(x)']
	trig_fns_l = ['\cos{(x)}','\sin{(x)}','\\tan{(x)}','\cot{(x)}','\sec{(x)}','\csc{(x)}']
	inv_trigs = ['arccos(x)','arcsin(x)','arctan(x)','arccot(x)','arcsec(x)','arccsc(x)']
	polys = ['x^2+1','x^3+x-1','x+3','x^2-2x+3','x^5','x^4-x^2+x','2x^3','2x^2+x+1','x^3+5x^2-3x+2','2x-1']

	if q_id == 'One':
		q_1 = str(get_rand(range(2,11),[.25,.25,.15,.1,.05,.05,.05,.05,.05]))

		in_fs = [get_rand_poly('x'),get_rand_poly('x'),'ln(x)','e^x+'+str(random.randint(1,9)),get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])]
		x_r = random.randint(0,1)
		in_fn = in_fs[x_r]

		return ''+in_fn, ''+in_fn
	elif q_id == 'Two':
		q_1 = get_rand_poly('x')
		return ''+q_1, ''+q_1
	elif q_id == 'Three':
		q_1 = get_rand(trig_fns,[.25,.25,.15,.15,.1,.1])
		q_2 = get_rand_poly('x')
		q_1 = q_1.replace('x','y')
		return q_2,q_2
	elif q_id == 'Four':
		if random.random()<.3:
			return get_question('One')
		else:
			if random.random()<.4:
				return get_question('Three')
			else:
				return get_question('Two')
	elif q_id == 'Five':
		if random.random()<.3:
			return get_question('One')
		else:
			if random.random()<.6:
				return get_question('Two')
			else:
				return get_question('Three')

class WorksheetForm(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter answer here.','size':'30','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))
import traceback
def any_worksheet(form,sheet_name,new_q,my_type):
	send_message = 'something wrong!'
	if(form.is_valid()):
		new_data = form.cleaned_data['your_name'].replace('\\','||')
		send_message = json.loads(new_data)
		my_answer = addpar(escape(send_message['yn']))
		my_question = send_message['yq']

		if my_question != 'LATEX':
			try:
				t1 = time.time()
				my_question_l = send_message['yq_l'].replace('||','\\')
				my_type = send_message['yt']
				new_q = get_question(my_type)
				for i in range(0,10):
					if new_q[0]==my_question:
						new_q = get_question(my_type)
					else:
						break
				
				t2 = time.time()
				fds = solve_for_2d(my_question)
				ycount_intl = fds[1]
				ycount_intr = fds[2]
				fds = fds[0]

			
				t3 = time.time()
				c_my_answer = cleanpar(my_answer,'x')
				c_fds = cleanpar(fds,'x')
				if checksame(c_my_answer,c_fds,'x'):
					message=get_rand(["That's it!",'Got it!','Nailed it!','Right on!','Good job!','Way to go!','Nice!','Correct!','<i class="icon-ok"></i><i class="icon-ok"></i><i class="icon-ok"></i>','<i class="icon-smile"></i><i class="icon-smile"></i><i class="icon-smile"></i>'],[.1,.1,.1,.1,.1,.1,.1,.1,.1,.1])
				else:
					message= 'NO!'
				t4 = time.time()

				my_function= {'var':'x','q':my_question}
				my_function = urllib.parse.urlencode(my_function)
				target = open('/home/django/data/'+sheet_name+'_ders_'+my_type+'.txt','a')
				my_target = File(target)
				if message == 'NO!':
					target.write(my_question+','+c_my_answer+','+c_fds+','+ycount_intl+','+ycount_intr+','+'N'+','+str(round(t2-t1,3))+','+str(round(t3-t2,3))+','+str(round(t4-t3,3))+'\n')
				else:
					target.write(my_question+','+c_my_answer+','+c_fds+','+ycount_intl+','+ycount_intr+','+'Y'+','+str(round(t2-t1,3))+','+str(round(t3-t2,3))+','+str(round(t4-t3,3))+'\n')
				target.close()

				send_message = {'message':message,'equation_python':new_q[0],'equation_latex':new_q[1],'my_q':my_question_l,'my_a':slatex(c_my_answer,'x'),'c_a':slatex(c_fds,'x'),'my_function':my_function}
			except Exception as e:
				message = "Error reading answer: "+my_answer+". Try again."
				target = open('/home/django/data/'+sheet_name+'_ders_'+my_type+'.txt','a')
				my_target = File(target)
				target.write(my_question+','+my_answer+','+str(e)+','+'error'+','+'E'+',-1,-1,-1\n')
				target.close()
				send_message= {'message':message}
		else:
			try:
				message = slatex(cleanpar(addpar(my_answer),'x'),'x')
			except:
				try:
					if my_answer == '':
						message = ''
					else:
						message = '\\text{Preview unavailable...}'
				except:
					message = '\\text{Preview unavailable...}'

			send_message= {'message':message}

	return HttpResponse(json.dumps(send_message))

def second_derivative_worksheet(request):
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
					return any_worksheet(form,'imp_diff',new_q,my_type)
				except:
					pass
			return any_worksheet(form,'imp_diff','noq','Zero')
		
	q_id = 'One'; gq = get_question(q_id)
	vsections = [{'title':'Implicit Differentiation','subsections':[{'title':'Powers','id':q_id,'form':WorksheetForm(),'equation_python':gq[0],'equation_latex':gq[1],'classinit':'BB'}]}]
	q_id = 'Two'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Logarithms','id':q_id,'form':WorksheetForm(),'equation_python':gq[0],'equation_latex':gq[1],'classinit':'B'})
	q_id = 'Three'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Trigonometry','id':q_id,'form':WorksheetForm(),'equation_python':gq[0],'equation_latex':gq[1],'classinit':'B'})
	q_id = 'Four'; gq = get_question(q_id)
	vsections[0]['subsections'].append({'title':'Exponentials','id':q_id,'form':WorksheetForm(),'equation_python':gq[0],'equation_latex':gq[1],'classinit':'B'})
	
	q_id = 'Five'; gq = get_question(q_id)
	vsections.append({'title':'Advanced','subsections':[{'title':'Double Chain','id':q_id,'form':WorksheetForm(),'equation_python':gq[0],'equation_latex':gq[1],'classinit':'B'}]})

	num_subsections = 0
	for i in vsections:
		num_subsections = num_subsections+len(i['subsections'])
	frac_q = str(round(1./num_subsections,5))
	rcarr = [{'href':'second_derivative_lesson.html','title':'Second Derivative Lesson'},{'href':'product_rule_worksheet.html','title':'Product Rule Worksheet'},{'href':'quotient_rule_worksheet.html','title':'Quotient Rule Worksheet'},{'href':'#','title':'Chain Rule Video'},{'href':'#','title':'Chain Rule Explained'}]
	meta_title = 'Second Derivative Worksheet - Learn Second Derivatives by working examples with Calculus College.'
	meta_des = "Infinitely many second derivative problems with step-by-step solutions if you make a mistake. Progress through several types of problems that help you improve."
	return render(request,'base_worksheet_2d.html',{'related_content':rcarr,'meta-des':meta_des,'title':meta_title,'header_1':'Second Derivative Worksheet','sections':vsections,'fraction_questions':frac_q})


