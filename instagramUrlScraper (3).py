import os
import sqlite3
from sqlite3 import Error
from time import sleep
from random import randint
from browser import Browser
hashtag=''
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
# Create table in the data base
def createTable(conn):
    """ create a table
    Args:
    conn: Connection object
    """
    sqlCreateProjectsTable = """
        CREATE TABLE if not exists urlInfo (
        url STRING  PRIMARY KEY,
        scraped BOOLEAN
        );
        """
    try:
        c = conn.cursor()
        c.execute(sqlCreateProjectsTable)
        conn.commit()
    except Error as e:
        print(e)
# Add urls in the table
def addDataIntoTable(conn,url):
    try:
        c = conn.cursor()
        sqliteInsertQuery = """INSERT INTO urlInfo (url,scraped) VALUES (?, ?);"""
        c.execute(sqliteInsertQuery,[url,False])
        conn.commit()
    except:
        pass
# Program to check all files present or not in the program directory
def checkAllFiles():
    # Check chrome driver exists in the folder or not
    if not os.path.exists('chromedriver.exe'):
        print('Chromedriver not found in the folder\nProgram Existing')
        exit(0)
# Function to perfrom login on the instagram
def performLogin()->bool:
    input('Afer entering login details Press Enter-> ')
    return True
# Function to perfrom scraping
def performScraping():
    browser.driver.implicitly_wait(20)
    while True:
        postContainers=browser.driver.find_elements_by_class_name('_bz0w')
        for postContainer in postContainers:
            link=postContainer.find_element_by_tag_name('a').get_attribute('href')
            addDataIntoTable(conn,link)
        browser.driver.implicitly_wait(30)
        browser.executeScript("window.scrollTo(0, document.body.scrollHeight);")
        browser.driver.implicitly_wait(30)
        sleep(randint(4,10))
# Calling function to check whether all files exits or not 
checkAllFiles()
conn = createConnection(database)
# create tables
if conn is not None:
    # create projects table
    createTable(conn)
    browser=Browser()
    browser.startBrowser('chromedriver.exe',logInUrl,userAgent=Browser.Chrome_UserAgent)
    browser.driver.implicitly_wait(15)
    hashtag=input('Enter hashtag[Example:code] -> ')
    # Check if log in was successful
    if performLogin():
        browser.getPage(f'https://www.instagram.com/explore/tags/{hashtag}/')
        browser.driver.implicitly_wait(30)
        try:
            performScraping()
        except Exception as exc:
            print('[Exception Occurred] : ',exc)
    else:
        print('Email or Password Not Correct\nOr\nEmail or Password Input Field Not Found\nProgram Existing')
    browser.driver.close()
else:
    print("Error! cannot create the database connection.")
# Closing database connection
conn.close()
print('Program End')