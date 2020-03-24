from django.shortcuts import render


def exponentials_logarithms_lesson(request):
    vtitle = 'Exponentials and Logarithms Lesson - Calculus College'
    meta_des = 'Exponential and logarithmic functions are easy to differentiate so make sure that you know how because they will appear repeatedly.'
    vLessonTitle = 'Exponentials and Logs'
    vFormal = '<h3>$\\frac{d}{dx}[b^x]=\ln(b)b^x$<br>$\\frac{d}{dx}[\log_{b}{x}]=\\frac{1}{\ln(b)x}$</h3>'
    vInformal = 'The derivative of the exponential function is itself. The derivative of the natural logarithm function is 1/x. '
    vLinks = [{'href':'exponentials_logarithms_worksheet.html','title':'Exponentials and Logarithms Worksheet','description':"Work as many problems as you need. They're broken into many categories for your pleasure."}]
    vLinks.append({'href':'http://tutorial.math.lamar.edu/Classes/CalcI/DiffExpLogFcns.aspx','title':'Derivatives of Exponential and Logarithm Functions','description':"Paul's Notes explain in-depth how to differentiate these functions and has examples worked out for you."})
    vLinks.append({'href':'http://www.math.brown.edu/UTRA/explog.html','title':'Derivatives of Exponential & Logarithmic Functions','description':'Brown University has a quick refresher on how to differentiate these functions.'})
    vFlowchart = 'static/img/exponentials_logarithms_flowchart.png'
    vparts = [{'header':'What is the derivative of an exponential or logarithmic function?','text':'The most common functions in this category are $e^x$ and $\ln(x)$. So you definitely need to learn that the derivative of $e^x$ is $e^x$ and the derivative of $\ln(x)$ is $1/x$. Although base $e$ may seem confusing, these functions are most common in Calculus class because they are the easiest to differentiate. Other bases have similar derivatives, but they involve ugly constant terms.'}]
    vparts.append({'header':'When can we treat the function as an exponential?','text':'Is the function of the form $b^x$ where $b$ does not depend on $x$? If so, then we can treat the function as an exponential. This base could be $e$ (and often is), a positive integer, a fraction, or some other constant. The only real confusion could arise if the function looks like $\\frac{1}{4^x}$ or $4^{-x}$ or $(1/2)^{2x}$. These are all the same function, but in order to treat the function as an exponential you must rewrite them to $(1/4)^x$. The exponent must exactly be $x$. We will learn other methods to deal with non-$x$ exponents later, but using properties of exponents allow for an easy method to make the function more basic.'})
    vparts.append({'header':'How do we differentiate an exponential function?','text':'Determine the base of the exponential. Take the natural logarithm of this base. Multiply this natural logarithm by the original function. If the base is $e$ then the natural logarithm of $e$ is 1 so the $\ln(e)$ can be ignored. If the base is an integer, like 2, then usually you just want to leave the natural logarithm in your answer, like $\ln(2)2^x$, rather than approximating.'})
    vparts.append({'header':'When can we treat the function as a logarithmic function?','text':'Is the function of the form $\ln(x)$ or $\log_b(x)$? If not, you need to be able to rewrite the function using properties of logarithms so that the inside of the logarithm is simply $x$.'})
    vparts.append({'header':'How do we differentiate a logarithmic function?','text':'Determine the base of the logarithm. Take the natural logarithm of this base. Multiply this natural logarithm by $x$ and place that product in the denominator of a fraction with a numerator of 1. Again, if the base is $e$ the natural logarithm does not change the expression. And if the base is an integer leave the natural logarithm in your answer.'})
    next_lesson = 'Learn how to differentiate <a href="trigonometric_functions_lesson.html">Trig Functions</a>'
    return render(request,'base_lesson.html',{'title':vtitle,'meta_des':meta_des,'LessonTitle':vLessonTitle,'Next':next_lesson,'Formal':vFormal,'Informal':vInformal,'Links':vLinks,'Flowchart':vFlowchart,'parts':vparts})
