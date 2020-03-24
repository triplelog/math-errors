from django.shortcuts import render


def trigonometric_functions_integral_lesson(request):
    vtitle = 'Trigonometric Integrals Lesson - Calculus College'
    meta_des = 'Learn how to integrate some basic trig functions.'
    vLessonTitle = 'Trigonometric Functions'
    vFormal = 'Memorize the chart!'
    vInformal = 'Remember how trig derivatives work. '
    vLinks = [{'href':'trigonometric_functions_integral_worksheet.hmtl','title':'Trigonometric Functions Worksheet','description':"Work as many problems as you need. They're broken into many categories for your pleasure."}]
    vLinks.append({'href':'','title':'','description':''})
    vLinks.append({'href':'','title':'','description':''})
    vFlowchart = 'static/img/trigonometric_functions_integral_flowchart.png'
    vparts = [{'header':'When do we use trig integration?','text':'Some trig functions are easy to integrate so learn to recognize these functions.'}]
    vparts.append({'header':'How do we ?','text':''})
    vparts.append({'header':'How do we ?','text':''})
    next_lesson = 'A lesson on the <a href="sum_rule_lesson.html">Sum Rule</a>'

    return render(request,'base_lesson.html',{'title':vtitle,'meta_des':meta_des,'LessonTitle':vLessonTitle,'Next':next_lesson,'Formal':vFormal,'Informal':vInformal,'Links':vLinks,'Flowchart':vFlowchart,'parts':vparts})
