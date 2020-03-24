from django.shortcuts import render

def sum_rule_lesson(request):
    vtitle = 'Sum Rule and Constant Multiples - Calculus College'
    meta_des = "Sums and constant multiples are easy to handle when taking derivatives. We'll make sure you get it right every time so you can focus on the rest of Calculus."
    vLessonTitle = 'Learn the Sum Rule'
    vFormal = '<h3 style="font-size:16px;">$\\frac{d}{dx}[f(x)+g(x)]=\\frac{d}{dx}[f(x)]+\\frac{d}{dx}[g(x)]$<br>$\\frac{d}{dx}[cf(x)]=c\\frac{d}{dx}[f(x)]$</h3>'
    vInformal = 'Add the derivatives of each term.'
    vLinks = [{'href':'sum_rule_worksheet.html','title':'Sum Rule Worksheet','description':"Work as many problems as you need. They're broken into many categories for your pleasure."}]
    vLinks.append({'href':'https://www.khanacademy.org/math/differential-calculus/basic-differentiation-dc/polynomial-functions-differentiation-dc/v/derivative-properties-and-polynomial-derivatives','title':'Differentiating Polynomials','description':'A Khan Academy video about differentiating polynomials which are some of the simplest functions with sums and constant multiples.'})
    vLinks.append({'href':'http://math2.org/math/derivatives/identities/sum.htm','title':'Sum Rule Proof','description':'A quick proof of the sum rule using limits.'})
    vFlowchart = 'static/img/sum_rule_flowchart.png'
    vparts = [{'header':'When do we use the sum rule?','text':'Are there multiple terms in the function? If so, apply the sum rule. Differences work as well since they can easily be converted to sums. Also repeated additions can be combined into one step where all the derivatives of each term are added together. '}]
    vparts.append({'header':'How do we take derivatives of sums?','text':'The sum rule is so easy that most of the time you will not even realize that you are doing anything. Once you have identified the terms being added or subtracted then take the derivative of each term. Taking these derivatives will be the hard part. Then once you have all of the derivatives just add them or subtract them back in the same order as in the original function.'})
    next_lesson = 'A lesson on the <a href="product_rule_lesson.html">Product Rule</a>'
    return render(request,'base_lesson.html',{'title':vtitle,'meta_des':meta_des,'LessonTitle':vLessonTitle,'Next':next_lesson,'Formal':vFormal,'Informal':vInformal,'Links':vLinks,'Flowchart':vFlowchart,'parts':vparts})
