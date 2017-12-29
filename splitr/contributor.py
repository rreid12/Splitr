import os

class Contributor(object):

	static_id = 0

	def __init__(self, name=0):
		Contributor.static_id += 1
		self.name = Contributor.static_id
		self.bills = []

	def __repr__(self):
		return "Contributor {id}".format(id=self.name)

	def add_bill(self, bill):
		self.bills.append(bill)


