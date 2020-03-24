import sympy
from sympy import *
from sympy import ratsimp
from sympy.parsing.sympy_parser import parse_expr

def fullparen(input_string):
	openpar = 0
	isbreak = 0
	cancel_it = 0
	really_cancel = 0
	for idx,i in enumerate(input_string):
		if i == '(':
			openpar = openpar+1
		elif i == ')':
			openpar = openpar-1
		if openpar == 0:
			cancel_it = 1
			isbreak = idx
			break
	if isbreak == len(input_string)-1:
		return True
	else:
		if input_string[0:3] in ['log','sin','cos','tan','cot','sec','csc']:
			return fullparen(input_string[3:])
		elif input_string[0:2] in ['ln']:
			return fullparen(input_string[2:])
		elif input_string[0:6] in ['arcsin','arccos','arctan','arccot','arcsec','arccsc']:
			return fullparen(input_string[6:])
		else:
			try:
				floatexp = float(input_string)
				return True
			except:
				return False

def full_sq(input_string):
	openpar = 0
	isbreak = 0
	for idx,i in enumerate(input_string):
		if i == '(':
			openpar = openpar+1
		elif i == ')':
			openpar = openpar-1
		if openpar == 0:
			isbreak = idx
			break
	return isbreak

def replace_sqrt(inputexpression):
	sqrt_index = -1
	go_sqrt = True
	while go_sqrt:
		go_sqrt = False
		sqrt_index = inputexpression.find('sqrt')
		if sqrt_index > -1:
			go_sqrt = True
			end_index = full_sq(inputexpression[sqrt_index+4:])
			t_inside = inputexpression[sqrt_index+5:sqrt_index+end_index+4]
			e_index = t_inside.find('^')
			no_change = 1
			if e_index > -1:
				if fullparen(t_inside[:e_index]):
					if fullparen(t_inside[e_index+1:]):
						new_ie = inputexpression[0:sqrt_index]+t_inside[:e_index+1]+'(('+t_inside[e_index+1:]+')/2)'+inputexpression[sqrt_index+end_index+5:]
						no_change = 0
			if no_change == 1:
				new_ie = inputexpression[0:sqrt_index]+inputexpression[sqrt_index+4:sqrt_index+end_index+5]+'^(1/2)'+inputexpression[sqrt_index+end_index+5:]
			inputexpression=new_ie

			# Check for full paren raised to full paren
	return inputexpression

def checksame(guess,checkfn,dvar):
	notsame = 0
	try:
		ssg = sympy.sympify(guess)
		ssc = sympy.sympify(checkfn)
		for i in [0,1,-1,.5]:
			try:
				lssg = ssg.subs(x,i)
				try:
					lssc = ssc.subs(x,i)
					if lssc < lssg-.00001:
						return False
					elif lssc > lssg+.00001:
						return False
				except:
					pass
			
			except:
				pass
		if ssg.equals(ssc):
			return True
		else:
			if guess.find('e^')>-1:
				ge = guess.replace('e^','2.7^')
				cf = checkfn.replace('e^','2.7^')
				if ge.equals(cf):
					return True
			if sympy.simplify(sympy.sympify(guess)).equals(sympy.simplify(sympy.sympify(checkfn))):
				return True
			else:
				guess = replace_sqrt(guess)
				checkfn = replace_sqrt(checkfn)
				try:
					if sympy.sympify(guess,evaluate=False).equals(sympy.sympify(checkfn,evaluate=False)):
						return True
					else:
						if sympy.sympify(guess).equals(sympy.sympify(checkfn)):
							return True
						else:
							if sympy.simplify(sympy.sympify(guess,evaluate=False)).equals(sympy.simplify(sympy.sympify(checkfn,evaluate=False))):
								return True
							else:
								if guess.find('e^')>-1:
									ge = guess.replace('e^','2.7^')
									cf = checkfn.replace('e^','2.7^')
									return checksame(ge,cf,dvar)
								else:
									if guess.find('abs('+dvar+')')>-1:
										ge =guess.replace('abs('+dvar+')','sqrt(('+dvar+')^2)')
										cf = checkfn.replace('abs('+dvar+')','sqrt(('+dvar+')^2)')
										return checksame(ge,cf,dvar)
									elif checkfn.find('abs('+dvar+')')>-1:
										ge =guess.replace('abs('+dvar+')','sqrt(('+dvar+')^2)')
										cf =checkfn.replace('abs('+dvar+')','sqrt(('+dvar+')^2)')
										return checksame(ge,cf,dvar)
									else:
										return False
				except:
					if sympy.sympify(guess).equals(sympy.sympify(checkfn)):
						return True
					else:
						if sympy.simplify(sympy.sympify(guess)).equals(sympy.simplify(sympy.sympify(checkfn))):
							return True
						else:
							if guess.find('e^')>-1:
								ge = guess.replace('e^','2.7^')
								cf = checkfn.replace('e^','2.7^')
								return checksame(ge,cf,dvar)
							else:
								if guess.find('abs('+dvar+')')>-1:
									ge =guess.replace('abs('+dvar+')','sqrt(('+dvar+')^2)')
									cf = checkfn.replace('abs('+dvar+')','sqrt(('+dvar+')^2)')
									return checksame(ge,cf,dvar)
								elif checkfn.find('abs('+dvar+')')>-1:
									ge =guess.replace('abs('+dvar+')','sqrt(('+dvar+')^2)')
									cf =checkfn.replace('abs('+dvar+')','sqrt(('+dvar+')^2)')
									return checksame(ge,cf,dvar)
								else:
									return False
	except:
		if guess.find('e^')>-1:
			ge = guess.replace('e^','2.7^')
			cf = checkfn.replace('e^','2.7^')
			return checksame(ge,cf,dvar)
		else:
			return False

def checksimilar(guess,checkfn,dvar):
	try:
		ssg = sympy.sympify(guess)
		ssc = sympy.sympify(checkfn)
		for i in [0,1,2,3,4,5,6,7,8,9,10]:
			try:
				lssg = ssg.subs(x,i)
				try:
					lssc = ssc.subs(x,i)
					if lssc < lssg-.00001:
						return False
					elif lssc > lssg+.00001:
						return False
				except:
					pass
			
			except:
				pass
		return True
	except:
		return False
#print sympy.sympify('-1/(sqrt(x^2-1)*abs(x))')
#print checksame('-1/(sqrt(x^2-1)*abs(x))','-1/(x**2*sqrt(1 - 1/x**2))','x')
#print sympy.sympify('log(x)').subs('x',0).evalf()
#print checksame('ln(sin(x))+1','ln(sin(x))+cos(x)^2+sin(x)^2','x')
#print replace_sqrt('sqrt(x^2)+sqrt((X)^5)+sqrt(x-2)+sqrt(x^21)')
#print checksame('3/2*x^(1/2)','3*x^2/(2*sqrt(x^3))','x')
