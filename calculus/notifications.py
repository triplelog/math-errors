
from account.utils import user_display
import psycopg2

def notifications(request):
	notifications = [{'badge':'0 minutes ago','message':"You're not signed in.",'type':'danger'}]
	notifications.append({'badge':'0 minutes ago','message':"But you can still learn a lot without an account!",'type':'info'})
	notifications.append({'badge':'0 minutes ago','message':"Imagine how much you can learn more with an account!",'type':'success'})
	conn = psycopg2.connect('host=localhost dbname=calculus user=calculus password=SoODplvPsF')
	cur=conn.cursor()
	current_user=request.user
	if current_user.is_authenticated():
		cur.execute("select * from user_data where username=%s limit 1",(str(user_display(current_user)),))
		current_data = cur.fetchone()
		if current_data is None:
			cur.execute("insert into user_data (username,power_rule,expolog_rule,trig_rule,product_rule,quo_rule, chain_rule, qanswered, notification_1, notification_2, notification_3, notification_4, notification_5, notification_6) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_display(current_user),1500,1500,1500,1500,1500,1500,0,'You joined Calculus College. Get to work!','Practice taking derivatives.','Watch video solutions.','Watch video explanations.','Read in-depth explanations.','Follow links to the best outside content.'))
			conn.commit()
			cur.execute("select * from user_data where username=%s limit 1",(str(user_display(current_user)),))
			current_data = cur.fetchone()
		my_notifications = []
		for i in range(8,14):
			my_notifications.append({'badge':'5 minutes ago','message':current_data[i]})
		skill_arr = [50,50,50,50,50,50]
		for i in range(1,7):
			skill_arr[i-1]=int(100./(1.+10.**((1500-float(current_data[i]))/400.)))
		my_skills =  {'pr':skill_arr[-1+1],'er':skill_arr[-1+2],'tr':skill_arr[-1+3],'xr':skill_arr[-1+4],'qr':skill_arr[-1+5],'cr':skill_arr[-1+6]}

	else:
		my_notifications = notifications
		my_skills = {'pr':50,'er':50,'tr':50,'xr':50,'qr':50,'cr':50}




	cur.close()
	conn.close()
	return [my_notifications, my_skills]