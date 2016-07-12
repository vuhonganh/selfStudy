class Parent():
	def __init__(self, last_name):
		self.m_last_name = last_name

	def show_info(self):
		print("Last Name - " + self.m_last_name)

class Child(Parent):
	def __init__(self, last_name, nb_of_toys):
		Parent.__init__(self, last_name)
		self.m_nb_of_toys = nb_of_toys

	def show_info(self):
		Parent.show_info(self)
		print("Number of toys - " + str(self.m_nb_of_toys))

billy_cyrus = Parent("Cyrus")
miley_cyrus = Child("Cyrus", 5)

miley_cyrus.show_info()
