from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import getpass

username = input("Please provide your github user name? ")
password = getpass.getpass("Please enter your github password? ")

try:
    options = Options()
    options.add_argument("--headless")
    edge = webdriver.Edge(options=options)
    edge.get("https://github.com/login")
    edge.find_element("id","login_field").send_keys(username)
    edge.find_element("id","password").send_keys(password)
    edge.find_element("name","commit").click()

    WebDriverWait(driver=edge, timeout=10).until(lambda x: x.execute_script("return document.readyState === 'complete'"))
    error_message = "Incorrect username or password."
    errors = edge.find_elements("css selector", ".flash-error")
    for e in errors:
        print(e.text)

    if any(error_message in e.text for e in errors):
        print("[!] Login failed")
        exit(1)
    else:
        print("[+] Login successful")

    repos = edge.find_element("css selector", ".js-repos-container")

    WebDriverWait(driver=edge, timeout=10).until((lambda x: repos.text != "Loading..."))
    
    #Expand all the project list
    edge.find_element("name","button").click()

    print("This is your public repository list")
    for repo in repos.find_elements("css selector", "li.public"):
        print(repo.find_element("css selector", "a").get_attribute("href"))
    
    print("\nThis is your private repository list")
    for repo in repos.find_elements("css selector", "li.private"):
        print(repo.find_element("css selector", "a").get_attribute("href"))
        
finally:
    edge.quit()

