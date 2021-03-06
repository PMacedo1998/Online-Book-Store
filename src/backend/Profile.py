import "PaymentMethod.py"
import "UserType.py"

class Profile():
	string firstName
	string lastName
	int phoneNum
	string email
	string password
	string shippingAddress = None
	PaymentMethod paymentMethod = None
	UserType userType
	string verificationCode

	def __init__(firstName, lastName, phoneNum, email, password, shippingAddress, paymentMethod, userType):
		this.firstName = firstName
		this.lastName =lastName
		this.phoneNum = phoneNum
		this.email = email
		this.password = password
		this.shippingAddress = shippingAddress
		this.paymentMethod = paymentMethod
		this.userType = userType

	def getName():
		return f'{this.firstName} {this.lastName}'

	def getPhoneNumber():
		return this.phoneNum

	def getEmail():
		return this.email

	def getPassword():
		return this.password

	def getAddress():
		return this.shippingAddress

	def getPaymentMethod():
		return this.paymentMethod

	def getType():
		return this.userType

	def getVerificationCode():
		return verificationCode

	def updateName(firstName, lastName):
		this.firstName = firstName
		this.lastName = lastName

	def updatePhoneNumber(phoneNum):
		this.phoneNum = phoneNum

	def updateEmail(email):
		this.email = email

	def updatePassword(password):
		this.password = password

	def updateAddress(address):
		this.shippingAddress = address

	def updatePaymentMethod(paymentMethod):
		this.paymentMethod = paymentMethod

	def updateUserType(userType):
		this.userType = userType