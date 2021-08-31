import os
import csv
import sqlite3
from sqlite3 import Error
from time import sleep
from random import randint
from browser import Browser
database = "database.db"
# Login url of instagram
logInUrl='https://www.instagram.com/accounts/login/?'
# Create connection with the database
def createConnection(dbFile):

    """
    Create a database connection to the SQLite database specified by db_file
    Args:
    dbFile(str): database file
    Return: Connection object or None
    """
    try:
        return sqlite3.connect(dbFile)
    except Error as e:
        print(e)
# Get all data from table
def getTableData():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM urlInfo")
        return cur.fetchall()
    except Error as e:
        print(e)
    return list()
#Update table data
def updateTableData(url):
    try:
        conn.execute(f"UPDATE urlInfo SET scraped = 1 WHERE url = '{url}'")
        conn.commit()
    except Error as e:
        print(e)
# Program to check all files present or not in the program directory
def checkAllFiles():
    # Check whether url file exists in the program folder or not
    if not os.path.exists(database):
        print('Database File Not Found\nProgram Existing')
        exit(0)
        # Check chrome driver exists in the folder or not
    if not os.path.exists('chromedriver.exe'):
        print('Chromedriver not found in the folder\nProgram Existing')
        exit(0)
    # Opening file and reading login detail
# Function to write csv file
def writeCsvFile(filePath,username):
    try:
        with open(filePath, 'a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username])
    except Exception as exc:
        print('Exception Occured while writing csv file : ',exc)
# Function to perfrom login on the instagram
def performLogin()->bool:
    input('Afer entering login details Press Enter-> ')
    return True
# Calling function to check whether all files exits or not 
checkAllFiles()
conn = createConnection(database)
# create tables
if conn is not None:
    filePath=input('Enter Output filename[Example:output] -> ')
    if not filePath:
        print('Output path not entered\nProgram Existing')
        exit(0)
    # Getting all table data
    data=getTableData()
    browser=Browser()
    browser.startBrowser('chromedriver.exe',logInUrl,userAgent=Browser.Chrome_UserAgent)
    browser.driver.implicitly_wait(20)
    sleep(4)
    if performLogin():
        # Scraping urls to get user names
        idx=0
        for url,val in data:
            try:
                # To check string is empty or not
                if val==False:
                    browser.getPage(url)
                    browser.driver.implicitly_wait(20)
                    userName=browser.driver.find_element_by_tag_name('header').text
                    userName=userName.split('\n')[0]
                    writeCsvFile(filePath+'.csv',userName)
                    updateTableData(url)
                    sleep(randint(1,4))
            except Exception as exc:
                print("[EXCEPTION OCCRED] : ",exc)
                choice=input("\nException Occured\nDo you want to continue or not(y|n) ->")
                if choice=='n':
                    break
            idx+=1
    else:
        print('Email or Password Not Correct\nOr\nEmail or Password Input Field Not Found\nProgram Existing')
    browser.driver.close()
else:
    print("Error! cannot create the database connection.")
# Closing database connection
conn.close()
print('Program Ended')
