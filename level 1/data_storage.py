# data_storage.py
class DataStorage:
    def __init__(self, base_file_name):
        self.base_file_name = base_file_name
    
    def record_finding(self, finding, category):
        with open(f"{self.base_file_name}_{category}_findings.txt", "a") as file:
            file.write(finding + "\n")
        print(f"Finding recorded for {category}: {finding}")
