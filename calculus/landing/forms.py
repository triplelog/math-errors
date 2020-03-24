from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter function to differentiate here...','size':'65','onKeyUp':'setTimeout(doLatex.bind(null,event),500)','class':'der_cal'}))


class NameForm1(forms.Form):
    your_fn = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter function to differentiate here...'}))
    your_guess = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'What do you think the derivative is?...'}))

 #<input type="text" class="form-control style_2" id="lastname_contact_home" name="lastname_contact_home" placeholder="Enter a function here for an interactive differentiation!" style="font-size:200%;">
class HomeForm(forms.Form):
	your_name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter function to differentiate here...','size':'75'}))

class TrigForm(forms.Form):
    trig_fn = forms.CharField(label='Expression to evaluate',widget=forms.TextInput(attrs={'placeholder': 'Enter something like sin(43pi/4) here...','size':'65','onKeyUp':'setTimeout(doLatexTrig.bind(null,event),500)','class':'der_cal'}))

class DerivForm(forms.Form):
    der_fn = forms.CharField(label='Function to differentiate',widget=forms.TextInput(attrs={'placeholder': 'Enter something like x^2 here...','size':'65','onKeyUp':'setTimeout(doLatexD.bind(null,event),500)','class':'der_cal'}))

class IntegralForm(forms.Form):
    int_fn = forms.CharField(label='Function to integrate',widget=forms.TextInput(attrs={'placeholder': 'Enter something like x^2 here...','size':'65','onKeyUp':'setTimeout(doLatexI.bind(null,event),500)','class':'der_cal'}))

class RiemannForm(forms.Form):
    rie_fn = forms.CharField(label='Function',widget=forms.TextInput(attrs={'placeholder': 'Enter something like x^2 here...','size':'25','onKeyUp':'setTimeout(doLatexRiemann.bind(null,event,1),500)','class':'der_cal'}))
    rie_a = forms.CharField(label='a',widget=forms.TextInput(attrs={'placeholder': 'Enter left edge of interval...','size':'25','onKeyUp':'setTimeout(doLatexRiemann.bind(null,event,2),500)','class':'der_cal','pattern':'[0-9pie.^-]*','title':'Must be a number.'}))
    rie_b = forms.CharField(label='b',widget=forms.TextInput(attrs={'placeholder': 'Enter right edge of interval...','size':'25','onKeyUp':'setTimeout(doLatexRiemann.bind(null,event,3),500)','class':'der_cal','type':'text','pattern':'[0-9pie.^-]*','title':'Must be a number.'}))
    rie_n = forms.CharField(label='# of rectangles',widget=forms.TextInput(attrs={'placeholder': 'Enter number of rectangles...','size':'25','onKeyUp':'setTimeout(doLatexRiemann.bind(null,event,4),500)','class':'der_cal','type':'text','pattern':'[0-9]+','title':'Must be a positive integer.'}))
    rie_r = forms.CharField(label='Method',widget=forms.TextInput(attrs={'placeholder': 'Enter left, mid, or right...','size':'25','onKeyUp':'setTimeout(doLatexRiemann.bind(null,event,5),500)','class':'der_cal','type':'text','pattern':'[lLmMrR][a-zA-z]*'}))

class TangentForm(forms.Form):
    tan_fn = forms.CharField(label='Function',widget=forms.TextInput(attrs={'placeholder': 'Enter something like x^2 here...','size':'65','onKeyUp':'setTimeout(doLatexT.bind(null,event,1),500)','class':'der_cal'}))
    tan_x = forms.CharField(label='x0',widget=forms.TextInput(attrs={'placeholder': 'Enter x-coordinate here...','size':'65','onKeyUp':'setTimeout(doLatexT.bind(null,event,2),500)','class':'der_cal','pattern':'[0-9pie.^-]*','title':'Must be a number.'}))

class NewtonForm(forms.Form):
    new_fn = forms.CharField(label='Function',widget=forms.TextInput(attrs={'placeholder': 'Enter something like x^2-40 here...','size':'65','onKeyUp':'setTimeout(doLatexNewton.bind(null,event,1),500)','class':'der_cal'}))
    new_x = forms.CharField(label='x0',widget=forms.TextInput(attrs={'placeholder': 'Enter first approximation...','size':'65','onKeyUp':'setTimeout(doLatexNewton.bind(null,event,2),500)','class':'der_cal','pattern':'[0-9pie.^-]*','title':'Must be a number.'}))

class WrongDForm(forms.Form):
    your_fn = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter function to differentiate here...','size':'65'}))
    your_guess = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'What do you think the derivative is?...','size':'65'}))

class SignupForm(forms.Form):
    your_email = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Email','size':'65','type':'email'}))
    your_password = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Password','size':'65','type':'password'}))
    conf_password = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Confirm','size':'65','type':'password'}))

class LoginForm(forms.Form):
    your_email = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Email','size':'65','type':'email'}))
    your_password = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Password','size':'65','type':'password'}))