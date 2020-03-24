from django.shortcuts import render


def power_rule_integral_lesson(request):
    vtitle = 'Power Rule Lesson - Calculus College'
    meta_des = 'The easiest functions to integrate are power functions, but make sure you can handle every case of the power rule every time without any stress.'
    vLessonTitle = 'Learn the Power Rule'
    vFormal = '<h3>$\\int[x^n]=\\frac{1}{n+1}x^{n+1}$</h3>'
    vInformal = 'Add one to the exponent and divide by the new exponent.'
    vLinks = [{'href':'\power_rule_integral_worksheet.html','title':'Power Rule Worksheet','description':"Work as many problems as you need. They're broken into many categories for your pleasure."}]
    vLinks.append({'href':'','title':'','description':''})
    vLinks.append({'href':'','title':'','description':''})
    vFlowchart = 'static/img/pr_integral_flow.png'
    vparts = [{'header':'What is the power rule?','text':'When the function is of the form $x^c$ for some constant $c\\neq -1$ then the integral is $\\frac{1}{c+1}x^{c+1}$.'}]
    vparts.append({'header':'When do we use the power rule?','text':'It should be obvious that when $x$ is raised to a positive integer power that the power rule applies. But the power rule applies for any real exponent other than -1. Fractions, decimals, constants, and even negative numbers are acceptable exponents to apply the power rule. Just make sure that the base is exactly $x$ (or whatever variable you are differentiating with respect to) and that there is nothing else happening in the function other than raising $x$ to a constant power.<p><br>Some functions are not obviously power functions. Any radical should be converted to a fractional exponent. And any power of $x$ in the denominator should be converted to a negative exponent so that the denominator is just 1. For example, $\sqrt{x}$ and $\\frac{1}{x^2}$ are power functions and the power rule should be applied to $x^{1/2}$ and $x^{-2}$ respectively.'})
    vparts.append({'header':'How do we use the power rule?','text':'Determine the exponent of $x$ and add one. Then divide by this new exponent. The only tricky part can be determining the exponent if the function is not already in $x^c$ form.'})
    vparts.append({'header':'What are some common mistakes?','text':'Be careful when adding one to a fractional exponent. Remember that one added to -2/3 is 1/3 not 2/3. Also be careful when adding to negative exponents. A negative number becomes smaller in magnitude when you add one (i.e. -5 becomes -4). These reminders may seem obvious, but make sure that you remember them every time you are speeding through an integral. Other than that, make sure you are really dealing with a power and the power rule is quite simple.'})
    next_lesson = 'Integrate <a href="exponentials_integral_lesson.html">Exponentials</a>'
    return render(request,'base_lesson.html',{'title':vtitle,'meta_des':meta_des,'LessonTitle':vLessonTitle,'Next':next_lesson,'Formal':vFormal,'Informal':vInformal,'Links':vLinks,'Flowchart':vFlowchart,'parts':vparts})
