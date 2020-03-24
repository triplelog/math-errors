from django.shortcuts import render


def quotient_rule_lesson(request):
    vtitle = 'Quotient Rule Lesson - Calculus College'
    meta_des = "You should be able to identify when a function is a fraction. Let us help you figure out what to do next so the quotient rule doesn't trip you up."
    vLessonTitle = 'Quotient Rule Lesson'
    vFormal = '<h3 style="font-size:20px;">$\\frac{d}{dx}[\\frac{f(x)}{g(x)}]=\\frac{g(x)\\frac{d}{dx}[f(x)]-f(x)\\frac{d}{dx}[g(x)]}{g(x)^2}$</h3>'
    vInformal = 'The derivative of a rational function has a numerator of the bottom function multiplied by the derivative of the top function minus the top function multiplied by the derivative of the bottom function. The denominator of the derivative is the bottom function squared.'
    vLinks = [{'href':'/quotient_rule_worksheet.html','title':'Quotient Rule Worksheet','description':"Work as many problems as you need. They're broken into many categories for your pleasure."}]
    vLinks.append({'href':'https://www.youtube.com/watch?v=jIX0VvwfEko','title':'Quotient Rule Made Easier','description':'A video by mathbff providing a quick explanation of how to learn the quotient rule.'})
    vLinks.append({'href':'https://www.math.hmc.edu/calculus/tutorials/quotient_rule/','title':'Quotient Rule for Derivatives','description':'Harvey Mudd College has a few examples of the quotient rule in action.'})
    vFlowchart = 'static/img/quotient_rule_flowchart.png'
    vparts = [{'header':'When can we apply the quotient rule?','text':'Apply the quotient rule when the function is a fraction where the numerator and denominator both depend on $x$. The function will be of the form $\\frac{f(x)}{g(x)}$ so try to identify what $f(x)$ and $g(x)$ equal. If you can break it down into that exact form then apply the quotient rule. There is no requirement that both the top and bottom must depend on $x$, but it is only really necessary in this case.'}]
    vparts.append({'header':'How do we differentiate a fraction?','text':'Determine the numerator and denominator of the function. This should be easy, but make sure that you are accounting for the entire function. Then differentiate each part separately. The numerator or denominator could be extremely complicated functions so remember to treat each function carefully when differentiating. Then plug these values into the quotient rule alongside the original functions. Do not forget where the negative sign goes.'})
    vparts.append({'header':'What are some common quotient rule mistakes?','text':'The two most common mistakes are getting the negative sign switched in the numerator and forgetting to divide by the square of the denominator. The first term in the numerator must be the one with the derivative of the numerator. In the <a href="product_rule_lesson.html">product rule</a> the order does not matter, but in the quotient rule the subtraction makes order matter. Make sure you memorize the exact form of the quotient rule!'})
    next_lesson = 'A lesson on the <a href="chain_rule_lesson.html">Chain Rule</a>'
    return render(request,'base_lesson.html',{'title':vtitle,'meta_des':meta_des,'LessonTitle':vLessonTitle,'Next':next_lesson,'Formal':vFormal,'Informal':vInformal,'Links':vLinks,'Flowchart':vFlowchart,'parts':vparts})
