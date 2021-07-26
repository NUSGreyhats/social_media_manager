from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome import options

def post(path:str, caption:str, username:str, password:str):
    """Post a post on instagram"""

    # Open the chrome driver
    driver = init_driver()

    # Go to instagram
    print("Going to instagram.")
    driver.get("http://www.instagram.com")

    # Sleep while the page loads
    sleep(1)

    driver.find_element_by_css_selector('#react-root > section > main > article > div > div > div > div.AC7dP.Igw0E.IwRSH.pmxbr.eGOV_._4EzTm.gKUEf > button:nth-child(1)').click()

    # Click on the login button
    # driver.find_element_by_css_selector("#react-root > section > main > article > div > div > div > div:nth-child(2) > button").click()

    print("Logging in")

    # Key in username
    user = driver.find_element_by_css_selector("#loginForm > div.Igw0E.IwRSH.eGOV_._4EzTm.kEKum > div:nth-child(3) > div > label > input")
    user.send_keys(username)

    # Key in password
    pw = driver.find_element_by_css_selector("#loginForm > div.Igw0E.IwRSH.eGOV_._4EzTm.kEKum > div:nth-child(4) > div > label > input")
    pw.send_keys(password)

    # Click on the login btn
    login_btn = driver.find_element_by_css_selector('#loginForm > div.Igw0E.IwRSH.eGOV_._4EzTm.kEKum > div:nth-child(6)')
    login_btn.click()
    
    sleep(5)

    print("Logged in")

    # Whether to save the login information (Click on not now button)
    try:
        driver.find_element_by_css_selector("#react-root > section > main > div > div > div > button").click()
        print('Press Cancel key')
    except:
        pass
    sleep(2)
    try:
        driver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm').click()
        print('Press 2nd cancel key')
    except:
        pass


    driver.execute_script(
        "HTMLInputElement.prototype.click = function() {                     " +
        "  if(this.type !== 'file') HTMLElement.prototype.click.call(this);  " +
        "};                                                                  ")

    sleep(5)

    # Click on the post button
    post_btn = driver.find_element_by_css_selector("#react-root > section > nav.NXc7H.f11OC > div > div > div.KGiwt > div > div > div.q02Nz._0TPg > svg")
    post_btn.click()

    send_img = driver.find_element_by_css_selector("#react-root > section > nav.NXc7H.f11OC > div > div > form > input")
    send_img.send_keys(path)

    sleep(1)

    # Make the image scale properly (No need to scale in this case because the image is always of the correct dimensions)
    scale_btn = driver.find_element_by_css_selector("#react-root > section > div.gH2iS > div.N7f6u.Bc-AD > div > div > div > button.pHnkA > span")
    scale_btn.click()

    # Go to next
    next_btn = driver.find_element_by_css_selector("#react-root > section > div.Scmby > header > div > div.mXkkY.KDuQp > button")
    next_btn.click()

    sleep(1)

    # Get the text area to key in caption
    caption_area = driver.find_element_by_css_selector("#react-root > section > div.A9bvI > section.IpSxo > div.NfvXc > textarea")
    caption_area.send_keys(caption)

    # Click on share button
    share_btn = driver.find_element_by_css_selector("#react-root > section > div.Scmby > header > div > div.mXkkY.KDuQp > button")
    share_btn.click()
    print('Posted')

    # Wait for 10 seconds for the image to upload
    sleep(10)

    # Close the window
    driver.close()

    exit(0)


def init_driver(executable_path: str = r"chromedriver.exe"):
    # Initialise the options from chrome.
    chrome_options = options.Options()

    # Run in normal mode
    chrome_options.add_argument('--incognito')

    mobile_emulation = { "deviceName": "Nexus 5" }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    # Do not use up screen real estate when executing.
    chrome_options.add_argument("--headless") # To be uncommented when everything is working as expected

    return webdriver.Chrome(options=chrome_options, executable_path=executable_path)

if __name__ == "__main__":
    pass