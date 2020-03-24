from django.shortcuts import render


def integration_by_parts_lesson(request):
    vtitle = 'Integration by Parts Lesson - Calculus College'
    meta_des = 'Learn how to use integration by parts to integrate more complicated integrals.'
    vLessonTitle = 'Integration by Parts'
    vFormal = '$\\int{f(x)dx}=$'
    vInformal = 'Undo the chain rule.'
    vLinks = [{'href':'integration_by_parts_worksheet.hmtl','title':'Integration by Parts Worksheet','description':"Work as many problems as you need. They're broken into many categories for your pleasure."}]
    vLinks.append({'href':'','title':'','description':''})
    vLinks.append({'href':'','title':'','description':''})
    vFlowchart = 'static/img/integration_by_parts_flowchart.png'
    vparts = [{'header':'When do we ?','text':''}]
    vparts.append({'header':'How do we ?','text':''})
    vparts.append({'header':'What ?','text':''})
    next_lesson = 'A lesson on the <a href="_lesson.html"></a>'

    return render(request,'base_lesson.html',{'title':vtitle,'meta_des':meta_des,'LessonTitle':vLessonTitle,'Next':next_lesson,'Formal':vFormal,'Informal':vInformal,'Links':vLinks,'Flowchart':vFlowchart,'parts':vparts})
