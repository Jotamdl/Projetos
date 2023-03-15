import os
import time
import re
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Convert_Values:

    def __init__(self, path: str = None, target_path: str =  None, generate_csv: bool = False,  target_currency: str = None, cur_col: str or int = None, values_col: str = None, new_cur_col: str = None) -> None:
        
        self.path = path
        self.target_path = target_path
        self.generate_csv = generate_csv
        self.target_currency = target_currency
        self.cur_col = cur_col
        self.values_col = values_col
        self.new_cur_col = new_cur_col

    def getCurrencies(self, path: str = None, cur_col: str or int = None) -> dict:
        currenciesDict = {} # instantiates dictionary that will be populated with various currencies  
        
        # checks if the path argument was provided properly
        if path == None:
            path = self.path
        if path == None:
            raise FileNotFoundError("Missing path argument")
        elif not (os.path.isfile(path)):
            raise FileNotFoundError("path argument is not a file")

        # checks if the cur_col argument was provided properly
        if cur_col == None:
            cur_col = self.cur_col
        if cur_col == None:
            raise ValueError("Missing cur_col argument")

        # checks if the database is a CSV or Excel file and reads it properly
        if path[-5:] == ".xlsx":
            df = pd.read_excel(path, usecols=[cur_col], header = 0, decimal = ",")
        else:
            df = pd.read_csv(path, usecols=[cur_col], header = 0, sep = ';', decimal = ",")
        
        df = df.drop_duplicates() # leaves only 1 type of each currency on the database
        
        # Gets the currency in the necessary format for the dict and adds it to the dict
        for i in df[df.columns[0]]:
            j = re.search(r'\W*[ABCDEFGHIJKLMNOPQRSTUVWXYZ]{3}\W*', i).group()
            currenciesDict[j] = 0

        return currenciesDict

    def getConvertion(self, currencies: dict = None, target_currency: str = None) -> dict:

        # checks if the currencies argument was provided properly
        if currencies == None:
            raise ValueError("Missing currencies argument")

        # checks if the target_currency argument was provided properly
        if target_currency == None:
            target_currency = self.target_currency
        if target_currency == None:
            raise ValueError("Missing target_currency argument")
        elif re.search(r'\W*[ABCDEFGHIJKLMNOPQRSTUVWXYZ]{3}\W*', target_currency).group() == None:
            raise ValueError("target_currency argument is not a valid currency, please use the 3 letter format (e.g. USD)")

        os.environ['WDM_SSL_VERIFY'] = '0' # ignores SSL errors
        T = 0 # errors counter

        while T < 5: # while under 5 errors during exectution
            
            # this 'try' makes sure that the code doesn't end abruptly whens a bug occurs on the website
            try:

                site = 'https://www.bcb.gov.br/conversao' # target website

                opts = Options() # sets some settings regarding the way the webscrapping will run
                opts.add_argument('--headless') # sets the webdriver to run without opening a window
                opts.add_argument('--ignore-certificate-errors') # --sets the webdriver to ignore a common error due to envirolment in wich the code runs

                browser = Chrome(service=Service(ChromeDriverManager().install()),options=opts) # instantiates the selenium Chrome webdriver with the specified options 
                browser.get(site) # makes the webdriver access the given website
                
                browser.find_element(By.XPATH, "//input[@placeholder='0,00']").send_keys(100) # sets the value oh 1.00 BRL to be converted to oher currencies

                # selects the desired currency in the target dropdown (to currency)
                browser.find_element(By.ID, 'button-converter-para').click()
                time.sleep(1.0)
                element = browser.find_element(By.XPATH, "//ul[@id='moedaResultado1']").find_element(By.PARTIAL_LINK_TEXT, f"({target_currency})")
                browser.execute_script("arguments[0].click();", element)

                # selects all the currencies present in the provided dict in the target dropdown (from currency)
                for i in currencies:
                    browser.find_element(By.ID, 'button-converter-de').click()
                    element = browser.find_element(By.ID, 'moedaBRL').find_element(By.PARTIAL_LINK_TEXT, f"({i})")
                    browser.execute_script("arguments[0].click();", element)
                    time.sleep(0.5)
                    text = browser.find_elements(By.XPATH, "//div[@class='card-body']")[2].text # gets the conversion value
                    currencies[i] = float(re.search(r'\d+\,\d+$', text).group().replace(",",".")) # updates the convertion value from any given currency in the provided dict
                currencies[target_currency] = 1 # makes shure that no error occurs when the base values include currencies in the target one

            # resets the website / webdriver if an error accurs 
            except:
                browser.close()
                print("****Code failed due to website malfunction, retrying")
                T += 1
                if T == 5: # if the code has failed at least 5 times, ends execution 
                    raise RuntimeError("Way too many errors, code shuting down")   
                continue
            break # breaks out of the loop if no error occurs during its execution

        return currencies

    def convertValues(self, path: str = None, target_path: str =  None, generate_csv: bool = False, currencies: dict = None, cur_col: str or int = None, values_col: str = None, new_cur_col: str = None):
        
        # checks if the path argument was provided properly
        if path == None:
            path = self.path
        if path == None:
            raise FileNotFoundError("Missing path argument")
        elif not (os.path.isfile(path)):
            raise FileNotFoundError("path argument is not a file")
        
        # checks if the target_path argument was provided properly
        if target_path == None:
            target_path = self.target_path
        if target_path == None:
            target_path = path[:-4] + "_converted.csv"
        elif not (os.path.isfile(target_path)):
            raise FileNotFoundError("target_path argument is not a file")

        # checks if the currencies argument was provided properly
        if currencies == None:
            currencies = self.currencies
        if currencies == None:
            raise ValueError("Missing currencies argument")

        # checks if the cur_col argument was provided properly
        if cur_col == None:
            cur_col = self.cur_col
        if cur_col == None:
            raise ValueError("Missing cur_col argument")
        
        # checks if the values_col argument was provided properly
        if values_col == None:
            values_col = self.values_col
        if values_col == None:
            raise ValueError("Missing values_col argument")
        
        # sets the name of the new column if none is provided
        if new_cur_col == None:
            new_cur_col = "New_Currency"

        # checks if the database is a CSV or Excel file and reads it properly
        if path[-5:] == ".xlsx":
            df = pd.read_excel(path, header = 0, decimal = ",")
        else:
            df = pd.read_csv(path, header = 0, sep = ';', decimal = ",")

        # converts the values from the provided column to the target currency
        df[new_cur_col] = df.apply(lambda row : row[values_col] * currencies[re.search(r'\W*[ABCDEFGHIJKLMNOPQRSTUVWXYZ]{3}\W*', row[cur_col]).group()], axis = 1)
        
        # saves the new database if the generate_csv argument is set to True
        if generate_csv == True:
            df.to_csv(target_path, index=False, header=True, sep=";", decimal=",")

        return df

    def __main__(self):
        
        dict = self.getCurrencies(self.path, self.cur_col)
        conv = self.getConvertion(dict, self.target_currency)
        df = self.convertValues(self.path, self.target_path, self.generate_csv, conv, self.cur_col, self.values_col, self.new_cur_col)

        return df