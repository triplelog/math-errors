from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)
	
	def tearDown(self):
		self.browser.quit()
	
	def test_can_start_something(self):
		self.browser.get('http://159.203.78.14:8000')
		self.assertIn('Calculus College', self.browser.title)
		self.fail('Finish the test!')

if __name__ == '__main__':
	unittest.main(warnings='ignore')
