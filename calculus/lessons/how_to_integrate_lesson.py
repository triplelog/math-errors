from django.shortcuts import render

def how_to_integrate_lesson(request):
    vtitle = 'How to Take Integrals - Calculus College'
    meta_des = 'We created an integral calculator and will teach you all the tricks it uses to compute integrals. Learn the process that works for every function you may need to integrate.'
    vLessonTitle = 'How to take any integral'
    vInformal = 'Try every rule until something works.'
    vFormal = 'Is the function one of the basic functions? If yes, take the integral. If not, apply the right rules until integration is posisble.'
    vLinks = [{'href':'','title':'','description':""}]
    vLinks.append({'href':'','title':'','description':''})
    vLinks.append({'href':'','title':'','description':''})
    vFlowchart = 'static/img/how_to_integrate_flowchart.png'
    vparts = [{'header':'How do we take integrals?','text':'It is important that you are comfortable with differentiation before learning integration. Derivatives follow a nice set of rules that allow for a straightforward process, while integrals try to undo those rules. Thus, integration is more of an artform. <br><p>Think about how a function might be differentiated to yield the given function. It is okay to take an educated guess or not know the exact form that needs to be differentiated. '}]
    vparts.append({'header':'What is the first step?','text':'Check if some basic function works.'})
    vparts.append({'header':'What if the function is not so basic?','text':'See if u-substitution, integration by parts, trigonometric identities, or partial fractions are needed. Look at how functions are combined to yield the integral. Are they multiplied? Function composition? <br><p>If you are taking a timed exam and do not see a way to integrate a function then skip it and come back later. As you work other problems you very well might see something that helps you solve the problem. If not, try to come up with a function with derivative as similar as possible. '})
    next_lesson = 'A lesson on the <a href="power_rule_lesson.html">Power Rule</a>'
    return render(request,'base_lesson.html',{'title':vtitle,'meta_des':meta_des,'LessonTitle':vLessonTitle,'Next':next_lesson,'Formal':vFormal,'Informal':vInformal,'Links':vLinks,'Flowchart':vFlowchart,'parts':vparts})
