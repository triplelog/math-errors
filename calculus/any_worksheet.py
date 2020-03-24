import urllib.parse
from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from main import fullderivative_y
from sumrule import sumrule
from checkcorrect import checksame
from clean import cleanpar, post_clean, addpar
import uuid
import json
import sympy
import random
import time
from fractions import gcd
from django.utils.html import escape
from django.core.files import File
from wsgiref.util import FileWrapper
import subprocess

def myslatex(input_string):
	input_string = sympy.latex(input_string.replace('abs(x)','holdforit')).replace('holdfordydx','\\frac{dy}{dx}').replace('log{','ln{').replace('log^','ln^').replace('holdforit','|x|')
	return input_string
def slatex(f,dvar):
	try:
		return myslatex(sympy.sympify(f,evaluate=False))
	except:
		return myslatex(sympy.sympify(f))
def get_rand(t_list,t_dist):
	x = random.random()
	for i in range(0,len(t_list)):
		if x < sum(t_dist[0:i+1]):
			return t_list[i]
	return t_list[len(t_list)-1]


def get_rand_a(t_list,t_dist,avoid_n):
	x = random.random()
	for ii in range(0,100):
		for i in range(0,len(t_list)):
			if x < sum(t_dist[0:i+1]):
				if t_list[i]!=avoid_n:
					return t_list[i]
	return t_list[0]
def get_rand_poly(dvar,ntarr=[.4,.85,.975]):
	x = random.random()
	n_terms = 2
	h_power = 5
	if x < ntarr[0]:
		n_terms = 2
		h_power = get_rand(range(n_terms-1,n_terms+8),[.24,.22,.18,.13,.08,.04,.04,.04,.03])
	elif x < ntarr[1]:
		n_terms = 3
		h_power = get_rand(range(n_terms-1,n_terms+7),[.27,.245,.17,.125,.08,.04,.04,.03])
	elif x < ntarr[2]:
		n_terms = 4
		h_power = get_rand(range(n_terms-1,n_terms+6),[.24,.24,.18,.17,.1,.04,.03])
	else:
		n_terms = 5
		h_power = get_rand(range(n_terms-1,n_terms+5),[.24,.24,.175,.175,.12,.05])
	
	next_power = h_power
	exponents = [h_power]
	for i in range(0,n_terms-1):
		xf = round(1./(next_power-n_terms+2+i),2)
		ft = 1-xf*(next_power-n_terms+2+i)
		sp_list = [xf+ft]
		for ii in range(0,next_power-n_terms+1+i):
			sp_list.append(xf)
		s_power = get_rand(range(n_terms-2-i,next_power),sp_list)
		next_power = s_power
		exponents.append(next_power)
	h_coef = get_rand([1,2,-1,3,4,5,-2,-3,-4,-5,6,7,8,9,10,-6,11,12],[.5,.05,.05,.04,.04,.04,.04,.04,.03,.03,.03,.02,.02,.02,.02,.01,.01,.01])
	coeffs = [h_coef]
	for i in range(0,n_terms-1):
		next_coef = get_rand([1,2,-1,3,4,5,-2,-3,-4,-5,6,7,8,9,10,-6,11,12],[.25,.1,.1,.08,.08,.07,.08,.08,.06,.05,.05,.02,.02,.02,.02,.02,.02,.02])
		coeffs.append(next_coef)
	if exponents[0]==1:
		if coeffs[0]==-1:
			t_poly='-'+dvar
		elif coeffs[0]==1:
			t_poly=dvar
		else:
			t_poly = str(coeffs[0])+dvar
	else:
		if coeffs[0]==-1:
			t_poly='-'+dvar+'^'+str(exponents[0])
		elif coeffs[0]==1:
			t_poly=dvar+'^'+str(exponents[0])
		else:
			t_poly = str(coeffs[0])+dvar+'^'+str(exponents[0])
	for i in range(1,n_terms):
		if exponents[i]==1:
			if coeffs[i]<-1:
				t_poly=t_poly+str(coeffs[i])+dvar
			elif coeffs[i]==-1:
				t_poly=t_poly+'-'+dvar
			elif coeffs[i]==1:
				t_poly=t_poly+'+'+dvar
			else:
				t_poly=t_poly+'+'+str(coeffs[i])+dvar
		elif exponents[i]==0:
			if coeffs[i]<-1:
				t_poly=t_poly+str(coeffs[i])
			elif coeffs[i]==-1:
				t_poly=t_poly+'-1'
			elif coeffs[i]==1:
				t_poly=t_poly+'+1'
			else:
				t_poly=t_poly+'+'+str(coeffs[i])
		else:
			if coeffs[i]<-1:
				t_poly=t_poly+str(coeffs[i])+dvar+'^'+str(exponents[i])
			elif coeffs[i]==-1:
				t_poly=t_poly+'-'+dvar+'^'+str(exponents[i])
			elif coeffs[i]==1:
				t_poly=t_poly+'+'+dvar+'^'+str(exponents[i])
			else:
				t_poly=t_poly+'+'+str(coeffs[i])+dvar+'^'+str(exponents[i])
	return t_poly
	#return t_list[0]
class PrintableForm(forms.Form):
	CHOICES =[('1','Easy'),('2','Medium'),('3','Hard'),('4','Mixed')]
	your_diff = forms.ChoiceField(label='',widget=forms.RadioSelect(attrs={'class':'list_1'}),choices=CHOICES)
class WorksheetForm(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter answer here.','size':'30','onKeyPress':"checkSubmit(event)",'onKeyUp':"setTimeout(doLatex.bind(null,event,this.value),500)"}))

def any_printable(your_diff,title,questions):

	first_title= str(your_diff)
	f = open("testtemplate.tex", "r")
	f_to_write = str(f.read())
	f.close()
	f = open("static/worksheets/testtemplate1.tex","w")
	f_to_write = f_to_write.replace('{{ title }}',title)
	for i in range(0,12):
		f_to_write = f_to_write.replace('{{ q'+str(i+1)+' }}',questions[i])
	f.write(f_to_write)
	f.close()
	subprocess.call(['pdflatex','-output-directory','static/worksheets','testtemplate1.tex'])
	f = open("static/worksheets/testtemplate1.pdf", "rb")
	response = HttpResponse(FileWrapper(f),content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename='+title.replace(' ','_')+'.pdf'
	f.close()
	return response
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

				send_message = cleanpar(my_question,'x')
				t2 = time.time()
				ycount = []
				for i in range(0,38):
					ycount.append(0)
				fds = fullderivative_y(send_message,'x',ycount,'y')
				ycount = fds[1]
				ycount_int = ''
				for i in range(0,38):
					ycount_int = ycount_int+str(ycount[i])
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
					target.write(my_question+','+c_my_answer+','+c_fds+','+ycount_int+','+'N'+','+str(round(t2-t1,3))+','+str(round(t3-t2,3))+','+str(round(t4-t3,3))+'\n')
				else:
					target.write(my_question+','+c_my_answer+','+c_fds+','+ycount_int+','+'Y'+','+str(round(t2-t1,3))+','+str(round(t3-t2,3))+','+str(round(t4-t3,3))+'\n')
				target.close()

				send_message = {'message':message,'question_python':new_q[0],'question_latex':new_q[1],'my_q':my_question_l,'my_a':slatex(c_my_answer,'x'),'c_a':slatex(c_fds,'x'),'my_function':my_function}
			except:
				message = "Error reading answer: "+my_answer+". Try again."
				target = open('/home/django/data/'+sheet_name+'_ders_'+my_type+'.txt','a')
				my_target = File(target)
				target.write(my_question+','+my_answer+','+'error'+','+'error'+','+'E'+',-1,-1,-1\n')
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