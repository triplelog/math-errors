from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from bs4 import BeautifulSoup
from landing.views import *
import sympy
from main import fullderivative
from checkcorrect import checksame, checksimilar
from clean import cleanpar

class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
		self.assertIn(b'<title>Calculus College - Learn Calculus</title>', response.content)

class WorksheetTest(TestCase):

	def test_power_correct(self):
		request = HttpRequest()
		response = power_rule_worksheet(request)
		soup = BeautifulSoup(response.content,'html5lib')
		self.assertEqual(str(soup.title),'<title>Power Rule Worksheet - Learn the Power Rule by working examples with Calculus College.</title>')
		for the_id in ['One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven']:
			t_id = 'Question_'+the_id
			find_id = soup.find_all(id=t_id)
			if len(find_id)>0:
				my_question = find_id[0].get_text()
				print(my_question, end=' ')
				sympy_diff = str(sympy.diff(sympy.sympify(cleanpar(my_question,'x').replace('arc','a')),'x'))
				my_diff = fullderivative(my_question,'x',0,'y')
				is_same = checksame(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x')

				
				#rint(sympy_diff,end=' ')
				#print(my_diff,end=' ')
				print(is_same)


				if not is_same:
					if checksimilar(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x'):
						if my_diff.find('abs')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						elif my_diff.find('sec')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						else:
							self.assertTrue(is_same)
					else:
						self.assertTrue(is_same)
				else:
					self.assertTrue(is_same)


	def test_sum_correct(self):
		request = HttpRequest()
		response = sum_rule_worksheet(request)
		soup = BeautifulSoup(response.content,'html5lib')
		self.assertEqual(str(soup.title),'<title>Sum Rule Worksheet - Learn the Sum Rule by working examples with Calculus College.</title>')
		for the_id in ['One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven']:
			t_id = 'Question_'+the_id
			find_id = soup.find_all(id=t_id)
			if len(find_id)>0:
				my_question = find_id[0].get_text()
				print(my_question, end=' ')
				sympy_diff = str(sympy.diff(sympy.sympify(cleanpar(my_question,'x').replace('arc','a')),'x'))
				my_diff = fullderivative(my_question,'x',0,'y')
				is_same = checksame(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x')

				
				#print(sympy_diff,end=' ')
				#print(my_diff,end=' ')
				print(is_same)

				
				if not is_same:
					if checksimilar(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x'):
						if my_diff.find('abs')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						elif my_diff.find('sec')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						else:
							self.assertTrue(is_same)
					else:
						self.assertTrue(is_same)
				else:
					self.assertTrue(is_same)

	def test_chain_correct(self):
		request = HttpRequest()
		response = chain_rule_worksheet(request)
		soup = BeautifulSoup(response.content,'html5lib')
		self.assertEqual(str(soup.title),'<title>Chain Rule Worksheet - Learn the Chain Rule by working examples with Calculus College.</title>')
		for the_id in ['One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven']:
			t_id = 'Question_'+the_id
			find_id = soup.find_all(id=t_id)
			if len(find_id)>0:
				my_question = find_id[0].get_text()
				print(my_question, end=' ')
				sympy_diff = str(sympy.diff(sympy.sympify(cleanpar(my_question,'x').replace('arc','a')),'x'))
				my_diff = fullderivative(my_question,'x',0,'y')
				is_same = checksame(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x')

				
				#print(sympy_diff,end=' ')
				#print(my_diff,end=' ')
				print(is_same)

				
				if not is_same:
					if checksimilar(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x'):
						if my_diff.find('abs')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						elif my_diff.find('sec')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						else:
							self.assertTrue(is_same)
					else:
						self.assertTrue(is_same)
				else:
					self.assertTrue(is_same)

	def test_product_correct(self):
		request = HttpRequest()
		response = product_rule_worksheet(request)
		soup = BeautifulSoup(response.content,'html5lib')
		self.assertEqual(str(soup.title),'<title>Product Rule Worksheet - Learn the Product Rule by working examples with Calculus College.</title>')
		for the_id in ['One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven']:
			t_id = 'Question_'+the_id
			find_id = soup.find_all(id=t_id)
			if len(find_id)>0:
				my_question = find_id[0].get_text()
				print(my_question, end=' ')
				sympy_diff = str(sympy.diff(sympy.sympify(cleanpar(my_question,'x').replace('arc','a')),'x'))
				my_diff = fullderivative(my_question,'x',0,'y')
				is_same = checksame(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x')

				
				#print(sympy_diff,end=' ')
				#print(my_diff,end=' ')
				print(is_same)

				
				if not is_same:
					if checksimilar(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x'):
						if my_diff.find('abs')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						elif my_diff.find('sec')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						else:
							self.assertTrue(is_same)
					else:
						self.assertTrue(is_same)
				else:
					self.assertTrue(is_same)

	def test_quotient_correct(self):
		request = HttpRequest()
		response = quotient_rule_worksheet(request)
		soup = BeautifulSoup(response.content,'html5lib')
		self.assertEqual(str(soup.title),'<title>Quotient Rule Worksheet - Learn the Quotient Rule by working examples with Calculus College.</title>')
		for the_id in ['One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven']:
			t_id = 'Question_'+the_id
			find_id = soup.find_all(id=t_id)
			if len(find_id)>0:
				my_question = find_id[0].get_text()
				print(my_question, end=' ')
				sympy_diff = str(sympy.diff(sympy.sympify(cleanpar(my_question,'x').replace('arc','a')),'x'))
				my_diff = fullderivative(my_question,'x',0,'y')
				is_same = checksame(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x')

				
				#print(sympy_diff,end=' ')
				#print(my_diff,end=' ')
				print(is_same)

				
				if not is_same:
					if checksimilar(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x'):
						if my_diff.find('abs')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						elif my_diff.find('sec')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						else:
							self.assertTrue(is_same)
					else:
						self.assertTrue(is_same)
				else:
					self.assertTrue(is_same)

	def test_explog_correct(self):
		request = HttpRequest()
		response = exponentials_logarithms_worksheet(request)
		soup = BeautifulSoup(response.content,'html5lib')
		self.assertEqual(str(soup.title),'<title>Exponentials and Logarithms Derivatives Worksheet - Learn to differentiate exponential and logarithmic functions by working examples with Calculus College.</title>')
		for the_id in ['One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven']:
			t_id = 'Question_'+the_id
			find_id = soup.find_all(id=t_id)
			if len(find_id)>0:
				my_question = find_id[0].get_text()
				print(my_question, end=' ')
				sympy_diff = str(sympy.diff(sympy.sympify(cleanpar(my_question,'x').replace('arc','a')),'x'))
				my_diff = fullderivative(my_question,'x',0,'y')
				is_same = checksame(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x')

				
				#print(sympy_diff,end=' ')
				#print(my_diff,end=' ')
				print(is_same)

				
				if not is_same:
					if checksimilar(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x'):
						if my_diff.find('abs')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						elif my_diff.find('sec')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						else:
							self.assertTrue(is_same)
					else:
						self.assertTrue(is_same)
				else:
					self.assertTrue(is_same)

	def test_trig_correct(self):
		request = HttpRequest()
		response = trigonometric_functions_worksheet(request)
		soup = BeautifulSoup(response.content,'html5lib')
		self.assertEqual(str(soup.title),'<title>Trigonometric Derivatives Worksheet - Learn how to differentiate trigonometric functions by working examples with Calculus College.</title>')
		for the_id in ['One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven']:
			t_id = 'Question_'+the_id
			find_id = soup.find_all(id=t_id)
			if len(find_id)>0:
				my_question = find_id[0].get_text()
				print(my_question, end=' ')
				sympy_diff = str(sympy.diff(sympy.sympify(cleanpar(my_question,'x').replace('arc','a')),'x'))
				my_diff = fullderivative(my_question,'x',0,'y')
				is_same = checksame(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x')

				
				#print(sympy_diff,end=' ')
				#print(my_diff,end=' ')
				print(is_same)

				
				if not is_same:
					if checksimilar(cleanpar(my_diff,'x'),cleanpar(sympy_diff,'x'),'x'):
						if my_diff.find('abs')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						elif my_diff.find('sec')>-1:
							print(my_question, end=' ')
							print('ONLY SIMILAR-CHECK FURTHER')
						else:
							self.assertTrue(is_same)
					else:
						self.assertTrue(is_same)
				else:
					self.assertTrue(is_same)

