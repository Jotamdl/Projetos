import difflib
import glob 
import re
import os

'''
    class dedicated to getting the latest files in a given directory
    the files are returned in a list and can be filtered by file type and file name format
    is also possible to determine the number of files to be returned by the function
        - dir_path: directory path
        - file_type: file type to be searched
        - number_of_files: number of files to be returned in the list
        - file_name_format: format of the file name to be searched
'''
class Get_latest_files: 
    
    def __init__(self, dir_path : str = None, file_type : str = "*", number_of_files: int = 1, file_name_format: str = None) -> None:

        self.dir_path = dir_path
        self.file_type = file_type
        self.number_of_files = number_of_files
        self.file_name_format = file_name_format

    def get_latest_files(self, dir_path : str = None, file_type : str = None, number_of_files: int = None, file_name_format: str = None) -> list:

        if dir_path is None and self.dir_path is None: # raises an erro if no dir_path is provided
            raise KeyError("dir_Path must be provided")
        elif dir_path is None:
            dir_path = self.dir_path

        if file_type is None:
            file_type = self.file_type
        if "." not in file_type: # adds a dot to the file type if it is not provided e.g. "txt" -> ".txt"
            file_type = "." + file_type

        if number_of_files is None:
            number_of_files = self.number_of_files
            
        if file_name_format is None:
            file_name_format = self.file_name_format
               

        dir_list = glob.glob(f"{dir_path}\*{file_type}") # gets all items in the directory
        dir_list = [file for file in dir_list if re.search(r"(\w)+\.", file)] # removes folders from the list

        if file_name_format is not None: # if a file name format is provided, the list is filtered by the format
            tupple_path_name = [(file_path, re.search(r"(\w)+\.", file_path).group()[0:-1]) for file_path in dir_list if re.search(r"(\w)+\.", file_path)]

            dir_list = [file_path for file_path, file_name in tupple_path_name if difflib.SequenceMatcher(None, file_name, file_name_format).ratio() > 0.65]

        latest_files = dir_list # copies the list to a new variable
        latest_files.sort(key=os.path.getctime, reverse=True) # sorts the list by creation time

        return latest_files[0:number_of_files] # returns the number of files specified by the user

    def __main__(self) -> list:
        return self.get_latest_files(self.dir_path, self.file_type, self.number_of_files, self.file_name_format)