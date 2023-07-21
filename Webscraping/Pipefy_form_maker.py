import os
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


'''
    class dedicated to creating forms in pipefy
    the class uses selenium to automate the process
    the class can create the following fields:
        - Short text
        - Long text
        - Statement
        - Attachment
        - Checkbox
        - Assignee select
        - Date
        - Datetime
        - Due date
        - Labels
        - Email
        - Phone number
        - Dropdown select
        - Radio select
        - Time
        - Numeric
        - Currency
        - Document ID
    the class can also create conditionals for the fields    
'''
class Pipefy_Form_Maker:

    def __init__(self, target_website : str = None) -> None:

        self.time = time
        self.actionchains = ActionChains
        self.select = Select
        self.target_website = target_website

        os.environ['WDM_SSL_VERIFY'] = '0' # ignores SSL errors

        opts = Options() # sets some settings regarding the way the webscrapping will run
        opts.add_argument('--ignore-certificate-errors')        # prevents the webdriver from raising errors
        opts.add_argument("--disable-extensions") # disables extensions to prevent them from interfering with the code
        opts.add_argument("--start-maximized") # sets the webdriver to start maximized so that the process can be supervised
        opts.add_argument('--allow-running-insecure-content')   # prevents the webdriver from raising errors 
        opts.add_argument("--allow-insecure-localhost")         # prevents the webdriver from raising errors
        opts.add_argument('--no-sandbox')                       # prevents the webdriver from raising errors

        self.driver = Chrome(service=Service(ChromeDriverManager().install()),options=opts) # instantiates the selenium Chrome webdriver with the specified options 

        self.wait = WebDriverWait(self.driver, 10) # sets the webdriver to wait for 10 seconds before raising an error

    def open_website(self, target_website : str = None) -> None:

        if target_website is None and self.target_website is None:
            raise AttributeError("Website was not provided")

        elif target_website is None:
            target_website = self.target_website

        while True:
            try:
                self.driver.get(target_website) # makes the webdriver access the given website
                break
            except:
                continue

    # opens the add field tab
    def Open_mini_card_view(self, new_field : str = None) -> None: 
        
        target_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='pp-fab-btn pp-ico-fab']")))
        self.driver.execute_script("arguments[0].click();", target_element) # clicks on the button to open the mini card view
        
        if new_field != None:
            target_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='pp-ico-plus pp-add-fields']")))
            self.driver.execute_script("arguments[0].click();", target_element) # clicks on the button to open the add fields tab

            target_element = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, new_field)))
            self.driver.execute_script("arguments[0].click();", target_element) # clicks on the desired new field option
        self.time.sleep(0.5)

    # closes the add field tab and the add conditionals tab if present
    def Close_mini_card_view(self) -> None:
        
        try:
            target_element = self.driver.find_element(By.XPATH, "//button[@class='pull-right pp-btn-primary pp-btn']")
            self.driver.execute_script("arguments[0].click();", target_element) # tries to click on the save button of common fields
        
        except:
            target_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pp-modals-body']/footer[@class='pp-modals-footer pp-flex-center pp-flex-justify-end']/button[@class='pp-btn-primary pp-btn']")))
            self.driver.execute_script("arguments[0].click();", target_element) # clicks on the button to save the new contitional
            
            # sets the button to click to exit the conditionals tab
            try:
                save_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//footer[@class='pp-modals-footer pp-flex-center pp-flex-justify-end']/button[@class='pp-btn-primary pp-btn'][contains(text(), 'Concluir')]")))
            except:
                save_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//footer[@class='pp-modals-footer pp-flex-center pp-flex-justify-end']/button[@class='pp-btn-primary pp-btn'][contains(text(), 'Done')]")))
            
            # leaves the conditionals tab 
            save_button.find_element(By.XPATH, "..").click()
            save_button.click()
        
        finally:
            target_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='pp-action-close pp-ico-close pp-btn-sm']")))
            self.driver.execute_script("arguments[0].click();", target_element) # closes the mini card view
       
        self.time.sleep(0.5)

    # adds the field components to the field (description, help text, requirement status)
    def Add_field_components(self, Description = None, Help_text = None, Required = False):
        
        self.time.sleep(0.3)

        # adds the description to the field if provided
        if Description is not None:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pp-box pp-description']/div[@class='pull-right pp-switch-button']"))).click()
            self.actionchains(self.driver).key_down(Keys.TAB).key_up(Keys.TAB).send_keys(Description).perform()
            self.time.sleep(0.2)

        # adds the help text to the field if provided
        if Help_text is not None:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pull-right pp-switch-button']/input[@id='settings-fields-help-toggle']/.."))).click()
            self.actionchains(self.driver).key_down(Keys.TAB).key_up(Keys.TAB).send_keys(Help_text).perform()
            self.time.sleep(0.2)

        # sets the field as required if set to do so
        if Required:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pull-right pp-switch-button']/input[@id='settings-fields-required-toggle']/.."))).click()
        
        self.time.sleep(0.2)

    # adds the options to the field (checkbox, dropdown select, radio select)
    def Add_options(self, Options = None, Display_Horizontally = False) -> None:
        
        self.time.sleep(0.3)

        # sets the field to display horizontally if set to do so
        if Display_Horizontally:
            display_type = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@class='pp-input-wrap']/div[@class='pp-custom-select']/select[@class='pp-select']")))
            self.select(display_type).select_by_index(1)

        # raises an error if the options argument is not provided or is not a list or is an empty list
        if Options == None:
            raise AttributeError("Options argument not provided")
        elif type(Options) != type([]):
            raise AttributeError("Options argument is not a list")
        elif len(Options) == 0:
            raise AttributeError("Options argument is empty")
        
        # selects the field to add the first option
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@class='pp-input-wrap pp-no-padding-top']/div[@class='pp-prefix'][span][input/@class='pp-input']"))).click()
        # iterates through the options list and adds them to the field
        for option in Options:
            self.actionchains(self.driver).send_keys(option).perform()
            self.actionchains(self.driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()
        
        self.time.sleep(0.2)

    def Create_Short_text(self, label = None, Description = None, Help_text = None, Required = True) -> None:

        if label == None:
            raise AttributeError("label argument was not provided")

        self.Open_mini_card_view("Short text")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view() 

    def Create_Long_text(self, label = None, Description = None, Help_text = None, Required = False) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Long text")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view()

    def Create_Statement(self, label = None, Description = None, Help_text = None) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Statement")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text)
        self.Close_mini_card_view()

    def Create_Attachment(self, label = None, Description = None, Help_text = None, Required = False) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Attachment")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view() 

    def Create_Checkbox(self, label = None, Description = None, Help_text = None, Required = False, Display_Horizontally = False, Options = None) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Checkbox")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_options(Options, Display_Horizontally)
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view()  

    def Create_Assignee_select(self, label = None, Description = None, Help_text = None, Required = False) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Assignee select")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view() 

    def Create_Date(self, label = None, Description = None, Help_text = None, Required = False) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Date")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view()

    def Create_Datetime(self, label = None, Description = None, Help_text = None, Required = False) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Datetime")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view()

    def Create_Due_date(self, label = None, Description = None, Help_text = None, Required = False) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Due date")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view()

    def Create_Labels(self, label = None, Description = None, Help_text = None, Required = False) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Labels")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view() 

    def Create_Email(self, label = None, Description = None, Help_text = None, Required = False) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Email")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view()

    def Create_Phone_number(self, label = None, Description = None, Help_text = None, Required = False) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Phone number")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view()  

    def Create_Dropdown_select(self, label = None, Description = None, Help_text = None, Required = False, Options = None) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Dropdown select")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_options(Options)
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view()  

    def Create_Radio_select(self, label = None, Description = None, Help_text = None, Required = False, Display_Horizontally = False, Options = None) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Radio select")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_options(Options, Display_Horizontally)
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view()  

    def Create_Time(self, label = None, Description = None, Help_text = None, Required = False) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Time")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view()

    def Create_Numeric(self, label = None, Description = None, Help_text = None, Required = False) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Numeric")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view() 

    def Create_Currency(self, label = None, Description = None, Help_text = None, Required = False) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Currency")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view()  

    def Create_Document_ID(self, label = None, Description = None, Help_text = None, Required = False) -> None:

        if label == None:
            raise AttributeError("label argument is None")
        
        self.Open_mini_card_view("Document ID")
        # sends the label to the field
        self.actionchains(self.driver).send_keys(label).perform()
        self.Add_field_components(Description, Help_text, Required)
        self.Close_mini_card_view()

    '''
        creates conditionals for the fields
        the conditionals must be provided in the following format:
            - Scenario_name: name of the scenario
            - Conditionals: list of lists of dictionaries
                - each list of dictionaries represents a group of conditions that must be met mutually ("and" type conditions e.g. [condition1 and condition2]])
                - different lists of dictionaries represent different groups of multual conditions ("or" type conditions e.g. [[condition1] or [condition2]])
                - each dictionary represents a condition
                    - the dictionary contains the field to be compared, the type of comparison and the value to be compared to
            - if_true: list of dictionaries
                - each dictionary represents a result if the conditions are met
                    - the dictionary contains the afected field and the value to be set to it
            - if_false: list of dictionaries
                - each dictionary represents a result if the conditions are not met
                    - the dictionary contains the afected field and the value to be set to it
    '''
    def Create_Field_conditionals(self, Scenario_name : str = None, Conditionals : list = None, if_true : list = None, if_false : list = None):

        self.Open_mini_card_view("Field conditionals")

        # clicks on the button to create a new conditional
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pp-modals-body']/div[@class='pp-modals-content pp-bg-light-gray']/div/a[@class='pp-btn-light-gray pp-width-100'][contains(text(), 'Criar novas condicionais')]"))).click()
        except:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pp-modals-body']/div[@class='pp-modals-content pp-bg-light-gray']/div/a[@class='pp-btn-light-gray pp-width-100'][contains(text(), 'Create new Conditional')]"))).click()

        # sets the scenario name
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@class='pp-input'][@placeholder=' Insira um titulo para sua condicional, por exemplo: Condicional #2']"))).send_keys(Scenario_name)
        except:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@class='pp-input'][@placeholder='Type a name for your conditional, ex: Conditional #2']"))).send_keys(Scenario_name)

        # makes the first loop ignore the "or" button to add another group of conditions
        first_or = True
        for conditional in Conditionals:
            
            if first_or:
                first_or = False
            else:
                # clicks on the "or" button to add another group of conditions
                self.driver.find_element(By.XPATH, f"//a[text()='ou'][span/@class='pp-ico-plus']").click()
            
            # makes the first loop ignore the "and" button to add another multual condition
            first_and = True
            for mutual_conditions in conditional:

                if first_and:
                    first_and = False
                else:
                    # clicks on the "and" button to add another multual condition
                    self.driver.find_elements(By.XPATH, f"//a[text()='e'][span/@class='pp-ico-plus']")[-1].click() # adds another "and" condition field

                # clicks on the select field dropdown
                try:    
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span/a[@class='pp-data-dropdown'][text()='Selecione o Campo'][span]"))).click()
                except:
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span/a[@class='pp-data-dropdown'][text()='Select Field'][span]"))).click()
                
                # clicks on the desired field
                desired_field_type = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//dd/a/span[text()='{mutual_conditions['field']}']"))) # selects the desired field
                
                select_type_field = False
                # checks if the selected field is of multiple choice type 
                if desired_field_type.find_element(By.XPATH, "..").get_attribute("class") in ["pp-ico-select", "pp-ico-radio", "pp-ico-checklist"]: 
                    select_type_field = True
                
                
                desired_field_type.click()
                
                # selects the desired condition type field
                if select_type_field:
                    # if the field is of multiple choice type, the condition type field is the second to last select field
                    conditions_select = self.driver.find_elements(By.XPATH, "//div/label[@class='pp-input-wrap pp-wrap-min']/div[@class='pp-custom-select pp-custom-select-lg']/select[@class='pp-select']")[-2]
                else:
                    # if the field is not of multiple choice type, the condition type field is the last input field
                    conditions_select = self.driver.find_elements(By.XPATH, "//div/label[@class='pp-input-wrap pp-wrap-min']/div[@class='pp-custom-select pp-custom-select-lg']/select[@class='pp-select']")[-1]

                # selects the desired condition type (like: "is equal to", "is not blank", etc)
                self.select(conditions_select).select_by_index(mutual_conditions['test_type'])
                
                try:
                    # tries to set a value to compare the field to
                    if select_type_field:
                        # if the field existis, the value to compare field is set
                        target_field = self.driver.find_elements(By.XPATH, "//div/label[@class='pp-input-wrap pp-wrap-min']/div[@class='pp-custom-select pp-custom-select-lg']/select[@class='pp-select']")[-1]
                        self.select(target_field).select_by_visible_text(str(mutual_conditions['value_to_compare']))
                    else:
                        # if the field does not exist, print that the desired option does not accept comparasin values
                        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div/label[@class='pp-input-wrap']/input[@class='pp-input'][last()]"))).send_keys(mutual_conditions['value_to_compare'])
                    
                except:
                    print("this option does not accept comparasin values")

        # makes the first loop ignore the button to add another result if the conditions are met
        first_and_true_outcome = True
        for true_outcome in if_true:

            if first_and_true_outcome:
                first_and_true_outcome = False
            else:
                # clicks on the button to add another result if the conditions are met
                try:
                    self.driver.find_elements(By.XPATH, "//div/div[@class='pp-box']/a[@class='pp-span-linkable pp-add-new pp-action-separator pp-text-uppercase'][contains(text(), 'Adicionar')][span/@class='pp-ico-plus']")[-2].click()
                except:
                    self.driver.find_elements(By.XPATH, "//div/div[@class='pp-box']/a[@class='pp-span-linkable pp-add-new pp-action-separator pp-text-uppercase'][contains(text(), 'Add new')][span/@class='pp-ico-plus']")[-2].click()

            # clicks on the select result dropdown
            true_show_or_hide_select = self.driver.find_elements(By.XPATH, "//div[@class='pp-automations-conditions pp-first-conditions-group pp-no-pseudo-elements pp-no-margin-left']/label[@class='pp-input-wrap pp-wrap-min']/div[@class='pp-custom-select']/select[@class='pp-select']")[-2]
            # selects the desired result (if the field should be shown or hidden)
            self.select(true_show_or_hide_select).select_by_index(true_outcome['SHOW_or_HIDE'])

            # clicks on the select field dropdown
            try:    
                self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span/a[@class='pp-data-dropdown'][text()='Selecione o Campo'][span]"))).click()
            except:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span/a[@class='pp-data-dropdown'][text()='Select Field'][span]"))).click()
            
            # selects the desired field to be affected 
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//dd/a/span[contains(text(), '{true_outcome['field']}')]"))).click()

        # makes the first loop ignore the button to add another result if the conditions are not met
        first_and_false_outcome = True
        for false_outcome in if_false:
            
            if first_and_false_outcome:
                first_and_false_outcome = False
            else:
                # clicks on the button to add another result if the conditions are met
                try:
                    self.driver.find_elements(By.XPATH, "//div/div[@class='pp-box']/a[@class='pp-span-linkable pp-add-new pp-action-separator pp-text-uppercase'][contains(text(), 'Adicionar')][span/@class='pp-ico-plus']")[-1].click()
                except:
                    self.driver.find_elements(By.XPATH, "//div/div[@class='pp-box']/a[@class='pp-span-linkable pp-add-new pp-action-separator pp-text-uppercase'][contains(text(), 'Add new')][span/@class='pp-ico-plus']")[-1].click()

            # clicks on the select result dropdown
            false_show_or_hide_select = self.driver.find_elements(By.XPATH, "//div[@class='pp-automations-conditions pp-first-conditions-group pp-no-pseudo-elements pp-no-margin-left']/label[@class='pp-input-wrap pp-wrap-min']/div[@class='pp-custom-select']/select[@class='pp-select']")[-1]
            # selects the desired result (if the field should be shown or hidden)
            self.select(false_show_or_hide_select).select_by_index(false_outcome['SHOW_or_HIDE'])

            # clicks on the select field dropdown
            try:    
                self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span/a[@class='pp-data-dropdown'][text()='Selecione o Campo'][span]"))).click()
            except:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span/a[@class='pp-data-dropdown'][text()='Select Field'][span]"))).click()
            
            # selects the desired field to be affected 
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//dd/a/span[contains(text(), '{false_outcome['field']}')]"))).click()

        self.Close_mini_card_view()

    # creates the conditionals dictionary
    def conditionals_dict_constructor(self, field : str = None, test_type : int = 3, value_to_compare : str = None) -> dict:
        
        cond = {}
        cond['field'] = field
        cond['test_type'] = test_type # e.g. 3 = "is equal to"
        cond['value_to_compare'] = value_to_compare
        
        return cond

    # creates the dictionary to be used if the conditions are met
    def if_true_dict_constructor(self, SHOW_or_HIDE : int = 2, field : str = None) -> dict:
       
        if_true = {}
        if_true['SHOW_or_HIDE'] = SHOW_or_HIDE # 1 = "show", 2 = "hide
        if_true['field'] = field

        return if_true

    # creates the dictionary to be used if the conditions are not met
    def if_false_dict_constructor(self, SHOW_or_HIDE : int = 2, field : str = None) -> dict:
        
        if_false = {}
        if_false['SHOW_or_HIDE'] = SHOW_or_HIDE # 1 = "show", 2 = "hide
        if_false['field'] = field

        return if_false

    # closes the webdriver
    def Close_Browser(self) -> None:
        self.driver.close()