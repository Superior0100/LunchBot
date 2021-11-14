import os
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from datetime import datetime
from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = r"C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(executable_path=PATH)

todayDate = datetime.now()
todayWeekday = todayDate.weekday()
todayMonthDay = todayDate.strftime("%d")
todayMonth = todayDate.strftime("%b")
todayYMD = todayDate.strftime('%Y-%m-%d')

def send(todayYMD):
    sender_email = "example@gmail.com" # Insert Secondary Sender Acc
    reciever_email = "example2@gmail.com" # Insert Primary Reciving Acc
    password = "examplePass" # Secondary Acc Pass

    subject = ' Lunch for Today '
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = reciever_email
    msg['Subject'] = subject

    body = "Sent using Python"
    msg.attach(MIMEText(body, "plain"))

    filename = f"lunch{todayYMD}.png"
    attachment = open(filename, 'rb')

    part = MIMEBase("application", "octet-stream")
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename="+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, reciever_email, text)






def lunchScreenshot():
    element = driver.find_element_by_xpath('/html/body/div[1]/ng-view/div/div[2]')  # find part of the page you want image of
    location = element.location
    size = element.size
    png = driver.get_screenshot_as_png()  # saves screenshot of entire page
    driver.quit()
    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))  # defines crop points
    im.save(f'lunch{todayYMD}.png')  # saves new cropped image



driver.get("https://garlandisd.nutrislice.com/menu/north-garland-high/grades-9-12-lunch/print-menu/week")
try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/ng-view/div/print-sidebar/div/div[1]/div[3]/div[1]/ul/li[1]/a"))
        )
        button.click()
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/ng-view/div/print-sidebar/a"))
        )
        button.click()
finally:
    lunchScreenshot()
    send(todayYMD)
    os.remove(f"lunch{todayYMD}.png")
