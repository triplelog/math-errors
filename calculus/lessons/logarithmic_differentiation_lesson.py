from django.shortcuts import render


def logarithmic_differentiation_lesson(request):
    vtitle = 'Logarithmic Differentiation Lesson - Calculus College'
    meta_des = 'When you have no other options, try taking a logarithm and then differentiating. Sounds crazy, but it helps. Learn how to do logarithmic differentiation properly.'
    vLessonTitle = 'Log Differentiation'
    vFormal = "<h3 style='font-size:22px;'>$\\frac{d}{dx}[\ln(f(x))]=\\frac{f'(x)}{f(x)}$<br>$\\frac{d}{dx}[f(x)]=\\frac{d}{dx}[\ln(f(x))]f(x)$</h3>"
    vInformal = 'Differentiate the natural logarithm of the function and then multiply that by the original function. '
    vLinks = [{'href':'http://tutorial.math.lamar.edu/Classes/CalcI/LogDiff.aspx','title':'Logarithmic Differentiation','description':"Paul's Notes provides an in-depth explanation of when and how to use logarithmic differentiation."}]
    vLinks.append({'href':'https://www.youtube.com/watch?v=Q27MGfI1V70','title':'Logarithmic Differentiation','description':'PatrickJMT has a good video on the subject.'})
    vLinks.append({'href':'https://www.math.ucdavis.edu/~kouba/CalcOneDIRECTORY/logdiffdirectory/LogDiff.html','title':'Logarithmic Differentiation','description':'UC Davis provides many example problems worked out for you.'})
    vFlowchart = 'static/img/logarithmic_differentiation_flowchart.png'
    vparts = [{'header':'When is logarithmic differentiation used?','text':'Only use logarithmic differentiation when taking the derivative without taking a logarithm seems impossible or would take many steps. One time when logarithms are unavoidable is when a function of $x$ is raised to an exponent that is also a function of $x$. The other time logarithms are used is when the function consists of the product of many functions of $x$. In this case it is possible to repeatedly apply the product rule, but logarithmic differentiation will be faster if there are several factors. Note that logarithmic differentiation is generally used on functions that do not have any logarithms involved. '}]
    vparts.append({'header':'What is logarithmic differentiation?','text':'The first step is to take the natural logarithm of the function. The only reason logarithmic differentiation helps is because properties of logarithms can simplify the problem so the next step is to apply one of two properties of logarithms. Either bring the exponent inside the logarithm to the front or separate the factors into a sum of logarithms. Then this new function should be easier to differentiate so do that now using the sum or product rule. Then to end up with the derivative we want we multiply this derivative by the original function.'})
    next_lesson = 'Learn how to integrate functions (coming soon)'
    return render(request,'base_lesson.html',{'title':vtitle,'meta_des':meta_des,'LessonTitle':vLessonTitle,'Next':next_lesson,'Formal':vFormal,'Informal':vInformal,'Links':vLinks,'Flowchart':vFlowchart,'parts':vparts})
