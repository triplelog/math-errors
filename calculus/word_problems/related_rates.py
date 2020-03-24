


We know the value of two variables, but want to know the value of a third. We need to find an equation relating the three variables. There is no equation relating just these three variables, but each is a derivative. What is an equation relating $x,y,$ and $z$? We have a right triangle so $x^2+y^2=z^2$. 
\newline
If two expressions are equal then the derivatives of each will also be equal. We want to differentiate each side of the equation, but we must be careful because we are differentiating with respect to $t$ and there does not appear to a $t$ in the equation. How can we differentiate with respect to $t$? Each of $x,y,$ and $z$ are functions of $t$ so we must apply the chain rule when differentiating each variable. 
\newline
What does the equaiton look like after differentiating? $2x\frac{dx}{dt}+2y\frac{dy}{dt}=2z\frac{dz}{dt}$. 
\newline
Which of these $6$ variables are not given in the problem? $z$ and $\frac{dz}{dt}$
\newline
How can we determine $z$ based on the information given? Use $x^2+y^2=z^2$.
\newline 
What is $z$? Plug in $x=4$ and $y=3$ to get $z^2=25$ so $z=5$.
\newline
What is $\frac{dz}{dt}$? Plug in all of our values into $2x\frac{dx}{dt}+2y\frac{dy}{dt}=2z\frac{dz}{dt}$ to yield $400+240=10\frac{dz}{dt}$ so $\frac{dz}{dt}=64$.
\newline
What is the final answer? The distance between the cars is increasing at a rate of $64$ mph.



num_minutes = 'four'
red = {'miles': 4, 'speed': 50}
gray = {'miles': 3, 'speed': 40}
base_q = 'Two cars leave an intersection. After '+num_minutes+' minutes, the red car is '+str(red['miles'])+' miles to the east and the gray car is '+str(gray['miles'])+' miles north of the intersection. The red car is travelling at '+str(red['speed'])+' mph and the gray car at '+str(gray['speed'])+' mph. At this moment, how fast is the distance between the cars changing?'

picture_cars = '\\begin{tikzpicture}[node distance=0pt]\n\\node (inter) [inter] {};\n\\node (car1) [car, right of=inter, xshift=300pt] {red car};\n\\node (car2) [car, below of=inter, yshift=225pt] {gray car};'

if nrounds>1:
	picture_arrows = '\draw [arrow] (inter.east) -- node[anchor=north] {$x$} (car1.west);\n'
else:
	picture_arrows = '\draw [arrow] (inter.east) -- node[anchor=north] {} (car1.west);\n'
if nrounds>3:
	picture_arrows = picture_arrows+'\draw [arrow] (inter.north) -- node[anchor=north] {$y$} (car2.south);\n'
else:
	picture_arrows = picture_arrows+'\draw [arrow] (inter.north) -- node[anchor=north] {} (car2.south);\n'
if nrounds>5:
	picture_arrows = picture_arrows+'\draw [darrow] (car1) -- node[anchor=north] {} (car2);\n\end{tikzpicture}\n\\newline\n'
else:
	picture_arrows = picture_arrows+'\draw [darrow] (car1) -- node[anchor=north] {} (car2);\n\end{tikzpicture}\n\\newline\n'

solution_x = ''
if nrounds>1:
	solution_x = "Let's call the distance from the intersection to the red car $x$. What does "+str(red['speed'])+" mph represent in terms of our variables?"
if nrounds>2:
	solution_x=solution_x+"$\\frac{dx}{dt}$\\newline"

solution_y = ''
if nrounds>3:
	solution_y = "Let's call the distance from the intersection to the red car $x$. What does "+str(red['speed'])+" mph represent in terms of our variables?"
if nrounds>4:
	solution_y=solution_y+"$\\frac{dy}{dt}$\\newline"

solution_z = ''
if nrounds>5:
	solution_z = "Let's call the distance between the two cars $z$. Then what rate are we trying to determine?"
if nrounds>6:
	solution_z=solution_z+"$\\frac{dz}{dt}$\\newline"


