import pandas as pd
import numpy as np
import json

class DfConverter:
    # Constructor
    def __init__(self):
        return
    
    # Methods
    def JsonRecordsToColumns(self, dataframe, columns=[], inplace=False, drop=False):
        '''
        Converts a dataframe with json records to a dataframe with columns.
        
        Parameters: 
            dataframe (pandas.DataFrame): Dataframe with json records
            columns (str, list<str>): Columns of type dict
            inplace (bool): If True, the dataframe is modified in place
            drop (bool): If True, the json records are dropped
        '''
        
        # CHECK 
        if (not isinstance(dataframe, pd.DataFrame)):
            raise TypeError
        if not ((isinstance(columns, list)) or (isinstance(columns, str))):
            raise TypeError
        if (not isinstance(inplace, bool)):
            raise TypeError
        if (not isinstance(drop, bool)):
            raise TypeError
        
        # INIT
        # Set columns
        if isinstance(columns, list):
            if (len(columns) == 0):
                columns = dataframe.columns.to_list()
        else:
            columns = [columns]
        
        # Init dataframe with inplace
        if not inplace:
            dataframe = dataframe.copy()
            
        # PROCESS
        for c in columns:
            # get data
            data = dataframe[c].to_list()
            dataframe = pd.concat([dataframe, pd.json_normalize(data).add_prefix(c + ".")], axis=1)

        # DROP
        if drop:
            dataframe.drop(columns=columns, inplace=True)
        
        # RETURN DF
        return dataframe
    
    def ListToColumns(self, dataframe, columns=[], inplace=False, drop=False):
        '''
        Converts a dataframe with list to a dataframe with columns.
        
        Parameters: 
            dataframe (pandas.DataFrame): Dataframe with json records
            columns (str, list<str>): Columns of type dict
            inplace (bool): If True, the dataframe is modified in place
            drop (bool): If True, the json records are dropped
        '''
        
        # CHECK 
        if (not isinstance(dataframe, pd.DataFrame)):
            raise TypeError
        if not ((isinstance(columns, list)) or (isinstance(columns, str))):
            raise TypeError
        if (not isinstance(inplace, bool)):
            raise TypeError
        if (not isinstance(drop, bool)):
            raise TypeError
        
        # INIT
        # Set columns
        if isinstance(columns, list):
            if (len(columns) == 0):
                columns = dataframe.columns.to_list()
        else:
            columns = [columns]
        
        # Init dataframe with inplace
        if not inplace:
            dataframe = dataframe.copy()
            
        # PROCESS
        # Init new dataset
        new_dataset = pd.DataFrame()
        # For each columns
        for c in columns:
            # For each rows
            for index in dataframe.index.to_list():
                # Create temp dataframe
                dataset_temp = pd.concat([dataframe.iloc[[index]]]*len(dataframe[c].iloc[[index]].to_list()[0]), ignore_index=True)
                # Create new columns
                dataset_temp[c + "_count"] = len(dataframe[c].iloc[[index]].to_list()[0])
                dataset_temp[c + "_index"] = np.arange(dataset_temp.shape[0])
                dataset_temp[c + "_value"] = dataframe[c].iloc[[index]].to_list()[0]
                # Add to the new_dataset
                new_dataset = pd.concat([new_dataset, dataset_temp])
        # If drop
        new_dataset.drop(columns=columns, inplace=True)

        # Update dataframe
        dataframe = new_dataset
        
        # RETURN DF
        return dataframe

    def JsonListToColumns(self, dataframe, columns=[], inplace=False, drop=False):
        '''
        Converts a dataframe with list of json to a dataframe with columns.
        
        Parameters: 
            dataframe (pandas.DataFrame): Dataframe with json records
            columns (str, list<str>): Columns of type dict
            inplace (bool): If True, the dataframe is modified in place
            drop (bool): If True, the json records are dropped
        '''
        
        # CHECK 
        if (not isinstance(dataframe, pd.DataFrame)):
            raise TypeError
        if not ((isinstance(columns, list)) or (isinstance(columns, str))):
            raise TypeError
        if (not isinstance(inplace, bool)):
            raise TypeError
        if (not isinstance(drop, bool)):
            raise TypeError
        
        # INIT
        # Set columns
        if isinstance(columns, list):
            if (len(columns) == 0):
                columns = dataframe.columns.to_list()
        else:
            columns = [columns]
        
        # Init dataframe with inplace
        if not inplace:
            dataframe = dataframe.copy()
            
        # PROCESS
        dataframe = self.ListToColumns(dataframe, columns=columns, inplace=False, drop=False)
        c = []
        for col in columns:
            c += [col + "_value"]
        dataframe = self.JsonRecordsToColumns(dataframe, columns=c, inplace=False, drop=False)

        if drop:
            dataframe.drop(columns=columns, inplace=True)

        # RETURN
        return dataframe