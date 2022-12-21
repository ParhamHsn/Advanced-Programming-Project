import database as d
class application:
	def main():
		print("Hello Welcome To Application")
		print("1) Creat New User")
		print("2) Login To Application")
		print("3) Exit Application")
		x = input("Please Enter A Number : ")
		if x == "1":
			name = input("Please Enter Your Name : ")
			nationalcode = input("Please Enter Your National Code : ")
			password = input("Please Enter Your Password : ")
			phone = input("Please Enter Your Phone : ")
			email = input("Please Enter Your Email : ")
			if " " in name or " " in nationalcode or " " in password or " " in phone or " " in email:
				print("No Space Supported In Informations ! Please Try Again !")
				application.main()
			if name == "" or nationalcode == "" or password == "" or phone == "" or email == "":
				print("No Empty Entry Supported ! Please Try Again !")
				application.main()
			query = "$ INSERT INTO Users VALUES (" + name + "," + nationalcode + ","  + password + ","  + phone + "," + email + ");"
			query = d.sql(query)
			query.mainCheck()
			if query.error == 0:				
				print("Thank You! Your Registration Was Successful!")
			application.main()
		elif x == "2":
			nationalcode = input("Please Enter Your National Code : ")
			password = input("Please Enter Your Password : ")
			condition = "nationalcode == '" + nationalcode + "' AND password == '" + password +"'"
			indx = d.sql.check("Users" , condition)
			if len(indx) == 0:
				print("Your National Code Or Password Is Incorrect !")
				application.main()
			else:
				print("You Have Successfuly Logged In !")
				login.main(nationalcode)
		else:
			import os
			os._exit(0)
class login():
	def main(nationalcode):
		print("1) Creat A New Bank Account")
		print("2) Show Details Of Your Accounts")
		print("3) Define Common Bank Accounts")
		print("4) Transfer Money")
		print("5) Paying Your Bills")
		print("6) Request For A Loan")
		print("7) Close A Bank Account")
		print("8) Logout")
		x = input("Please Enter A Number : ")
		if x == "1":
			login.creatAccount(nationalcode)
		elif x == "2":
			login.showDetails(nationalcode)
		elif x == "3":
			login.commonAccounts(nationalcode)
		elif x == "4":
			login.transfer(nationalcode)
		elif x == "5":
			login.bill(nationalcode)
		elif x == "6":
			login.requestLoan(nationalcode)
		elif x == "7":
			login.closeAccount(nationalcode)
		elif x == "8":
			application.main()
		else:
			login.main(nationalcode)
	def generateAccount():
		import random
		string = ""
		for i in range(0,10):
			a = random.randint(0,9)
			string += str(a)
		return(string)	
	def creatAccount(nationalcode):
		alias = input("Please Enter An Alias For Your New Bank Account : ")
		password = input("Please Enter A Password For Your New Account : ")
		money = input("Please Enter Your Initial Amount Of Money For Your New Account : ")
		accountNumber = login.generateAccount()
		if " " in alias or " " in password or " " in money:
			print("No Space Supported In Informations ! Please Try Again !")
		if alias == "" or password == "" or accountNumber == "":
			print("No Empty Entry Supported ! Please Try Again !")
		query = "$ INSERT INTO BankAccounts VALUES (" + nationalcode + "," + alias + ","  + password + ","  + money + "," + accountNumber + ");"
		query = d.sql(query)
		query.mainCheck()
		if query.error == 0:				
				print("Thank you! Your New Bank Account Was Submitted Successfuly!")
				print("Your Account Number Is :",accountNumber)
				print("Your Alias Is :",alias)
		login.main(nationalcode)
	def showDetails(nationalcode):
		print("Here Are Your Accounts")
		query = "$ SELECT FROM BankAccounts WHERE nationalcode == '" + nationalcode + "';"
		query = d.sql(query)
		l = query.mainCheck()
		if len(l) == 1:
			print("Can't Find Any Bank Accounts !")
			login.main(nationalcode)
		else:
			for i in l:
				print(i.split()[2],i.split()[4],i.split()[5])
		print("Do You Want To See Your Transactions ?")
		print("1) Yes")
		print("2) No")
		x = input("Please Enter A Number : ")
		if x == "1":
			accountNumber = input("Please Enter Your Account Number From Above List : ")
			query = "$ SELECT FROM BankAccounts WHERE accountNumber == '" + accountNumber + "' AND nationalcode == '" + nationalcode +"';"
			query = d.sql(query)
			l = query.mainCheck()
			if len(l) == 1:
				print("This Account Number Is Not Yours ! Please Try Again !")
				login.showDetails(nationalcode)
			else:
				query = "$ SELECT FROM Transactions WHERE From == '" + accountNumber + "' OR To == '"+ accountNumber + "';"
				query = d.sql(query)
				l = query.mainCheck()
				if len(l) == 1:
					print("Can't Find Any Transactions !")
					login.main(nationalcode)
				else:
					for i in range(len(l)):
						s = l[i].split()[1:]
						for j in range(len(s)):
							if s[j] == accountNumber:
								if j == 0:
									t = "-"
								elif j == 1:
									t = "+"
							if j != 2 or i == 0:
								print(s[j],end=" ")
							else:
								print(t+s[j],end=" ")
						print("")
		else:
			login.main(nationalcode)
		login.main(nationalcode)
	def commonAccounts(nationalcode):
		accountNumber = input("Please Enter The Account Number : ")
		query = "$ SELECT FROM BankAccounts WHERE accountNumber == '" + accountNumber + "';"
		query = d.sql(query)
		l = query.mainCheck()
		if len(l) == 1:
			print("Can't Find Any Account Number !")
			print("Please Try Again !")
			login.commonAccounts(nationalcode)
		query = "$ SELECT FROM BankAccounts WHERE accountNumber == '" + accountNumber + "' AND nationalcode == '" + nationalcode + "';"
		query = d.sql(query)
		l = query.mainCheck()
		if len(l) == 1:
			alias = input("Enter Alias For Account Number : ")
			query = "$ INSERT INTO CommonAccounts VALUES (" + nationalcode + "," + accountNumber + ","  + alias + ");"
			query = d.sql(query)
			query.mainCheck()
			print("Account Number :",accountNumber,"With Alias :",alias,"Added To Your Common Accounts !")
		else:
			alias = l[1].split()[2]
			query = "$ INSERT INTO CommonAccounts VALUES (" + nationalcode + "," + accountNumber + ","  + alias + ");"
			query = d.sql(query)
			query.mainCheck()
			print("Account Number :",accountNumber,"With Alias :",alias,"Added To Your Common Accounts !")
		login.main(nationalcode)
	def transfer(nationalcode):
		print("How Do You Want To Choose Your Source Account")
		print("1) Choose From My Common Bank Accounts")
		print("2) Enter Account Number Manually")
		x = input("Please Enter A Number : ")
		if x == "1":
			query = "$ SELECT FROM CommonAccounts WHERE nationalcode == '" + nationalcode + "';"
			query = d.sql(query)
			l = query.mainCheck()
			for i in l:
				print(i.split()[3])
			alias = input("Please Enter The Alias From Above List : ")
			cnt = 0
			for i in l:
				if i.split()[3] == alias:
					cnt += 1
					accountNumberSource = i.split()[2]
			if cnt == 0:
				print("Alias Not Found ! Please Try Again !")
				login.transfer(nationalcode)
			query = "$ SELECT FROM BankAccounts WHERE nationalcode == '" + nationalcode + "' AND accountNumber == '"+ accountNumberSource +"';"
			query = d.sql(query)
			l = query.mainCheck()
			if len(l) == 1:
				print("This Bank Account Is Not Yours ! Please Try Again !")
				login.transfer(nationalcode)
		elif x == "2":
			accountNumberSource = input("Please Enter Your Source Account Number : ")
			query = "$ SELECT FROM BankAccounts WHERE nationalcode == '" + nationalcode + "' AND accountNumber == '"+ accountNumberSource +"';"
			query = d.sql(query)
			l = query.mainCheck()
			if len(l) == 1:
				print("Can't Find Your Bank Account ! Please Try Again !")
				login.transfer(nationalcode)
		else:
			login.main(nationalcode)		
		price = input("Please Enter The Price You Want To Transfer : ")
		password = input("Please Enter Your Bank Account Password : ")
		if password != l[1].split()[3]:
			print("Your Password Is Incorrect ! Please Try Again !")
			login.transfer(nationalcode)
		if int(l[1].split()[4]) - int(price) < 0:
			print("Your Account Money Is Not Enough ! Please Try Again !")
			login.transfer(nationalcode)
		print("How Do You Want To Choose Destination Account")
		print("1) Choose From My Common Bank Accounts")
		print("2) Enter Account Number Manually")
		x = input("Please Enter A Number : ")
		if x == "1":
			query = "$ SELECT FROM CommonAccounts WHERE nationalcode == '" + nationalcode + "';"
			query = d.sql(query)
			l = query.mainCheck()
			for i in l:
				print(i.split()[3])
			alias_Dest = input("Please Enter The Alias From Above List : ")
			cnt = 0
			for i in l:
				if i.split()[3] == alias_Dest:
					cnt += 1
					accountNumberDest = i.split()[2]
			if cnt == 0:
				print("Alias Not Found ! Please Try Again !")
				login.transfer(nationalcode)
			if accountNumberSource == accountNumberDest:
				print("Source And Destination Are Same ! Please Try Again !")
				login.transfer(nationalcode)

			query = "$ SELECT FROM BankAccounts WHERE accountNumber == '"+ accountNumberSource +"';"
			query = d.sql(query)
			l = query.mainCheck()
			s = l[1].split()
			new_money = int(s[4]) - int(price)
			new_money = str(new_money)
			s[4] = new_money
			new_values = ",".join(s[1:])
			query = "$ UPDATE BankAccounts WHERE accountNumber == '" + accountNumberSource + "' VALUES (" + new_values + ");"
			query = d.sql(query)
			query.mainCheck()

			query = "$ SELECT FROM BankAccounts WHERE accountNumber == '"+ accountNumberDest +"';"
			query = d.sql(query)
			l = query.mainCheck()
			s = l[1].split()
			new_money = int(s[4]) + int(price)
			new_money = str(new_money)
			s[4] = new_money
			new_values = ",".join(s[1:])
			query = "$ UPDATE BankAccounts WHERE accountNumber == '" + accountNumberDest + "' VALUES (" + new_values + ");"
			query = d.sql(query)
			query.mainCheck()
		elif x == "2":
			accountNumberDest = input("Please Enter Destination Account Number : ")
			query = "$ SELECT FROM BankAccounts WHERE accountNumber == '"+ accountNumberDest +"';"
			query = d.sql(query)
			l = query.mainCheck()
			if len(l) == 1:
				print("Can't Find Destination Bank Account ! Please Try Again !")
				login.transfer(nationalcode)
			if accountNumberSource == accountNumberDest:
				print("Source And Destination Are Same ! Please Try Again !")
				login.transfer(nationalcode)

			query = "$ SELECT FROM BankAccounts WHERE accountNumber == '"+ accountNumberSource +"';"
			query = d.sql(query)
			l = query.mainCheck()
			s = l[1].split()
			new_money = int(s[4]) - int(price)
			new_money = str(new_money)
			s[4] = new_money
			new_values = ",".join(s[1:])
			query = "$ UPDATE BankAccounts WHERE accountNumber == '" + accountNumberSource + "' VALUES (" + new_values + ");"
			query = d.sql(query)
			query.mainCheck()

			query = "$ SELECT FROM BankAccounts WHERE accountNumber == '"+ accountNumberDest +"';"
			query = d.sql(query)
			l = query.mainCheck()
			s = l[1].split()
			new_money = int(s[4]) + int(price)
			new_money = str(new_money)
			s[4] = new_money
			new_values = ",".join(s[1:])
			query = "$ UPDATE BankAccounts WHERE accountNumber == '" + accountNumberDest + "' VALUES (" + new_values + ");"
			query = d.sql(query)
			query.mainCheck()
		else:
			login.main(nationalcode)		
		query = "$ INSERT INTO Transactions VALUES (" + accountNumberSource + "," + accountNumberDest + "," + price + ");"
		query = d.sql(query)
		query.mainCheck()
		print("Money Transferred Successfully !")
		login.main(nationalcode)
	def bill(nationalcode):
		Billing_Id = input("Please Enter Billing Id = ")
		Payment_Id = input("Please Enter Payment Id = ")
		import random
		price = random.randint(0,100000)
		print("The Cost Of Your Bill Is :",price)
		accountNumber = input("Please Enter Your Account Number To Pay The Bill : ")
		query = "$ SELECT FROM BankAccounts WHERE accountNumber == '" + accountNumber + "' AND nationalcode == '" + nationalcode +"';"
		query = d.sql(query)
		l = query.mainCheck()
		if len(l) == 1:
			print("This Account Number Is Not Yours ! Please Try Again !")
			login.bill(nationalcode)
		if int(l[1].split()[4]) - price < 0:
			print("Your Account Money Is Not Enough ! Please Try Again !")
			login.bill(nationalcode)
		query = "$ SELECT FROM BankAccounts WHERE accountNumber == '"+ accountNumber +"';"
		query = d.sql(query)
		l = query.mainCheck()
		s = l[1].split()
		new_money = int(s[4]) - price
		new_money = str(new_money)
		s[4] = new_money
		new_values = ",".join(s[1:])
		query = "$ UPDATE BankAccounts WHERE accountNumber == '" + accountNumber + "' VALUES (" + new_values + ");"
		query = d.sql(query)
		query.mainCheck()

		query = "$ INSERT INTO Transactions VALUES (" + accountNumber + "," + "0000000000" + "," + str(price) + ");"
		query = d.sql(query)
		query.mainCheck()
		print("Your Bill Has Been Paid Successfully !")
		login.main(nationalcode)
	def requestLoan(nationalcode):
		money = input("Please Enter The Loan Amount : ")
		accountNumber = input("Please Enter Your Account Number : ")
		query = "$ SELECT FROM BankAccounts WHERE accountNumber == '" + accountNumber + "' AND nationalcode == '" + nationalcode +"';"
		query = d.sql(query)
		l = query.mainCheck()
		if len(l) == 1:
			print("This Account Number Is Not Yours ! Please Try Again !")
			login.requestLoan(nationalcode)

		query = "$ SELECT FROM Loan WHERE accountNumber == '" + accountNumber + "';"
		query = d.sql(query)
		l = query.mainCheck()
		if len(l) != 1:
			print("You Already Have A Loan On This Account Number ! Please Try Again !")
			login.requestLoan(nationalcode)

		query = "$ SELECT FROM BankAccounts WHERE accountNumber == '"+ accountNumber +"';"
		query = d.sql(query)
		l = query.mainCheck()
		s = l[1].split()
		new_money = int(s[4]) + int(money) + int(money)//12
		new_money = str(new_money)
		s[4] = new_money
		new_values = ",".join(s[1:])
		query = "$ UPDATE BankAccounts WHERE accountNumber == '" + accountNumber + "' VALUES (" + new_values + ");"
		query = d.sql(query)
		query.mainCheck()

		query = "$ INSERT INTO Transactions VALUES (0000000000," + accountNumber + "," + money + ");"
		query = d.sql(query)
		query.mainCheck()
		print("The Loan Was Successfully Deposited In Your Bank Account And The Payment Period Is 12.")
		print("That Will Be Deducted From Your Account Every Twenty Seconds.")

		monthlyPayment = str(int(money)//12)
		query = "$ INSERT INTO Loan VALUES (" + nationalcode + "," + accountNumber + "," + money + ",13,12," + monthlyPayment + ");"
		query = d.sql(query)
		query.mainCheck()

		login.main(nationalcode)
	def closeAccount(nationalcode):
		accountNumber = input("Please Enter Your Account Number : ")
		query = "$ SELECT FROM BankAccounts WHERE accountNumber == '" + accountNumber + "' AND nationalcode == '" + nationalcode +"';"
		query = d.sql(query)
		l = query.mainCheck()
		if len(l) == 1:
			print("This Account Number Is Not Yours ! Please Try Again !")
			login.main(nationalcode)
		password = input("Please Enter Your Bank Account Password : ")
		query = "$ SELECT FROM BankAccounts WHERE accountNumber == '" + accountNumber + "' AND password == '" + password +"';"
		query = d.sql(query)
		l = query.mainCheck()
		if len(l) == 1:
			print("Your Password Is Incorrect ! Please Try Again !")
			login.main(nationalcode)
		money = l[1].split()[4]
		if int(money) > 0:
			print("Your Current Money Is",money)
			accountNumberDest = input("Please Enter Destination Account Number : ")

			query = "$ SELECT FROM BankAccounts WHERE accountNumber == '"+ accountNumberDest +"';"
			query = d.sql(query)
			l = query.mainCheck()
			s = l[1].split()
			money = int(money)
			new_money = int(s[4]) + money
			new_money = str(new_money)
			s[4] = new_money
			new_values = ",".join(s[1:])
			query = "$ UPDATE BankAccounts WHERE accountNumber == '" + accountNumberDest + "' VALUES (" + new_values + ");"
			query = d.sql(query)
			query.mainCheck()
			print("The Money Transferred To Destination Account !")

			query = "$ INSERT INTO Transactions VALUES (" + accountNumber + "," + accountNumberDest + "," + str(money) + ");"
			query = d.sql(query)
			query.mainCheck()
			print("Money Transferred Successfully !")
		
		query = "$ DELETE FROM BankAccounts WHERE accountNumber == '" + accountNumber +"';"
		query = d.sql(query)
		query.mainCheck()
		print("Your Account Has Been Deleted Successfully !")
		login.main(nationalcode)

import threading
def computeLoan():
	query = "$ SELECT FROM Loan WHERE paymentPeriod  == '12';"
	query = d.sql(query)
	L = query.mainCheck()
	if len(L) == 1:
		threading.Timer(20.0, computeLoan).start()
	else:
		threading.Timer(20.0, computeLoan).start()
		for i in range(1,len(L)):
			s = L[i].split()
			accountNumber = s[2]
			monthlyPayment = s[6]
			if int(s[4]) == 0:
				query = "$ DELETE FROM Loan WHERE accountNumber == '" + accountNumber +"';"
				query = d.sql(query)
				query.mainCheck()
				continue
			new_rep = int(s[4]) - 1
			new_rep = str(new_rep)
			s[4] = new_rep
			new_values = ",".join(s[1:])
			query = "$ UPDATE Loan WHERE accountNumber == '" + accountNumber + "' VALUES (" + new_values + ");"
			query = d.sql(query)
			query.mainCheck()


			query = "$ SELECT FROM BankAccounts WHERE accountNumber == '"+ accountNumber +"';"
			query = d.sql(query)
			l = query.mainCheck()
			s = l[1].split()
			new_money = int(s[4]) - int(monthlyPayment)
			new_money = str(new_money)
			s[4] = new_money
			new_values = ",".join(s[1:])
			query = "$ UPDATE BankAccounts WHERE accountNumber == '" + accountNumber + "' VALUES (" + new_values + ");"
			query = d.sql(query)
			query.mainCheck()
			

			if new_rep != "12":
				query = "$ INSERT INTO Transactions VALUES (" + accountNumber + "," + "0000000000" + "," + monthlyPayment + ");"
				query = d.sql(query)
				query.mainCheck()

computeLoan()

application.main()

