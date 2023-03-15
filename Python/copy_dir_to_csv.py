import os
import pandas as pd

class Excel_to_CSV:

    def __init__(self, path = None, target_path =  None):
        
        if path == None:
            raise FileNotFoundError("Missing path argument")         
        elif not (os.path.isdir(path)):
            raise FileNotFoundError("path argument is not a directory")
        self.path = path

        if target_path == None:
            self.target_path = path
        elif not (os.path.isdir(target_path)):
            raise FileNotFoundError("target_path argument is not a directory")
        else:
            self.target_path = target_path

    def copie(self, path = None, target_path =  None):
        if path == None:
            raise FileNotFoundError("Missing path argument")
        elif not (os.path.isdir(path)):
            raise FileNotFoundError("path argument is not a directory")
        
        if target_path == None:
            target_path = path
        elif not (os.path.isdir(target_path)):
            raise FileNotFoundError("target_path argument is not a directory")

        dir_list = os.listdir(path) # makes a list out of every file in the directory
        target_dir_list = os.listdir(target_path) # makes a list out of every file in the target directory

        # iterares through every file in the directory to see if it needs to receive a copy in csv
        for i in dir_list:
            if i[-5:] == ".xlsx": # checks if the current file is an excel file
                if f"{i[:-5]}.csv" in target_dir_list: # checks if the current file already has its csv counterpart, skips to the next loop if it does
                    continue

                # procedes to make a csv copy of the current file
                df = pd.read_excel(f"{path}\{i}")
                df.to_csv(f"{target_path}\{i[:-5]}.csv", index=False, header=True, sep=";")
                print(f"{i} copied to csv")
        print("Directory fully copied to CSV\n")
        return

    def check_dir(self, path = None):
        if path == None:
            raise FileNotFoundError("Missing path argument")
        elif not (os.path.isdir(path)):
            raise FileNotFoundError("path argument is not a directory")

        xlsx = 0 # excel file counter
        csv = 0  # csv file counter

        dir_list = os.listdir(path) # makes a list out of every file in the directory

        # iterates through the directory files, to count each file type
        for i in os.listdir(path): 
            if i[-5:] == ".xlsx":
                xlsx += 1
            elif i[-4:] == ".csv":
                csv += 1

        # outputs the file count
        print(f"directory file count: {len(dir_list)}\ncsv: {csv}\txlsx: {xlsx}\n")
        return
        
    def __main__(self):
        self.copie(self.path, self.target_path)
        self.check_dir(self.path)
        return