import os, math
from random import randint
from contributor import Contributor

class Bill(object):

	def __init__(self, total=0.0):
		self.total = total
		self.contributions = {}

	def __repr__(self):
		return "Bill total: {total}".format(total=self.total)

	def add_contributor(self, contributor):
		self.contributions[contributor] = None
		contributor.add_bill(self)

	def even_split(self):
		ways_split = len(self.contributions)
		percentage_contribution = 1.0 / ways_split
		payment_per_contributor = percentage_contribution * self.total
		payment_per_contributor = self.currency_round_down(payment_per_contributor, 2)
		contributors = self.contributions.keys()

		for con in contributors:
			self.contributions[con] = payment_per_contributor

		incomplete_total = payment_per_contributor * ways_split
		extra_pennies = int(round((self.total - incomplete_total) / 0.01))
		print(extra_pennies)
		random_number = randint(0, len(contributors)-1)

		for x in range(extra_pennies):
			print(random_number)
			self.contributions[contributors[random_number]] += 0.01
			del contributors[random_number]
			random_number = randint(0, len(contributors)-1)


	def currency_round_up(self, num, places):
		return math.ceil(num * 10**places) / 10**places

	def currency_round_down(self, num, places):
		return math.floor(num * 10**places) / 10**places

	def digits_after_decimal(self, cont):
		s = str(cont)
		if not '.' in s:
			return 0
		return len(s) - s.index('.') - 1



#Testing
num = 7
bill = Bill(341.37)

for x in range(num):
	cont = Contributor()
	bill.add_contributor(cont)

bill.even_split();



for key in bill.contributions:
	print('{contributor} has to pay the following bills: {bills}. They are responsible for the following: {amount}'.format(contributor=key, bills=key.bills, amount=bill.contributions[key]))