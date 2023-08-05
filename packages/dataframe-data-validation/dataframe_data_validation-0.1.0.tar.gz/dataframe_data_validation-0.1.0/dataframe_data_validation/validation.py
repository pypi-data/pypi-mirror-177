import pandas as pd

class Validation():
    
    
    def validateInteger(data_frame, column):
        """
        validating integer data types
        :param data_frame: Pandas DataFrame
        :param column: columns for validation
        :return: True if all task complete Successfully, otherwise False
        """

        try:
            # first, trying to apply pd.to_numeric to desire column. if anything goes wrong then value will set to None
            data_frame[column] = data_frame[column].apply(pd.to_numeric, errors='coerce')

            # we need to remove None values for next step, so ...
            data_frame.dropna(inplace=True)
            data_frame.reset_index(drop=True, inplace=True)

            # then change column type to int, because it probably is float (pd.to_numeric)
            data_frame[column] = data_frame[column].astype(int)
            msg = '{} converted to integer successfully'.format(column)
        except Exception as e:
            msg = 'Error converting column {} to integer : {}'.format(column, e)
            return [False , msg]
        return [True , msg]

