import "Profile.py"
import ShoppingCart

class RegisteredUser():
	string status
	int accountID
	Profile profile
	ShoppingCart cart
	bool promoStatus

	def logout():
		pass
		# TODO implement

	def addToCart(b):
		pass
		# TODO implement

	def resetPassword(password):
		profile.updatePassword(password)

	def returnBook(b):
		pass
		# TODO implement

	def getProfile():
		return profile

	def getOrderHistory():
		pass
		# TODO implement

	def getCart():
		return cart

	def getPromoStatus():
		return promoStatus

	def updatePromoStatus(promoStatus):
		this.promoStatus = promoStatus

	def updateCart()
		pass 
		# TODO implement