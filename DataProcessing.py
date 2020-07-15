import pandas as pd
import numpy as np

class DataProcessing:
    def __init__(self, file, train):
        self.file = pd.read_excel(file)
        self.train = train
        self.i = int(self.train * len(self.file))
        self.stock_train = self.file[0: self.i]
        self.stock_test = self.file[self.i:]
        self.input_train = []
        self.output_train = []
        self.input_test = []
        self.output_test = []