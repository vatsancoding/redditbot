# All modules to be imported
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

# Configuring settings
options = Options()
#options.add_argument("--headless")
options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\vatsa\OneDrive\Desktop\redditbot\chromedriver.exe")
print("\n\n\nLoading page\n\n\n")


# Initializing variables
username = "WalrusLimp7694"
password = "abracadabra"
#sub = input("\n\nEnter the subreddit here: ")
sub = "ApplyingToCollege" # Can be deleted later
message = "Sample message"
users = []
recursion = 0


# Opening Reddit
def openBrowser():
    driver.maximize_window()
    time.sleep(1)
    driver.get("https://www.reddit.com/login")
    time.sleep(15)
    print("\n\n\nPage loading...\n\n\n")
    return 1



# Logging in
def login():
    global recursion
    try:
        time.sleep(1)
        usrField = driver.find_element(By.ID, "loginUsername")
        if usrField.is_displayed():
            usrField.click()
            usrField.send_keys(username)
        time.sleep(1)
        pwdField = driver.find_element(By.ID, "loginPassword")
        if pwdField.is_displayed():
            pwdField.click()
            pwdField.send_keys(password)
            time.sleep(1)
            pwdField.send_keys(Keys.ENTER)
        print("\n\n\nSuccessfully logged into Reddit!\n\n\n")
        time.sleep(2)
        recursion = 0
        return 1
    except Exception:
        print("\nFailed to login. Possible reasons include failure to load Reddit. Trying again...\n")
        time.sleep(5)
        recursion += 1
        if recursion > 20:
            raise Exception("Internet connection failed")
        login()


# Making a new Reddit tab
def makeNewTab():
    global recursion
    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        print("\n\nSuccessfully created a new tab\n\n\n")
        recursion = 0
        return 1
    except Exception:
        print("\nFailed to create new tab. Trying again...\n")
        time.sleep(2)
        recursion += 1
        if recursion > 20:
            raise Exception("Internet connection failed")
        makeNewTab()


# Opening target subreddit
def openSubreddit():
    global recursion
    try:
        driver.get("https://www.reddit.com/r/" + sub + "/top/?t=day")
        print("\n\n\nThe subreddit was opened successfully\n\n\n")
        recursion = 0
        return 1
    except Exception:
        print("\nFailed to open the subreddit. Possible causes include poor internet connection. Trying again shortly...\n")
        time.sleep(5)
        recursion += 1
        if recursion > 20:
            raise Exception("Internet connection failed")
        openSubreddit()



# Computing the number of posts to search
def computePostLength():
    global recursion
    try:
        postLen = int(str(driver.execute_script('return document.getElementsByClassName("_11R7M_VOgKO1RJyRSRErT3").length')))
        print("\n\n\nPost length:", postLen, "\n\n\n")
        recursion = 0
        return postLen
    except Exception:
        print("\nScript injection for computing post length failed. Possible causes include failure of website to load completely. This is a common issue. Trying again shortly\n")
        time.sleep(10)
        recursion += 1
        if recursion > 20:
            raise Exception("Internet connection failed")
        return computePostLength()

# Finding the contents of a given post
def postContent(i):
    global recursion
    try:
        data = driver.execute_script('return document.getElementsByClassName("_11R7M_VOgKO1RJyRSRErT3")[' + str(i) + '].innerText ')
        print("\nPost content has been successfully retrieved\n")
        recursion = 0
        return data
    except Exception:
        print("\nFailed to extract all contents of post", i + 1, ". Possible causes include failure to load the post. Trying again shortly...\n")
        time.sleep(7)
        recursion += 1
        if recursion > 20:
            raise Exception("Internet connection failed")
        return postContent(i)

# Clicks a given post
def clickPost(i):
    global recursion
    try:
        driver.execute_script('document.getElementsByClassName("_11R7M_VOgKO1RJyRSRErT3")[' + str(i) + '].click()')
        print("\nPost",i,"has been successfully clicked\n")
        recursion = 0
        return 1
    except Exception:
        print("\nFailed to click post. Possible causes include failure to load the post. Trying again shortly...\n")
        time.sleep(7)
        recursion += 1
        if recursion > 20:
            raise Exception("Internet connection failed")
        clickPost(i)

# Extracts all commentator usernames from a post website
def extractUsername():
    global recursion
    try:
        data = driver.execute_script('data = ""; for(i=0;i<document.getElementsByClassName("wM6scouPXXsFDSZmZPHRo").length;i++) { data += document.getElementsByClassName("wM6scouPXXsFDSZmZPHRo")[i].innerText + " "; }; return data; ').split(" ")
        print("Data:",data)
        if len(data) == 1 and data[0].strip() == "":
            raise Exception("Failed to gather sufficient data")
        else:
            print("\n\n\nAll usernames successfully extracted\n\n\n")
            recursion = 0
            return data
    except Exception:
        print("\nFailed to extract all usernames. Possible causes include poor internet connection and failure to load the post website completely. Trying again shortly...\n")
        driver.execute_script("window.location.reload();")
        time.sleep(7)
        recursion += 1
        if recursion > 20:
            raise Exception("Internet connection failed")
        return extractUsername()


# Finds the chat button
def findChat():
    chatFinder = """
        buttons = document.getElementsByClassName("_2iuoyPiKHN3kfOoeIQalDT"); 
        let i = 0; 
        let found = 0; 
        for(i=0;i<buttons.length;i++) {
            if(buttons[i].innerText.includes("Chat")) {
                chatbutton = buttons[i]; 
                found = 1; 
                break; 
            }
        }
        if(found == 1) { chatbutton.click(); } 
        return found; 
        """
    global recursion
    try:
        chatStatus = driver.execute_script(chatFinder)
        print("\nChat status detected\n")
        recursion = 0
        return not bool(chatStatus)
    except Exception:
        print("\nFailed to find the chat button. Possible causes include failure to load. Trying again shortly...\n")
        time.sleep(7)
        recursion += 1
        if recursion > 20:
            raise Exception("Internet connection failed")
        return findChat()


# Sends message to a particular user
def sendmessage(user):
    global recursion
    print("Trying to message " + user)
    try:
        messagetyper = driver.find_element(By.CLASS_NAME, "_24sbNUBZcOO5r5rr66_bs4")
        messagetyper.send_keys(message)
        messagetyper.send_keys(Keys.ENTER)
        print("\nMessage successfully sent to", user, "\n")
        print("Messagetyper", messagetyper.get_attribute("placeholder"))
        recursion = 0
        return 1
    except Exception:
        print("\n\nFailed to send message. Possible causes include failure to load chat. Trying again shortly...\n\n ",recursion)
        time.sleep(3)
        recursion += 1
        if recursion > 10:
            recursion = 0
            driver.execute_script("window.location.reload()")
            print("\n\nAfter a long wait, chat has been refreshed to reload it\n\n")
        sendmessage(user)

# Adds the user to database
def updateDatabase(user):
    File = open("database/" + user[0] + ".txt", "a+")
    File.write("\n" + user)
    File.close()
    print("\n" + user + " has been added to the database\n")
    return 1


# Sends messages to all users
def sendmessagetoall(newUsers):
    driver.execute_script('window.open("")')
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[2])
    for user in newUsers:
        driver.get("https://www.reddit.com/user/" + user)
        time.sleep(10)
        chatDisabled = findChat()
        if chatDisabled:
            print("\n\n" + user + " has disabled chat")
            continue
        time.sleep(15)
        sendmessage(user)
        updateDatabase(user)
    return 1

# Processes data from a post
def processPost():
    postLen = computePostLength()
    postLen = 1
    for i in range(postLen):
        content = postContent(i)
        if "Promoted" not in content:
            clickPost(i)
            time.sleep(2)
            if "reddit" not in driver.current_url:
                print("\nAlert! Advertisement website detected")
                continue
            time.sleep(15)
            data = extractUsername()
            for username in data:
                if username not in users and username.strip() != "" and "deleted" not in username:
                    users.append(username)
            time.sleep(1)
            driver.execute_script("history.back();")
            print("\n\n Extracted data")
            print(i)
            print(users)
        else:
            print("\nPotential advertisement avoided")
    print("\n\n\n\nData successfully gathered!\n\n\n")
    newUsers = []
    for user in users:
        db = open("database/" + user[0] + ".txt", "a+")
        dbInfo = db.read()
        db.close()
        if user not in dbInfo:
            newUsers.append(user)
    print("\n\n\nUsers successfully filtered out\n\n\n")
    newUsers = newUsers[3:]
    sendmessagetoall(newUsers)
    return 1


# Driver code
if __name__ == '__main__':
    openBrowser()
    login()
    makeNewTab()
    openSubreddit()
    processPost()


