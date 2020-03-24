from django.shortcuts import render


def product_rule_lesson(request):
    vtitle = 'Product Rule Lesson - Calculus College'
    meta_des = "You should be able to identify when a function is a product. Let us help you figure out what to do next so the product rule doesn't trip you up."
    vLessonTitle = 'Product Rule Lesson'
    vFormal = '$\\frac{d}{dx}[f(x)g(x)]=f(x)\\frac{d}{dx}[g(x)]+g(x)\\frac{d}{dx}[f(x)]$'
    vInformal = 'Multiply each factor by the derivative of the other factor and then add these two terms together.'
    vLinks = [{'href':'\product_rule_worksheet.html','title':'Product Rule Worksheet','description':"Work as many problems as you need. They're broken into many categories for your pleasure."}]
    vLinks.append({'href':'https://www.math.hmc.edu/calculus/tutorials/prodrule/','title':'Product Rule for Derivatives','description':'Harvey Mudd College has a few product rule examples ready for you.'})
    vLinks.append({'href':'https://www.khanacademy.org/math/ap-calculus-ab/product-quotient-chain-rules-ab/product-rule-ab/v/applying-the-product-rule-for-derivatives','title':'Product Rule Intro','description':'A short Khan Academy video working through a product rule problem.'})
    vFlowchart = 'static/img/product_rule_flowchart.png'
    vparts = [{'header':'When do you use the product rule?','text':'Use the product rule when the function consists of the product of two simpler functions. Can you identify an $f(x)$ and $g(x)$ such that the function exactly equals $f(x)g(x)$? If yes, use the product rule.'}]
    vparts.append({'header':'How do you use the product rule?','text':'Once you have identified the two factors, $f(x)$ and $g(x)$, find the derivative of each factor. These derivatives could be complicated and require several steps, but they shoud be easier than differentiating the original function. Once you have carefully differentiated both factors combine the derivatives and the original functions according to the product rule: $f(x)\\frac{d}{dx}[g(x)]+g(x)\\frac{d}{dx}[f(x)]$.'})
    vparts.append({'header':'What are some common mistakes to avoid?','text':'Do not simply differentiate each factor and multiply the derivatives. Also you can rearrange the terms or factors according to the commutative property so your answer may come in many equivalent forms, but it is necessary that the derivatives be multiplied by the other function.'})
    next_lesson = 'A lesson on the <a href="quotient_rule_lesson.html">Quotient Rule</a>'
    return render(request,'base_lesson.html',{'title':vtitle,'meta_des':meta_des,'LessonTitle':vLessonTitle,'Next':next_lesson,'Formal':vFormal,'Informal':vInformal,'Links':vLinks,'Flowchart':vFlowchart,'parts':vparts})
