from datetime import datetime, timedelta, date
import math
vehicles=open("Vehicles.txt","r")
allVehicles=[]
while True:
    line=vehicles.readline()
    line=line.strip()
    if len(line)==0:
        break
    line=line.split(",")
    allVehicles.append(line)
vehicles.close()

def menu1():
    return input("""You may select one of the following:
1) List available cars
2) Rent a car
3) Return a car
4) Count the money
0) Exit
What is your selection?\n""")

def availableCars():
    rented=open("RentedVehicles.txt","r")
    rentedVehicles=[]
    while True:
        line=rented.readline()
        line=line.strip()
        if len(line)==0:
            break
        line=line.split(",")
        rentedVehicles.append(line[0])
    rented.close()
    print("The following cars are available:")
    available=[]
    for x in allVehicles:
        if x[0] not in rentedVehicles:
            print(f"* Reg. nr: {x[0]}, Model: {x[1]}, Price per day: {x[2]}")
            print("Properties: ", end="")
            print(*x[3:], sep=", ")
            available.append(x[0])
    print()
    return available

def customerOrNot(birth):
    cust=open("Customers.txt", "r")
    customers=[]
    firstnames=[]
    while True:
        line=cust.readline()
        line=line.strip()
        if len(line)==0:
            break
        line=line.split(",")
        customers.append(line[0])
        firstnames.append(line[1])
    cust.close()
    if birth in customers:
        return customers, firstnames
    else:
        return False

def validate(date):
        try:
            datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            return False
    
def rentACar():
    while True:
        try:
            available1=available
            regNum = input("Input registration number:\n")
            if regNum not in available1:
                print("Car not available, try again")
            else:
                break
        except:
            return print("Please look at available cars first.")
    while True:
        birthday=input("Input your birthday (DD/MM/YYYY):\n")
        today=date.today()
        val=validate(birthday)
        if val==False:
            print("Wrong birthday format, try again.")
        elif (today.year - datetime.strptime(birthday, "%d/%m/%Y").year -((today.month, today.day) <(datetime.strptime(birthday, "%d/%m/%Y").month, datetime.strptime(birthday, "%d/%m/%Y").day)))>100 or (today.year - datetime.strptime(birthday, "%d/%m/%Y").year -((today.month, today.day) <(datetime.strptime(birthday, "%d/%m/%Y").month, datetime.strptime(birthday, "%d/%m/%Y").day)))<18:
            print("Age isn't between permitted numbers (18-100)")
        else:
            break
    yesno=customerOrNot(birthday)
    if yesno==False:
        first=input("Please input your first name:\n")
        last=input("Please input your last name:\n")
        while True:
            email=input("Please input your email address:\n")
            if "@" in email and "." in email:
                break
            else:print("Wrong email format")
        cust=open("Customers.txt","a")
        cust.write(f"{birthday},{first},{last},{email}\n")
        cust.close()
    else:
        days,names=customerOrNot(birthday)
        c=0
        for x in days:
            if x==birthday:
                first=names[c]
            c+=1
    now=datetime.today()
    now=now.strftime("%d/%m/%Y %H:%M")
    rent=open("RentedVehicles.txt", "a")
    rent.write(f"{regNum},{birthday},{now}\n")
    rent.close()
    print(f"Hello {first}")
    print(f"You rented the car {regNum}")

def returnACar():
    rented=open("RentedVehicles.txt","r")
    while True:
        regNum=input("Input registration number:\n")
        car=[]
        while True:
            line=rented.readline()
            line=line.strip()
            if len(line)==0:
                print("This car does not exist or isn't rented, try again.")
                break
            line=line.split(',')
            if line[0]==regNum:
                car.append(line)
                break
        if car!=[]:
            break
    rented.close()
    veh=open("Vehicles.txt","r")
    price=0
    while True:
        line=veh.readline()
        line=line.strip()
        line=line.split(',')
        if line[0]==regNum:
            price=int(line[2])
            break
    veh.close()
    today=datetime.now()
    rentday=datetime.strptime(car[0][2], "%d/%m/%Y %H:%M")
    rentdays=math.ceil((today-rentday)/ timedelta(hours=1)/24)
    totalprice=int(rentdays)*int(price)
    print(f"The rent lasted {rentdays} days and the cost is {totalprice}.00 euros")
    rented=open("RentedVehicles.txt","r")
    allRented=[]
    while True:
        line=rented.readline()
        line=line.strip()
        if len(line)==0:
            break
        line=line.split(',')
        if line[0]!=regNum:
            allRented.append(','.join(line))
    rented.close()
    rented=open("RentedVehicles.txt","w")
    for x in allRented:
        rented.write(x+"\n")
    rented.close()
    trans=open("transActions.txt","a")
    for x in car[0]:
        trans.write(x+',')
    trans.write(today.strftime("%d/%m/%Y %H:%M")+f',{rentdays},{totalprice}.00\n')
    trans.close()

def countMoney():
    trans=open('transActions.txt','r')
    money=0
    while True:
        line=trans.readline()
        line=line.strip()
        if len(line)==0:
            break
        line=line.split(',')
        money+=round(float(line[-1]))
    print(f'The total amount of money is {money}.00 euros')
    trans.close()

while True:
    menu=menu1()
    if menu=="0":
        break
    elif menu=="1":
        available=availableCars()
    elif menu=="2":
        rentACar()
    elif menu=="3":
        returnACar()
    elif menu=="4":
        countMoney()
    else:print("Choose one of the available options")
    print()