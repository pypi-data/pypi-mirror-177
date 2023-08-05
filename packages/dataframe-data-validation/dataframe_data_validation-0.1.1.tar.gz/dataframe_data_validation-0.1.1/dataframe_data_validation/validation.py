import pandas as pd
import re
from enum import Enum

class NanValues(Enum):
    RemainNan = 0
    DropNan = 1
    SetToZero = 2
    SetToMinimum = 3
    SetToAverage = 4
    SetToMaximum = 5
    
    
    
class Validation:
    
    def __init__(self, dataframe:pd.DataFrame,
                 reset_index:bool):
        self.dataframe = dataframe
        
        self.reset_index = reset_index
        
    def changeNanValues(self, column, nan_values_set_to):
        if nan_values_set_to == NanValues.SetToZero:
            self.dataframe[column] = self.dataframe[column].fillna(0)
        elif nan_values_set_to == NanValues.SetToMinimum:
            minimum = self.dataframe[column].min()
            self.dataframe[column] = self.dataframe[column].fillna(minimum)
        elif nan_values_set_to == NanValues.SetToMaximum:
            maximum = self.dataframe[column].max()
            self.dataframe[column] = self.dataframe[column].fillna(maximum)
        elif nan_values_set_to == NanValues.SetToAverage:
            average = self.dataframe[column].mean()
            self.dataframe[column] = self.dataframe[column].fillna(average)
        elif nan_values_set_to == NanValues.DropNan:
            self.dataframe.dropna(inplace=True)
            if self.reset_index:
                self.dataframe.reset_index(drop=True, inplace=True)
                
    def checkAllIsDigit(self, num: str):
        """
        Check that all character of input string is Digits

        :param data_frame: Pandas DataFrame
        :param column: columns for validation
        :return: same as input, if all character of input string is Digits, otherwise None
        """
        try:
            after_remove_other_than_digits = re.sub(r'[^\d]', '', num)
            if num == after_remove_other_than_digits:
                return num
            else:
                return None
        except Exception as e:
            return None
        
    def checkTimestampInSec(self, num: str):
        """
        Check that all character of input string is Digits

        :param data_frame: Pandas DataFrame
        :param column: columns for validation
        :return: same as input, if all character of input string is Digits, otherwise None
        """
        try:
            if len(num) > 10:
                # it means that even if input string is all digit, its is bigger than what we are looking for
                # so we cant accept it
                # FYI, we are looking for String Unix Timestamp values in second precision, YES this is who we are
                return None
            else:
                return num
        except Exception as e:
            return None
        
    def checkTimestampInMSec(self, num: str):
        """
        Check that all character of input string is Digits

        :param data_frame: Pandas DataFrame
        :param column: columns for validation
        :return: same as input, if all character of input string is Digits, otherwise None
        """
        try:
            if len(num) > 13:
                # it means that even if input string is all digit, its is bigger than what we are looking for
                # so we cant accept it
                # FYI, we are looking for String Unix Timestamp values in second precision, YES this is who we are
                return None
            else:
                return num
        except Exception as e:
            print(e)
            return None
        
    def removeEverythingExceptDigits(self, num: str):
        """
        Check that all character of input string is Digits

        :param data_frame: Pandas DataFrame
        :param column: columns for validation
        :return: same as input, if all character of input string is Digits, otherwise None
        """
        try:
            return re.sub(r'[^\d]', '', num)
        except Exception as e:
            return None


    def removeThousandsSeparator(self, num: str):
        """
        Check that all character of input string is Digits

        :param data_frame: Pandas DataFrame
        :param column: columns for validation
        :return: same as input, if all character of input string is Digits, otherwise None
        """
        try:
            return num.replace(',', '')
        except Exception as e:
            return None


    def validateIntegerValues(self, column:str, change_type_to_int:bool, 
                              remove:list, 
                              nan_values_set_to:NanValues):
        """
        validating integer data types
        :param data_frame: Pandas DataFrame
        :param column: columns for validation
        :return: True if all task complete Successfully, otherwise False
        """
        if not isinstance(nan_values_set_to, NanValues):
            raise TypeError('nan_values_set_to must be an instance of NanValues Enum')
        
        try:
            
            # self.removeCurrencySeparator(column=column)
            # self.dataframe[column] = self.dataframe[column].str.replace(',', '')
            if '*' in remove:
                self.dataframe[column] = self.dataframe[column].apply(lambda x: self.removeEverythingExceptDigits(str(x)))
            if ',' in remove:
                self.dataframe[column] = self.dataframe[column].apply(lambda x: self.removeThousandsSeparator(str(x)))

            # first, trying to apply pd.to_numeric to desire column. if anything goes wrong then value will set to None
            self.dataframe[column] = self.dataframe[column].apply(pd.to_numeric, errors='coerce')

            # we need to remove None values for next step, so ...
            self.changeNanValues(column=column, nan_values_set_to=nan_values_set_to)
            
            # then change column type to int, because it probably is float (pd.to_numeric)
            if change_type_to_int and self.nan_values_set_to != NanValues.RemainNan:
                self.dataframe[column] = self.dataframe[column].astype(int)
                
            msg = '{} converted to integer successfully'.format(column)
        except Exception as e:
            msg = 'Error converting column {} to integer : {}'.format(column, e)
            raise Exception(msg)
        return msg


    def validateUnixTimestampValues(self, column, base, remove, 
                                    nan_values_set_to:NanValues):
        """Unix Timestamp values Validation

        Args:
            column (_type_): _description_
            base (_type_): _description_
        """
        if not isinstance(nan_values_set_to, NanValues):
            raise TypeError('nan_values_set_to must be an instance of NanValues Enum')
        
        try:
            if '*' in remove:
                self.dataframe[column] = self.dataframe[column].apply(lambda x: self.removeEverythingExceptDigits(str(x)))
            if base == 's':
                self.dataframe[column] = self.dataframe[column].apply(lambda x: self.checkTimestampInSec(str(x)))
            if base == 'ms':
                self.dataframe[column] = self.dataframe[column].apply(lambda x: self.checkTimestampInMSec(str(x)))

            self.dataframe[column] = self.dataframe[column].apply(lambda x: self.checkAllIsDigit(str(x)))

            self.changeNanValues(column=column, nan_values_set_to=nan_values_set_to)

            msg = '{} is in Unix TIMESTAMP Type'.format(column)
        except Exception as e:
            msg = 'Error validating column {} to Unix TIMESTAMP : {}'.format(column, e)
            raise TypeError (msg)
        return msg