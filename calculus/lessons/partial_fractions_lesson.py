from django.shortcuts import render


def partial_fractions_lesson(request):
    vtitle = 'Definite Integrals Lesson - Calculus College'
    meta_des = 'Learn how to compute definite integrals.'
    vLessonTitle = 'Definite Integrals'
    vFormal = '$\\int_a^b{f(x)dx}=F(b)-F(a)$'
    vInformal = 'Evaluate the antiderivative at the right endpoint and subtract the antiderivative evaluated at the left endpoint.'
    vLinks = [{'href':'definite_integrals_worksheet.hmtl','title':'Trigonometric Functions Worksheet','description':"Work as many problems as you need. They're broken into many categories for your pleasure."}]
    vLinks.append({'href':'','title':'','description':''})
    vLinks.append({'href':'','title':'','description':''})
    vFlowchart = 'static/img/definite_integrals_flowchart.png'
    vparts = [{'header':'When do we ?','text':''}]
    vparts.append({'header':'How do we ?','text':''})
    vparts.append({'header':'What ?','text':''})
    next_lesson = 'A lesson on the <a href="_lesson.html"></a>'

    return render(request,'base_lesson.html',{'title':vtitle,'meta_des':meta_des,'LessonTitle':vLessonTitle,'Next':next_lesson,'Formal':vFormal,'Informal':vInformal,'Links':vLinks,'Flowchart':vFlowchart,'parts':vparts})
