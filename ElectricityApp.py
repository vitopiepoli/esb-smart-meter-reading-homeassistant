import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.webdriver.chrome.options import Options
import glob
# # Function to load ESB data
# def load_esb_data(user, password, mpnr, start_date):
#   print("[+] open session ...")
#   s = requests.Session()
#   s.headers.update({
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
#   })    
#   print("[+] calling login page. ..")
#   login_page = s.get('https://myaccount.esbnetworks.ie/', allow_redirects=True)
#   result = re.findall(r"(?<=var SETTINGS = )\S*;", str(login_page.content))
#   settings = json.loads(result[0][:-1])
#   # print("[+] sending credentials ...")
#   # s.post(
#   #   'https://login.esbnetworks.ie/esbntwkscustportalprdb2c01.onmicrosoft.com/B2C_1A_signup_signin/SelfAsserted?tx=' + settings['transId'] + '&p=B2C_1A_signup_signin', 
#   #   data={
#   #     'signInName': user, 
#   #     'password': password, 
#   #     'request_type': 'RESPONSE'
#   #   },
#   #   headers={
#   #     'x-csrf-token': settings['csrf'],
#   #   },
#   #   allow_redirects=False)
#   # print("[+] passing AUTH ...")
#   # confirm_login = s.get(
#   #   'https://login.esbnetworks.ie/esbntwkscustportalprdb2c01.onmicrosoft.com/B2C_1A_signup_signin/api/CombinedSigninAndSignup/confirmed',
#   #   params={
#   #     'rememberMe': False,
#   #     'csrf_token': settings['csrf'],
#   #     'tx': settings['transId'],
#   #     'p': 'B2C_1A_signup_signin',
#   #   }
#   # )
#   # print("[+] confirm_login: ",confirm_login)
#   # print("[+] doing some BeautifulSoup ...")
#   # soup = BeautifulSoup(confirm_login.content, 'html.parser')
#   # form = soup.find('form', {'id': 'auto'})
#   # s.post(
#   #   form['action'],
#   #   allow_redirects=False,
#   #   data={
#   #     'state': form.find('input', {'name': 'state'})['value'],
#   #     'client_info': form.find('input', {'name': 'client_info'})['value'],
#   #     'code': form.find('input', {'name': 'code'})['value'],
#   #   }, 
#   # )
  
#   # #data = s.get('https://myaccount.esbnetworks.ie/datadub/GetHdfContent?mprn=' + mpnr + '&startDate=' + start_date.strftime('%Y-%m-%d'))
#   # print("[+] getting CSV file for MPRN ...")
#   # data = s.get('https://myaccount.esbnetworks.ie/DataHub/DownloadHdf?mprn=' + mpnr + '&startDate=' + start_date.strftime('%Y-%m-%d'))

#   # print("[+] CSV file received !!!")
#   # data_decoded = data.content.decode('utf-8').splitlines()

#   #   # Split each string by commas
#   # data_split = [line.split(',') for line in data_decoded]

#   # # Use the first list as the header
#   # header = data_split[0]

#   # # Use the remaining lists as rows
#   # rows = data_split[1:]

#   # # Create the DataFrame
#   # df = pd.DataFrame(rows, columns=header)
  
#   return settings

def esb_data(user, password,download_dir):

    # get the path of the driver
    path = os.getenv("Selenium")
    options = webdriver.ChromeOptions()
    # add headers to the browser
    options.add_argument("user-agent=Chrome/58.0.3029.110 Safari/537.3")
    options.add_argument('--headless')  # This option runs Chrome in headless mode.
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # modify the download directory

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    #query which is download directory


    driver = webdriver.Chrome(options=options)

    # Open the webpage
    driver.get('https://myaccount.esbnetworks.ie/')
    # driver.maximize_window()
    # Allow the page to load
    time.sleep(3)


    # Find the username field using XPath and enter the username
    username_field = driver.find_element(By.XPATH, '//*[@id="signInName"]')
    username_field.send_keys(user)

    # Find the password field using XPath and enter the password
    password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
    password_field.send_keys(password)

    # Submit the form (assuming the form is submitted by pressing Enter in the password field)
    password_field.send_keys(Keys.RETURN)

    # driver accept cookies
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
    #scroll down the page
    driver.execute_script("window.scrollTo(0, 500)")

    # click on Xpath element
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/main/div[1]/div[3]/div/div/div[1]/div[2]/div/a/span').click()
    # click on Xpath element
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="tab-pane-2-button"]/span').click()


    # Allow some time for the login process to complete
    driver.execute_script("window.scrollTo(0, 500)")
    time.sleep(3)

    #click on Xpath element
    driver.find_element(By.XPATH, '//*[@id="btnDownload-intervalkw"]/span').click()
    time.sleep(5)
    # Close the browser
    driver.quit()

user = "vitopiepoli@gmail.com"
password = "!$?NvtidHx4F74P"


start_date = datetime.today() - timedelta(days=30)

# Function to calculate daily cost
def calculate_daily_cost(df, cost_per_kw, discount, vat, fixed_cost):
    daily_kwh = df.groupby(df.index.date).sum()['Read Value']
    daily_cost = (daily_kwh * (cost_per_kw/100) * discount) 
    vat_cost = daily_cost * vat
    daily_cost_total = daily_cost + vat_cost + fixed_cost
    return daily_cost_total

# Streamlit application
st.title("ESB Electricity Consumption and Cost Analysis")

# User credentials

user = "xxxxxxxxxxxxxx"
password = "xxxxxxxxxxxxxxx"

# Date input
start_date = datetime.today() - timedelta(days=30)

# Load data once and store it in session state
if 'df' not in st.session_state:
    download_dir ="xxxxxxxxxxxxxxxxxxxx"
    esb_data(user, password,download_dir)

# identify the csv file in the download directory
    data = glob.glob(r"xxxxxxxxxxxxxxxxxxxxxxx/*.csv")
# extract the csv file name
    file_name = os.path.basename(data[0])
    df = pd.read_csv(download_dir + "\\" + file_name)
    df['Read Date and End Time'] = pd.to_datetime(df['Read Date and End Time'], format='%d-%m-%Y %H:%M')
    df['Read Value'] = df['Read Value'].astype(float) / 2
    df["Read Value"] = pd.to_numeric(df["Read Value"], errors='coerce').astype(float)
    df = df[["Read Date and End Time", "Read Value"]]
    df.set_index('Read Date and End Time', inplace=True)
    st.session_state.df = df
else:
    df = st.session_state.df



# Process data
df_resampled = df.resample('h').sum().reset_index()
df_daily = df.resample('D').sum().reset_index()



# Date input
start_date = st.date_input("Start Date", datetime.today() -  timedelta(days=30), min_value=df.index.min())
end_date = st.date_input("End Date", datetime.today())

# subset df resampled to the same range of dates
mask_2 = (df_resampled['Read Date and End Time'] > pd.Timestamp(start_date)) & (df_resampled['Read Date and End Time'] <= pd.Timestamp(end_date))
df_resampled = df_resampled.loc[mask_2]
df_resampled['Read Date and End Time'] = np.array(df_resampled['Read Date and End Time'])

# Filter data by selected date range
mask = (df_daily['Read Date and End Time'] >= pd.Timestamp(start_date)) & (df_daily['Read Date and End Time'] <= pd.Timestamp(end_date))
df_daily_sum = df_daily.loc[mask]
df_daily['Read Date and End Time'] = np.array(df_daily['Read Date and End Time'])
# Calculate daily cost
cost_per_kw = 33.96
discount = 0.8
vat = 0.09
fixed_cost = 0.66
daily_cost = calculate_daily_cost(df, cost_per_kw, discount, vat, fixed_cost)

# Tabs
tab1, tab2 = st.tabs(["Daily Consumption and Cost", "Summary"])

with tab1:
    st.header("Daily Consumption and Cost")
    fig = px.line(df_resampled, x='Read Date and End Time', y='Read Value',
                  title='Hourly and Daily Electricity Consumption',
                  labels={'Read Value': 'Consumption (kW)'})
    fig.add_scatter(x=df_daily_sum['Read Date and End Time'], y=df_daily_sum['Read Value'], mode='lines', name='Daily')
    fig.update_xaxes(
        dtick="D1",
        tickformat="%b %d",
        title_text="",
        tickangle=45
    )
    st.plotly_chart(fig)

    daily_cost=daily_cost.loc[start_date:end_date]

    fig_cost = px.bar(x=daily_cost.index, y=daily_cost.values, labels={'x': 'Date', 'y': 'Daily Cost'},
                      title='Daily Electricity Cost')
    fig_cost.add_scatter(x=daily_cost.index, y=daily_cost.rolling(window=3).mean(), mode='lines', name='7-Day Rolling Mean')
    st.plotly_chart(fig_cost)

with tab2:
    st.header("Total Cost")
    total_cost = daily_cost.loc[start_date:end_date].sum()
    st.write(f"Total Cost for the selected period: €{total_cost:.2f}")
    number_of_days = len(daily_cost.loc[start_date:end_date])
    st.write(f"Number of days in the selected period: {number_of_days}")
