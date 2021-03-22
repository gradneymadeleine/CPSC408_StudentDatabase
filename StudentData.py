import sqlite3
import pandas as pd
from pandas import DataFrame

#Opens up database and cursor and closes when the user wants to end the program
conn = sqlite3.connect('/Users/madeleinegradney/Desktop/pythonProject1/StudentDB.db') #establish my connection
mycursor = conn.cursor() #the cursor allows python to execute sql statements

#displays all students
def displayStudents():
    print("| • Display All Students • |")
    mycursor.execute("SELECT * FROM Student;")
    students = mycursor.fetchall()
    #shows all of the rows and columns
    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
    frame = DataFrame(students,
                   columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City',
                            'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted'])
    print(frame)
    question = int(input(
        "Would you like to: \n1) Add Students \n2) Update Student \n3) Delete Student \n4) Search for Student by Major, GPA, and Address, \n5) Exit \nInput: \n"))
    if question == 1:
        addStudent()

    elif question == 2:
        updateStudent()

    elif question == 3:
        deleteStudent()

    elif question == 4:
        searchStudents()

    elif question == 5:
        print("Goodbye")
        conn.commit()
        conn.close()
        print("disconnected from database")

    else:
        print("Error, invalid input")
        displayStudents()



#Function that allows you to add a new student
def addStudent():
    print("| • Add Student • |")
    firstName = input("Enter the student's first name: ")
    lastName = input("Enter the student's last name: ")
    gpa = input("Enter a GPA: ")
    #need to make sure gpa is numerical value
    while (gpa.isalpha() == True):
        gpa = input("Error. Please try again and enter a numerical value for GPA: ")
    gpa = float(gpa)
    major = input("Enter a major: ")
    facultyAdvisor = input("Enter the faculty advisor: ")
    address = input("Enter an address: ")
    city = input("Enter a city: ")
    state = input("Enter a state: ")
    zipCode = input("Enter a zipcode: ")
    #zip code should not have alpha characters so check for that
    while (zipCode.isalpha() == True):
        zipCode = input("Error. Please input digits only for the zipcode: ")
    phoneNumber = input("Enter a mobile phone number: ")
    mycursor.execute(
        "INSERT INTO Student(FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (firstName, lastName, gpa, major, facultyAdvisor, address, city, state, zipCode, phoneNumber))
    conn.commit()
    print("Added", firstName," ", lastName)
    question = int(input(
        "Would you like to: \n1) Display Students \n2) Update Student \n3) Delete Student \n4) Search for Student by Major, GPA, and Address, \n5) Exit \nInput: \n"))
    if question == 1:
        displayStudents()

    elif question == 2:
        updateStudent()

    elif question == 3:
        deleteStudent()

    elif question == 4:
        searchStudents()

    elif question == 5:
        print("Goodbye")
        conn.commit()
        conn.close()
        print("disconnected from database")

    else:
        print("Error, invalid input")
        addStudent()
#soft delete
def deleteStudent():
    print("| • Delete Student • |")
    studId = input("Enter StudentId: ")
    mycursor.execute("UPDATE Student SET isDeleted = 1 WHERE StudentId = ?", [studId])
    conn.commit()
    print("Student deleted")
    question = int(input(
        "Would you like to: \n1) Display Students \n2) Add Student \n3) Update Student \n4) Search for Student by Major, GPA, and Address, \n5) Exit \nInput: \n"))
    if question == 1:
        displayStudents()

    elif question == 2:
        addStudent()

    elif question == 3:
        updateStudent()

    elif question == 4:
        searchStudents()

    elif question == 5:
        print("Goodbye")
        conn.commit()
        conn.close()
        print("disconnected from database")

    else:
        print("Error, invalid input")
        deleteStudent()


#Function that updates a student's information
def updateStudent():
    print("| • Update Student • |")
    check = False
    while (check == False):
        studID = input("Enter the student ID for which student's info you would like to update: ")
        mycursor.execute("SELECT * FROM Student WHERE StudentId = ?", [studID])
        data = mycursor.fetchall()
        # If the ID the user entered does not exsit in the table, then they need to keep trying again until they get it right
        if data == []:
            print("Student ID entered is invalid, please try again.")
            continue
        else:
            check = True
            choose = int(
                input("What do you want to update?\n1) Major \n2) Faculty Advisor \n3) Phone Number \n Input: \n"))
            if choose == 1:
                mInput= input("Enter a new major: ")
                mycursor.execute("UPDATE Student SET Major = ? WHERE StudentId = ?",(mInput, studID))
                conn.commit()
                print("Successfully updated the student's major")
            if choose == 2:
                faInput = input("Enter a new faculty advisor: ")
                mycursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?", (faInput, studID))
                conn.commit()
                print("Successfully updated the student's advisor ")
            if choose == 3:
                pInput = input("Enter new phone number: ")
                mycursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?", (pInput, studID))
                conn.commit()
                print("Successfully updated the student's number")
                break
    question = int(input(
        "Would you like to: \n1) Display Students \n2) Add Student \n3) Delete Student \n4) Search for Student by Major, GPA, and Address, \n5) Exit \n Input: \n"))
    if question == 1:
        displayStudents()

    elif question == 2:
        addStudent()

    elif question == 3:
        deleteStudent()

    elif question == 4:
        searchStudents()

    elif question == 5:
        print("Goodbye")
        conn.commit()
        conn.close()
        print("disconnected from database")

    else:
        print("Error, invalid input.")
        updateStudent()


#Function that lets you display by a specific field
def searchStudents():
    check = True
    while (check):
        print("How would you like to display students by? ")
        search = int(input("1) GPA \n2) Major \n3) Faculty Advisor \n4) City  \n5) State \n"))

        # GPA
        if (search == 1):
            check= False
            # unique GPAs
            mycursor = conn.execute("SELECT DISTINCT GPA FROM Student")
            info = mycursor.fetchall()
            print("Unique GPAs: ", info)
            doubleCk = False
            while (doubleCk == False):
                gpa = input("Enter a GPA: ")
                mycursor.execute("SELECT * FROM Student WHERE GPA = ?", [gpa])
                # need to check for specific GPA
                showGPA = mycursor.fetchall()
                # if GPA is not found
                if showGPA == []:
                    print("GPA not found, please try again.")
                    continue
                else:
                    doubleCk = True
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    frame = DataFrame(showGPA,
                                      columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor',
                                               'Address', 'City',
                                               'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted'])
                    print(frame)
                    break

        #Major
        elif (search == 2):
            check = False
            mycursor = conn.execute("SELECT DISTINCT Major FROM Student")
            info = mycursor.fetchall()
            print("Majors: ", info)
            #need to check specific major
            doubleCk = False
            while (doubleCk == False):
                major = input("Enter a major: ")
                mycursor.execute("SELECT * FROM Student WHERE Major = ?", [major])
                showMajors = mycursor.fetchall()
                # check if major is there
                if showMajors == []:
                    print("Major not found, please try again.")
                    continue
                else:
                    doubleCk = True
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    frame = DataFrame(showMajors,
                                   columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor',
                                            'Address', 'City',
                                            'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted'])
                    print(frame)
                    break

        # advisor
        elif (search == 3):
            check = False
            mycursor = conn.execute("SELECT DISTINCT FacultyAdvisor FROM Student")
            info = mycursor.fetchall()
            print("Faculty Advisors: ", info)
            # check if advisor is not found
            doubleCk = False
            while (doubleCk == False):
                advisor = input("Enter an advisor you would like to see records for: ")
                mycursor.execute("SELECT * FROM Student WHERE FacultyAdvisor = ?", [advisor])
                showAdvisors = mycursor.fetchall()
                # If the advisor the user entered does not exsit in the table, then they need to keep trying again until they get it right
                if showAdvisors == []:
                    print("Advisor not found, please try again.")
                    continue
                else:
                    doubleCk = True
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    frame = DataFrame(showAdvisors,
                                   columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor',
                                            'Address', 'City',
                                            'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted'])
                    print(frame)
                    break


        #city
        elif (search == 4):
            check = False
            mycursor = conn.execute("SELECT DISTINCT City FROM Student")
            info = mycursor.fetchall()
            print("Cities: ", info)
            #check specific city
            doubleCk = False
            while (doubleCk == False):
                city = input("Enter a city: ")
                mycursor.execute("SELECT * FROM Student WHERE City = ?", [city])
                showCity = mycursor.fetchall()
                #If city is not found
                if showCity == []:
                    print("City not found, please try again.")
                    continue
                else:
                    doubleCk = True
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    frame = DataFrame(showCity,
                                   columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor',
                                            'Address', 'City',
                                            'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted'])
                    print(frame)
                    break
        #state
        elif (search== 5):
            check = False
            #unique states --> so there are no repeats
            mycursor = conn.execute("SELECT DISTINCT State FROM Student")
            info = mycursor.fetchall()
            print("States: ", info)
            #check for specific States
            doubleCk = False
            while (doubleCk == False):
                state = input("Enter a state you would like to see records for: ")
                mycursor.execute("SELECT * FROM Student WHERE State = ?", [state])
                showStates = mycursor.fetchall()
                #If state is not found
                if showStates == []:
                    print("This state doesn't exist, please try again.")
                    continue
                else:
                    doubleCk = True
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    frame = DataFrame(showStates,
                                   columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor',
                                            'Address', 'City',
                                            'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted'])
                    print(frame)
                    break

        else:
            print("Invalid input, please try again.")

    question = int(input(
        "Would you like to: \n1) Display Students \n2) Add Student \n3) Delete Student \n4) Search for Student by Major, GPA, and Address, \n5) Exit \n Input: \n"))
    if question == 1:
        displayStudents()

    elif question == 2:
        addStudent()

    elif question == 3:
        deleteStudent()

    elif question == 4:
        updateStudent()

    elif question == 5:
        print("Goodbye")
        conn.commit()
        conn.close()
        print("disconnected from database")

    else:
        print("Error, invalid input.")
        searchStudents()

#Function that prints out menu during each iteration
def GUI():
    print("|• • • Chapman University's Student Database • • •|")
    question = int(input(
        "Input the number of the option you want to see: \n1) Display Students \n2) Add Student \n3) Delete Student \n4) Update Student \n5) Search for Student by Major, GPA, and Address, \n6) Exit\n Input: "))
    if question == 1:
        displayStudents()
    elif question == 2:
        addStudent()
    elif question == 3:
        deleteStudent()
    elif question == 4:
        updateStudent()
    elif question == 5:
        searchStudents()
    else:
        print("Not a valid input")
        print("Please try again")
        GUI()



#Function that reads in the CSV file
def readInCSV():
    # import data from csv
    mycursor = conn.execute("SELECT * FROM Student")
    data = mycursor.fetchall()
    #Only import the csv if the table is empty otherwise it will repeat rows and values every time you run it
    if (data  == []):
        with open("./students.csv") as file:
            num_records = 0
            for row in file:
                if num_records != 0:
                    mycursor.execute(
                        "INSERT INTO Student(FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA) VALUES (?,?,?,?,?,?,?,?,?)",
                        row.split(","))
                    conn.commit()
                num_records += 1

