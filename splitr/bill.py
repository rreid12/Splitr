import math
from contributor import Contributor

class Bill(object):
	def __init__(self, total=0.0):
		self.total = total
		self.contributors = []
		self.contributions = []

	def add_contributor(self, roommate):
		self.contributors.append(roommate)

	def split(self):
		even_split = True

		percentage = 1.0 / len(self.contributors)
		contribution = percentage * self.total

		if self.digits_after_decimal(contribution) > 2:
			print('Extra penny: {extra}'.format(extra=self.currency_round_up(contribution, 2)))

		print('The rest will pay: {regular}'.format(regular=self.currency_round_down(contribution, 2)))

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
cons = [Contributor(), Contributor()]
bill = Bill(34.33)


for con in cons:
	bill.add_contributor(con)

bill.split()