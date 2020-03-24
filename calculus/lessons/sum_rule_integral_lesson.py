from django.shortcuts import render

def sum_rule_integral_lesson(request):
    vtitle = 'Sum Rule and Constant Multiples - Calculus College'
    meta_des = "Sums and constant multiples are easy to handle when taking integrals. We'll make sure you get it right every time so you can focus on the rest of Calculus."
    vLessonTitle = 'Learn the Sum Rule'
    vFormal = '<h3 style="font-size:16px;">$\\int{f(x)+g(x)dx}=\\int{f(x)dx}+\\int{g(x)dx}$<br>$\\int{cf(x)dx}=c\\int{f(x)dx}$</h3>'
    vInformal = 'Add the integrals of each term.'
    vLinks = [{'href':'sum_rule_integral_worksheet.html','title':'Sum Rule Worksheet','description':"Work as many problems as you need. They're broken into many categories for your pleasure."}]
    vLinks.append({'href':'','title':'','description':''})
    vLinks.append({'href':'','title':'','description':''})
    vFlowchart = 'static/img/sum_rule_integral_flowchart.png'
    vparts = [{'header':'When do we use the sum rule?','text':'Are there multiple terms in the function? If so, apply the sum rule. Differences work as well since they can easily be converted to sums. Also repeated additions can be combined into one step where all the integrals of each term are added together. <br><p>While using the sum rule will always be correct, sometimes it is easier to integrate without breaking up the sum first. When using the product rule to differentiate, a sum appears. Also, when differentiating a power function a coefficient appears. In both of these cases (and more) it is simpler to not break up the integral.'}]
    vparts.append({'header':'How do we take integrals of sums?','text':'The sum rule is so easy that most of the time you will not even realize that you are doing anything. Once you have identified the terms being added or subtracted then take the integral of each term. Taking these integrals will generally be the hard part. Then once you have all of the integrals just add them or subtract them back in the same order as in the original function.'})
    next_lesson = 'A lesson on the <a href="product_rule_lesson.html">Product Rule</a>'
    return render(request,'base_lesson.html',{'title':vtitle,'meta_des':meta_des,'LessonTitle':vLessonTitle,'Next':next_lesson,'Formal':vFormal,'Informal':vInformal,'Links':vLinks,'Flowchart':vFlowchart,'parts':vparts})
