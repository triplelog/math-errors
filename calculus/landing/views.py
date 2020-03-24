import json
from clean import cleanpar, addpar
import sympy
def myslatex(input_string):
	input_string = sympy.latex(input_string).replace('holdfordydx','\\frac{dy}{dx}').replace('log{','ln{').replace('log^','ln^')
	return input_string
def slatex(f,dvar):
	return myslatex(sympy.sympify(f.replace('e^','exp(1)^'),evaluate=False))
def cleandecimal(inputval,maxd):
	rval = str(round(inputval,maxd))
	while rval.find('.') > -1 and (rval[-1] == '0' or rval[-1] == '.'):
		rval=rval[:-1]
	return rval
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
#from account.utils import user_display
from django.http import HttpResponseRedirect
from django.http import JsonResponse

from .forms import NameForm, NameForm1, HomeForm, TrigForm, DerivForm, RiemannForm, NewtonForm, TangentForm, IntegralForm, WrongDForm, SignupForm, LoginForm
from main import index_fn
from mainw import index_fn_w
import mainIntegral


from django.utils.html import escape
import psycopg2
import main
import uuid
import urllib.parse
import time
from django.core.files import File

from lessons.power_rule_worksheet import *
from lessons.product_rule_worksheet import *
from lessons.chain_rule_worksheet import *
from lessons.sum_rule_worksheet import *
from lessons.quotient_rule_worksheet import *
from lessons.exponentials_logarithms_worksheet import *
from lessons.trigonometric_functions_worksheet import *
from lessons.logarithmic_differentiation_worksheet import *
from lessons.all_derivatives_worksheet import *

from lessons.implicit_differentiation_worksheet import *
from lessons.increasing_decreasing_worksheet import *
from lessons.second_derivative_worksheet import *
from lessons.optimization_worksheet import *
from lessons.related_rates_worksheet import *

from lessons.power_rule_lesson import *
from lessons.chain_rule_lesson import *
from lessons.how_to_differentiate_lesson import *
from lessons.sum_rule_lesson import *
from lessons.exponentials_logarithms_lesson import *
from lessons.product_rule_lesson import *
from lessons.quotient_rule_lesson import *
from lessons.logarithmic_differentiation_lesson import *
from lessons.trigonometric_functions_lesson import *
from lessons.what_are_derivatives_lesson import *

from lessons.power_rule_integral_lesson import *
from lessons.how_to_integrate_lesson import *
from lessons.sum_rule_integral_lesson import *
from lessons.exponentials_integral_lesson import *
from lessons.trigonometric_functions_integral_lesson import *
from lessons.what_are_integrals_lesson import *
from lessons.integration_by_parts_lesson import *
from lessons.u_substitution_lesson import *
from lessons.definite_integrals_lesson import *
from lessons.partial_fractions_lesson import *

from lessons.more_derivatives_lesson import *

import riemannlatex
import tangentlatex
import triglatex
import newtonlatex
import relatedlatex
#from djangosecure.decorators import frame_deny_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

import stripe
stripe.api_key = settings.STRIPE_PRIVATE_KEY


def home_page(request):
	return render(request,'index.html',{'message':'Hello'})

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			my_email = form.cleaned_data['your_email']
			my_pword = form.cleaned_data['your_password']
			conf_pword = form.cleaned_data['conf_password']
			if User.objects.filter(username=my_email).exists():
				return render(request,'account/signup.html',{'form':SignupForm(),'paymentTime':False})
			if my_pword == conf_pword:
				context = { 'form':SignupForm({'your_email': my_email, 'your_password': 'password', 'conf_password': 'password'}),'paymentTime':True,"stripe_key": settings.STRIPE_PUBLIC_KEY,'userEmail':my_email }
				User.objects.create_user(my_email, my_email, my_pword)
				return render(request,'account/signup.html',context)
				#
				#return redirect('charge.html')
	form = SignupForm()
	context = { 'form':form,'paymentTime':False }
	return render(request,'account/signup.html',context)

def login_page(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = LoginForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			my_email = form.cleaned_data['your_email']
			my_pword = form.cleaned_data['your_password']
			user = authenticate(username=my_email, password=my_pword)
			if user is not None:
				login(request, user)
				return redirect('videoIndex.html')
	form = LoginForm()
	return render(request,'account/login.html',{'form':form})

def charge_page(request):
	if request.method == 'POST':
		charge = stripe.Charge.create(
			amount=500,
			currency='usd',
			description='6 months of Premium',
			source=request.POST['stripeToken']
		)
		return render(request, 'account/charge.html')

def apiDerivative(request):
	my_function = request.GET.get('q','')
	if my_function != '':
		try:
			fn_sym = sympy.sympify(cleanpar(my_function,'x').replace('e^','exp(1)^'),evaluate=False)
			fn_latex = myslatex(fn_sym)
			dfn_latex = myslatex(sympy.diff(fn_sym))
			full_latex = '\\displaystyle\\frac{d}{dx}['+fn_latex+']='+dfn_latex
		except:
			fn_latex = ''
			dfn_latex = ''
			full_latex = ''
	response = HttpResponse(content_type="text/html")
	response.write(full_latex)
	return response

def apiIntegral(request):
	my_function = request.GET.get('q','')
	if my_function != '':
		try:
			fn_sym = sympy.sympify(cleanpar(my_function,'x').replace('e^','exp(1)^'),evaluate=False)
			fn_latex = myslatex(fn_sym)
			ifn_latex = myslatex(sympy.integrate(fn_sym))
			full_latex = '\\displaystyle\\int '+fn_latex+'dx ='+ifn_latex+'+C'
		except:
			full_latex = ''
	response = HttpResponse(content_type="text/html")
	response.write(full_latex)
	return response

def apiTangent(request):
	my_function = request.GET.get('q','')
	
	if my_function != '':
		try:
			x = sympy.symbols('x')
			try:
				x0 = float(request.GET.get('x',''))
			except:
				x0 = sympy.sympify(request.GET.get('x','').replace('e','exp(1)'))
			fn_sym = sympy.sympify(cleanpar(my_function,'x').replace('e^','exp(1)^'))
			y0_latex = fn_sym.evalf(subs={x:x0})
			m_latex = sympy.diff(fn_sym).evalf(subs={x:x0})
			try:
				x0 = cleandecimal(x0,4)
			except:
				x0 = myslatex(x0)
			try:
				m_latex = cleandecimal(m_latex,4)
			except:
				m_latex = myslatex(m_latex)
			try:
				y0_latex = cleandecimal(y0_latex,4)
			except:
				y0_latex = myslatex(y0_latex)

			full_latex = 'y='+m_latex+'(x-'+x0+')+'+y0_latex
			full_latex = full_latex.replace('+-','-').replace('--','+')
		except:
			full_latex = ''
	response = HttpResponse(content_type="text/html")
	response.write(full_latex)
	return response

def apiNewton(request):
	my_function = request.GET.get('q','')
	
	if my_function != '':
		try:
			x = sympy.symbols('x')
			try:
				x0 = float(request.GET.get('x',''))
			except:
				x0 = float(request.GET.get('x','').replace('e','2.7182818284590452353').replace('pi','3.14159265358979'))
			fn_sym = sympy.sympify(cleanpar(my_function,'x').replace('e^','2.7182818284590452353^').replace('pi','3.14159265358979'))
			dfn_sym = sympy.diff(fn_sym)

			for i in range(0,10):
				x1=x0-fn_sym.evalf(subs={x:x0})/dfn_sym.evalf(subs={x:x0})
				if cleandecimal(x1,6)==cleandecimal(x0,6):
					break
				else:
					x0 = x1

	
			full_latex = myslatex(sympy.sympify(cleanpar(my_function,'x').replace('e^','exp(1)^')))+'=0 \\text{ when } '+'x\\approx '+cleandecimal(x1,6)
		except:
			full_latex = ''
	response = HttpResponse(content_type="text/html")
	response.write(full_latex)
	return response

def apiRiemann(request):
	response = HttpResponse(content_type="text/html")
	

	try:
		x = sympy.symbols('x')
		notfull = False
		try:
			try:
				a = float(request.GET.get('a',''))
				if a.is_integer():
					a = int(a)
			except:
				a = sympy.sympify(request.GET.get('a','').replace('e','exp(1)'))
			
		except:
			a = ''
			notfull = True

		try:
			try:
				b = float(request.GET.get('b',''))
				if b.is_integer():
					b = int(b)
			except:
				b = sympy.sympify(request.GET.get('b','').replace('e','exp(1)'))
			
		except:
			b = ''
			notfull = True

		try:
			n = int(request.GET.get('n',''))
			if n == 0:
				notfull = True
		except:
			n = ''
			notfull = True

		try:
			rtype = request.GET.get('r','')
			if rtype == '':
				notfull = True
		except:
			rtype = ''
			notfull = True

		try:
			my_function = request.GET.get('q','')
			if my_function == '':
				notfull = True
		except:
			my_function = ''
			notfull = True

		if notfull:
			if my_function != '':
				fn_sym = sympy.sympify(cleanpar(my_function,'x').replace('e^','exp(1)^'))
				int_latex = '\\displaystyle\\int_{'+myslatex(sympy.sympify(a))+'}^{'+myslatex(sympy.sympify(b))+'}'+myslatex(fn_sym)+'dx\\approx'
			else:
				int_latex = '\\displaystyle\\int_{'+myslatex(sympy.sympify(a))+'}^{'+myslatex(sympy.sympify(b))+'} dx\\approx'
			
			heights = []
			fnheights = []
		else:
			
			fn_sym = sympy.sympify(cleanpar(my_function,'x').replace('e^','exp(1)^'))

			w = (b-a)*1.0/n

			rshift = 0.0
			if rtype[0] == 'R' or rtype[0] =='r':
				rshift = w
			elif rtype[0] == 'M' or rtype[0] =='m':
				rshift = w/2
			try:
				if w.is_integer():
					w = int(w)
			except:
				pass
			try:
				if rshift.is_integer():
					rshift = int(rshift)
			except:
				pass
			

			heights = []
			rsum = 0
			for i in range(0,n):
				hval = fn_sym.evalf(subs={x:a+rshift+i*w})
				heights.append(hval)
				rsum += hval*w
			int_latex = '\\displaystyle\\int_{'+myslatex(sympy.sympify(a))+'}^{'+myslatex(sympy.sympify(b))+'}'+myslatex(fn_sym)+'dx\\approx'+myslatex(sympy.sympify(rsum))

			fnheights = []
			for i in range(0,n*10+1):
				hval = fn_sym.evalf(subs={x:a+i*w*1.0/10})
				fnheights.append(hval)

	except:
		heights = []
		int_latex = ''
		fnheights = []

	
	response.write(heights)
	response.write('|')
	response.write(int_latex)
	response.write('|')
	response.write(fnheights)
	return response

def videoIndex(request):
	#User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
	#user = authenticate(username='john', password='johnpassword')
	my_function = request.GET.get('q','')
	#if user is not None:
	#	login(request, user)
	#	return render(request,'index-mustard.html',{'videoUrl':my_function,'form1':''})
	#else:
	form1 = DerivForm()
	form2 = IntegralForm()
	form3 = RiemannForm()
	form4 = TangentForm()
	form5 = NewtonForm()
	form6 = TrigForm()
	return render(request,'index-mustard.html',{'videoUrl':my_function,'form1':form1,'form2':form2,'form3':form3,'form4':form4,'form5':form5,'form6':form6})

def derivative_calculator(request):
	working = "Hello World!"
	images = []
	audios = []
	ycount = '0'
	full_derivative = ''
	ofunction = 'f(x)'
	is_derivative = False
	is_error = False
	my_function=''
	dvar = 'x'
	#if request.method == 'GET':
	dvar = request.GET.get('var','x')
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = NameForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			my_function = form.cleaned_data['your_name']
			try:
				send_message = json.loads(my_function)
				my_f = escape(send_message['yn'])
				try:
					message = slatex(cleanpar(addpar(my_f),'x'),'x')
				except:
					try:
						if my_f == '':
							message = ''
						else:
							message = '\\text{???}'
					except:
						message = '\\text{???}'

				send_message= {'message':message}
				return HttpResponse(json.dumps(send_message))
			except:
				try:
					my_function = escape(my_function)
					full_derivative, ofunction,ycount,f_d = index_fn(addpar(my_function),dvar,'y')
					my_function= {'var':dvar,'q':addpar(my_function)}

					target = open('/home/django/data/function.txt','a')
					my_target = File(target)
					target.write(my_function['q']+','+f_d+','+ycount+'\n')
					target.close()
					

					my_function = urllib.parse.urlencode(my_function)
					#hashprefix = str(uuid.uuid4())
					
					#for i in range(0,n_pics):
					#	images.append(hashprefix+'ex'+str(i)+'.png')
					#	audios.append(hashprefix+'ex'+str(i)+'.mp3')
					#working=str(n_pics)
					is_derivative = True
				except:
					is_error = True


	# if a GET (or any other method) we'll create a blank form
	else:
		form = NameForm()
	return render(request,'derivative_calculator.html',{'my_function':my_function,'working':working,'form': form,'images':images,'ofunction':ofunction,'full_derivative':full_derivative,'ycount':ycount,'audios':audios,'is_derivative':is_derivative,'is_error':is_error})

def integral_calculator(request):
	working = "Hello World!"
	images = []
	audios = []
	ycount = '0'
	full_derivative = ''
	ofunction = 'f(x)'
	is_derivative = False
	is_error = False
	my_function=''
	dvar = 'x'
	#if request.method == 'GET':
	#dvar = request.GET.get('var','x')
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = NameForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			my_function = form.cleaned_data['your_name']
			try:
				send_message = json.loads(my_function)
				my_f = escape(send_message['yn'])
				try:
					message = slatex(cleanpar(addpar(my_f),'x'),'x')
				except:
					try:
						if my_f == '':
							message = ''
						else:
							message = '\\text{???}'
					except:
						message = '\\text{???}'

				send_message= {'message':message}
				return HttpResponse(json.dumps(send_message))
			except:
				try:
					my_function = escape(my_function)
					full_derivative, ofunction,ycount,f_d = mainIntegral.index_fn(addpar(my_function),dvar)
					mainIntegral.run_it()
					my_function= {'var':dvar,'q':addpar(my_function)}

					target = open('/home/django/data/function.txt','a')
					my_target = File(target)
					target.write(my_function['q']+','+f_d+','+str(ycount)+'\n')
					target.close()
					

					my_function = urllib.parse.urlencode(my_function)
					#hashprefix = str(uuid.uuid4())
					
					#for i in range(0,n_pics):
					#	images.append(hashprefix+'ex'+str(i)+'.png')
					#	audios.append(hashprefix+'ex'+str(i)+'.mp3')
					#working=str(n_pics)
					is_derivative = True
				except:
					is_error = True


	# if a GET (or any other method) we'll create a blank form
	else:
		form = NameForm()
	return render(request,'integral_calculator.html',{'my_function':my_function,'working':working,'form': form,'images':images,'ofunction':ofunction,'full_derivative':full_derivative,'ycount':ycount,'audios':audios,'is_derivative':is_derivative,'is_error':is_error})


def wrong(request):
	working = "Hello World!"
	images = []
	audios = []
	full_derivative = ''
	ofunction = 'f(x)'
	is_derivative = False
	my_function=''
	error='none'
	dvar = 'x'
	#if request.method == 'GET':
	dvar = request.GET.get('var','x')
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = NameForm1(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			my_function = form.cleaned_data['your_fn']
			my_guess = form.cleaned_data['your_guess']
			full_derivative, ofunction,ycount,f_d = index_fn(my_function,dvar,'y')
			error = index_fn_w(my_function,dvar,'y', my_guess)
			my_function= {'var':dvar,'q':my_function}
			my_function = urllib.parse.urlencode(my_function)
			#hashprefix = str(uuid.uuid4())
			
			#for i in range(0,n_pics):
			#	images.append(hashprefix+'ex'+str(i)+'.png')
			#	audios.append(hashprefix+'ex'+str(i)+'.mp3')
			#working=str(n_pics)
			is_derivative = True

	# if a GET (or any other method) we'll create a blank form
	else:
		form = NameForm1()
	return render(request,'index2.html',{'error':error,'my_function':my_function,'working':working,'form': form,'images':images,'ofunction':ofunction,'full_derivative':full_derivative,'audios':audios,'is_derivative':is_derivative})


def worksheets(request):
	functions = []
	ii = 1
	for n_pics, my_function  in [[17, '-2x^3+3x^2'], [6, '3x^(-2)'], [18, '5(x+1)^(1/3)'], [15, 'x^2+5x-11'], [25, '2x^6+4x^3-3x+5'], [13, 'x^5+5/x'], [18, '2sin(x^2+1)'], [8, 'ln(x)+1/x'], [15, 'xln(x)-x'], [8, 'e^x+x^e'], [13, 'e^(x^3+1)'], [8, 'cos(x)/x']]:
		images = []
		audios = []
		full_derivative = ''
		ofunction = 'f(x)'
		is_derivative = False

		full_derivative, ofunction = index_fn(my_function,'x','y')
		modal_header = 'f(x)='+ofunction
		for i in range(0,n_pics+1):
			images.append('worksheet1/f'+str(ii)+'ex'+str(i)+'.png')
			#audios.append(hashprefix+'ex'+str(i)+'.mp3')
			#audios.append('blank.mp3')
		working=str(n_pics+1)
		is_derivative = True
		functions.append({'id':str(ii),'modal_header':modal_header,'images':images,'ofunction':modal_header,'full_derivative':full_derivative,'audios':audios})
		ii=ii+1
	return render(request,'worksheets.html',{'functions':functions,'is_derivative':is_derivative})

@xframe_options_exempt
def swipe(request):
	working = "Hello World!"
	images = []
	audios = []
	full_derivative = ''
	ofunction = 'f(x)'
	is_derivative = False
	my_function = request.GET.get('q','')
	dvar = 'x'
	dvar = request.GET.get('var','')
	hashprefix = str(uuid.uuid4())
	n_pics, full_derivative,ofunction,stepinfo = main.run_it(my_function,hashprefix,dvar,'yyyyy',False)
	
	for i in range(0,n_pics):
		images.append(hashprefix+'ex'+str(i)+'.png')
		audios.append('blank.mp3')
	working=str(n_pics)
	is_derivative = True

	return render(request,'swipe.html',{'working':working,'images':images,'ofunction':ofunction,'full_derivative':full_derivative,'audios':audios,'is_derivative':is_derivative,'stepinfo':stepinfo})

@xframe_options_exempt
def swipeIntegral(request):
	working = "Hello World!"
	images = []
	audios = []
	full_derivative = ''
	ofunction = 'f(x)'
	is_derivative = False
	my_function = request.GET.get('q','')
	dvar = 'x'
	dvar = request.GET.get('var','')
	hashprefix = str(uuid.uuid4())
	full_derivative, dparts = mainIntegral.fullintegral(my_function,'x',0,0,0)
	
	is_derivative = True

	return render(request,'swipeIntegral.html',{'working':working,'images':images,'ofunction':ofunction,'full_derivative':full_derivative,'audios':audios,'is_derivative':is_derivative})

@xframe_options_exempt
def videoDerivative(request):
	working = "Hello World!"
	images = []
	audios = []
	full_derivative = ''
	ofunction = 'f(x)'
	is_derivative = False
	my_function = request.GET.get('der_fn','')
	dvar = 'x'
	dvar = request.GET.get('var','x')
	hashprefix = str(uuid.uuid4())
	videoURL, colors = main.run_it(my_function,hashprefix,dvar,'yyyyy',True)
	
	#for i in range(0,n_pics):
	#	images.append(hashprefix+'ex'+str(i)+'.png')
	#	audios.append('blank.mp3')
	#working=str(n_pics)
	#is_derivative = True

	return render(request,'videoRiemann.html',{'videoURL':'media/'+videoURL,'videoJS':colors})

@xframe_options_exempt
def videoRiemann(request):
	my_function = request.GET.get('rie_fn','')
	a = sympy.sympify(request.GET.get('rie_a',''))
	b = sympy.sympify(request.GET.get('rie_b',''))
	n = int(request.GET.get('rie_n',''))
	rtype = request.GET.get('rie_r','')

	#if a.is_integer():
	#	a = int(a)
	alatex = myslatex(a)
	blatex = myslatex(b)
	a = float(a)
	if a.is_integer():
		a = int(a)
	b = float(b)
	if b.is_integer():
		b = int(b)

	if rtype[0] == 'r' or rtype[0] == 'R':
		rtype = 'RRAM'
	if rtype[0] == 'm' or rtype[0] == 'M':
		rtype = 'MRAM'
	if rtype[0] == 'l' or rtype[0] == 'L':
		rtype = 'LRAM'
	hashprefix = str(uuid.uuid4())
	videoURL,colors, subtitlesURL = riemannlatex.run_it(my_function,hashprefix,a,b,n,rtype,alatex,blatex)

	return render(request,'videoRiemann.html',{'videoURL':'media/'+videoURL,'videoJS':colors,'subtitlesURL':'media/'+subtitlesURL})

@xframe_options_exempt
def videoTangent(request):
	my_function = request.GET.get('tan_fn','')
	x0 = float(request.GET.get('tan_x',''))
	hashprefix = str(uuid.uuid4())
	videoURL,colors, subtitlesURL = tangentlatex.run_it(my_function,x0,hashprefix)

	return render(request,'videoRiemann.html',{'videoURL':'media/'+videoURL,'videoJS':colors,'subtitlesURL':'media/'+subtitlesURL})

@xframe_options_exempt
def videoTrig(request):
	my_function = request.GET.get('trig_fn','')
	hashprefix = str(uuid.uuid4())
	videoURL, colors, subtitlesURL = triglatex.run_it(my_function,hashprefix)
	return render(request,'videoRiemann.html',{'videoURL':'media/'+videoURL,'videoJS':colors,'subtitlesURL':'media/'+subtitlesURL})

	

@xframe_options_exempt
def videoNewton(request):
	my_function = request.GET.get('new_fn','')
	x0 = float(request.GET.get('new_x',''))
	hashprefix = str(uuid.uuid4())
	videoURL, colors = newtonlatex.run_it(my_function,float(x0),hashprefix)

	return render(request,'videoRiemann.html',{'videoURL':'media/'+videoURL,'videoJS':colors})

@xframe_options_exempt
def videoIntegral(request):
	my_function = request.GET.get('int_fn','')
	hashprefix = str(uuid.uuid4())
	videoURL,colors, subtitlesURL = mainIntegral.run_it(my_function,hashprefix)
	return render(request,'videoRiemann.html',{'videoURL':'media/'+videoURL,'videoJS':colors,'subtitlesURL':'media/'+subtitlesURL})

@xframe_options_exempt
def videoRelated(request):
	hashprefix = str(uuid.uuid4())
	videoURL,colors, subtitlesURL = relatedlatex.run_it(hashprefix)
	return render(request,'videoRiemann.html',{'videoURL':'media/'+videoURL,'videoJS':colors,'subtitlesURL':'media/'+subtitlesURL})

@xframe_options_exempt
def videoSearch(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = TrigForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			my_function = form.cleaned_data['trig_fn']
			if my_function is not None:
				if not request.user.is_authenticated:
					hashprefix = str(uuid.uuid4())
				else:
					hashprefix = 'logged'
				videoURL, colors, subtitlesURL = triglatex.run_it(my_function,hashprefix)
				return render(request,'videoRiemann.html',{'videoURL':'media/'+videoURL,'videoJS':colors,'subtitlesURL':'media/'+subtitlesURL})

	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = RiemannForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			my_function = form.cleaned_data['rie_fn']
			if my_function is not None:
				hashprefix = str(uuid.uuid4())
				a = form.cleaned_data['rie_a']
				b = form.cleaned_data['rie_b']
				n = form.cleaned_data['rie_n']
				rtype = form.cleaned_data['rie_r']

				a = float(a)
				b = float(b)
				n = int(n)
				if rtype != 'RRAM' and rtype != 'MRAM':
					rtype = 'LRAM'
				videoURL,colors, subtitlesURL = riemannlatex.run_it(my_function,hashprefix,a,b,n,rtype)

				return render(request,'videoRiemann.html',{'videoURL':'media/'+videoURL,'videoJS':colors,'subtitlesURL':'media/'+subtitlesURL})
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = TangentForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			my_function = form.cleaned_data['tan_fn']
			if my_function is not None:
				hashprefix = str(uuid.uuid4())
				x0 = form.cleaned_data['tan_x']
				x0 = float(x0)
				#if x0.is_integer():
				#	x0 = int(x0)
				hashprefix = str(uuid.uuid4())
				videoURL,colors, subtitlesURL = tangentlatex.run_it(my_function,x0,hashprefix)

				return render(request,'videoRiemann.html',{'videoURL':'media/'+videoURL,'videoJS':colors,'subtitlesURL':'media/'+subtitlesURL})
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = NewtonForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			my_function = form.cleaned_data['new_fn']
			if my_function is not None:
				hashprefix = str(uuid.uuid4())
				x0 = form.cleaned_data['new_x']
				x0 = float(x0)
				#if x0.is_integer():
				#	x0 = int(x0)
				hashprefix = str(uuid.uuid4())
				videoURL,colors = newtonlatex.run_it(my_function,x0,hashprefix)

				return render(request,'videoRiemann.html',{'videoURL':'media/'+videoURL,'videoJS':colors})
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = IntegralForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			my_function = form.cleaned_data['int_fn']
			if my_function is not None:
				hashprefix = str(uuid.uuid4())
				videoURL,colors, subtitlesURL = mainIntegral.run_it(my_function,hashprefix)

				return render(request,'videoRiemann.html',{'videoURL':'media/'+videoURL,'videoJS':colors,'subtitlesURL':'media/'+subtitlesURL})
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = DerivForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			my_function = form.cleaned_data['der_fn']
			if my_function is not None:
				hashprefix = str(uuid.uuid4())
				videoURL,colors = main.run_it(my_function,hashprefix,'x','yyyyy',True)

				return render(request,'videoRiemann.html',{'videoURL':'media/'+videoURL,'videoJS':colors})
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = WrongDForm(request.POST)
		# check whether it's valid:
		if form.is_valid():	
			working = "Hello World!"
			images = []
			audios = []
			full_derivative = ''
			ofunction = 'f(x)'
			is_derivative = False
			my_function=''
			error='none'
			dvar = 'x'
			#if request.method == 'GET':
			# if this is a POST request we need to process the form data

			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			my_function = form.cleaned_data['your_fn']
			if my_function is not None:
				my_guess = form.cleaned_data['your_guess']
				full_derivative, ofunction,ycount,f_d = index_fn(my_function,dvar,'y')
				error = index_fn_w(my_function,dvar,'y', my_guess)
				my_function= {'var':dvar,'q':my_function}
				my_function = urllib.parse.urlencode(my_function)
				#hashprefix = str(uuid.uuid4())
				
				#for i in range(0,n_pics):
				#	images.append(hashprefix+'ex'+str(i)+'.png')
				#	audios.append(hashprefix+'ex'+str(i)+'.mp3')
				#working=str(n_pics)
				is_derivative = True

				return render(request,'index2.html',{'error':error,'my_function':my_function,'working':working,'form': form,'images':images,'ofunction':ofunction,'full_derivative':full_derivative,'audios':audios,'is_derivative':is_derivative})

	form1 = TrigForm()
	form2 = DerivForm()
	form3 = RiemannForm()
	form5 = TangentForm()
	form6 = NewtonForm()
	form4 = IntegralForm()
	form7 = WrongDForm()
	return render(request,'videoSearch.html',{'form1':form1,'form2':form2,'form3':form3,'form4':form4,'form5':form5,'form6':form6,'form7':form7})
def trigInteractive(request):
	return render(request,'trigInteractive.html')
def riemannInteractive(request):
	return render(request,'riemannInteractive.html')
def riemannInteractiveFixed(request):
	return render(request,'riemannInteractiveFixed.html')
def about(request):
	return render(request,'about.html')
def help(request):
	return render(request,'help.html')

def derivative_worksheets(request):
	return render(request,'derivative_worksheets.html')

def derivatives_lesson(request):
	return render(request,'derivatives_lesson.html')

def calculus_worksheets(request):
	return render(request,'calculus_worksheets.html')
def loaderio(request):
	return render(request,'loaderio.html')
def privacy(request):
	return render(request,'privacy.html')
def terms(request):
	return render(request,'terms.html')
def contact(request):
	return render(request,'about.html')
def google(request):
	return render(request,'google.html')
def sitemap(request):
	return render(request,'sitemap.html', content_type="application/xhtml+xml")
def robots(request):
	return render(request,'robots.txt', content_type="text/plain")


def handler404(request):
	response = render_to_response('404.html', {},
								  context_instance=RequestContext(request))
	response.status_code = 404
	return response


def handler500(request):
	response = render_to_response('500.html', {},
								  context_instance=RequestContext(request))
	response.status_code = 500
	return response


#create table user_data(username varchar(30) primary key, power_rule numeric(6,2), expolog_rule numeric(6,2), trig_rule numeric(6,2), product_rule numeric(6,2), quo_rule numeric(6,2), chain_rule numeric(6,2), qanswered int, notification_1 varchar(140), notification_2 varchar(140), notification_3 varchar(140), notification_4 varchar(140), notification_5 varchar(140), notification_6 varchar(140), time_1 timestamptz default now(), time_2 timestamptz default now(), time_3 timestamptz default now(), time_4 timestamptz default now(), time_5 timestamptz default now(), time_6 timestamptz default now())
