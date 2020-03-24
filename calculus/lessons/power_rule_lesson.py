from django.shortcuts import render


def power_rule_lesson(request):
    vtitle = 'Power Rule Lesson - Calculus College'
    meta_des = 'The easiest functions to differentiate are power functions, but make sure you can handle every case of the power rule every time without any stress.'
    vLessonTitle = 'Learn the Power Rule'
    vFormal = '<h3>$\\frac{d}{dx}[x^n]=nx^{n-1}$</h3>'
    vInformal = 'Move the exponent down and subtract one from the old exponent.'
    vLinks = [{'href':'\power_rule_worksheet.html','title':'Power Rule Worksheet','description':"Work as many problems as you need. They're broken into many categories for your pleasure."}]
    vLinks.append({'href':'http://patrickjmt.com/basic-derivative-examples/','title':'Derivatives – Basic Examples','description':'PatrickJMT works through examples that use the power rule'})
    vLinks.append({'href':'https://www.khanacademy.org/math/calculus-home/taking-derivatives-calc/power-rule-calc/v/proof-d-dx-x-n','title':'Proof of power rule for positive integer powers','description':'A Khan Academy video proving part of the power rule.'})
    vFlowchart = 'static/img/pr_flow.png'
    vparts = [{'header':'What is the power rule?','text':'When the function is of the form $x^c$ for some constant $c$ then the derivative is $cx^{c-1}$.'}]
    vparts.append({'header':'When do we use the power rule?','text':'It should be obvious that when $x$ is raised to a positive integer power that the power rule applies. But the power rule applies for any real exponent. Fractions, decimals, constants, and even negative numbers are acceptable exponents to apply the power rule. Just make sure that the base is exactly $x$ (or whatever variable you are differentiating with respect to) and that there is nothing else happening in the function other than raising $x$ to a constant power.<p><br>Some functions are not obviously power functions. Any radical should be converted to a fractional exponent. And any power of $x$ in the denominator should be converted to a negative exponent so that the denominator is just 1. For example, $\sqrt{x}$ and $\\frac{1}{x^2}$ are power functions and the power rule should be applied to $x^{1/2}$ and $x^{-2}$ respectively.'})
    vparts.append({'header':'How do we use the power rule?','text':'Determine the exponent of $x$ and make it the new coefficient. Then reduce this exponent by one and make that the new exponent. The only tricky part can be determining the exponent if the function is not already in $x^c$ form.'})
    vparts.append({'header':'What are some common mistakes?','text':'Be careful when subtracting one from a fractional exponent. Remember that one subtracted from 1/3 is -2/3 not -1/3. Also be careful when subtracting from negative exponents. A negative number becomes larger in magnitude when you subtract one (i.e. -5 becomes -6). These reminders may seem obvious, but make sure that you remember them every time you are speeding through a derivative. Other than that, make sure you are really dealing with a power and the power rule is quite simple.'})
    next_lesson = 'Differentiate <a href="exponentials_logarithms_lesson.html">Exponentials & Logarithms</a>'
    return render(request,'base_lesson.html',{'title':vtitle,'meta_des':meta_des,'LessonTitle':vLessonTitle,'Next':next_lesson,'Formal':vFormal,'Informal':vInformal,'Links':vLinks,'Flowchart':vFlowchart,'parts':vparts})
