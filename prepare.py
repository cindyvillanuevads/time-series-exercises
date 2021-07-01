import numpy as np
import pandas as pd
# datetime utilities
from datetime import timedelta, datetime
# visualization
import matplotlib.pyplot as plt

# no yelling in the library
import warnings
warnings.filterwarnings("ignore")


def date_to_index (df, col_date):
    '''
    takes in a df and a name of the column that is a date. 
    return a df with the selected column in datetime format  as Index 
    '''
    #convert sale_date to datetime format
    df[col_date]= pd.to_datetime(df[col_date])
    #set date as index
    df = df.set_index(col_date).sort_index()
    return df



def prep_sales (df, col_date):
    '''
    takes in a df and the name of the column (date),
    return df  with the selected column in datetime format  as Index, new columns:
    month, day of week and sales_total
    '''
    
    #set date to index
    df = date_to_index (df, col_date)
    
    #create new columns
    df['month '] = df.index.month
    df['day_of_week' ] = df.index.day_name()
    df['sales_total'] = df.sale_amount * df.item_price
    #drop a column
    df = df.drop(columns ='Unnamed: 0')

    return df

def prep_germany (df, col_date):
    '''   
    takes in a dataframe and the name of the column (date),
    return dataframe  with the selected column in datetime format  as Index, new columns:
    month, day of week and sales_total
    
    '''

    # set date to index
    df = date_to_index(df, col_date)
    
    #create new columns
    df['month '] = df.index.month
    df['year' ] = df.index.year
    
    #fill na with cero
    df= df.fillna(0)
    
    #recalculate
    df['Wind+Solar'] = df['Solar'] + df['Wind']
    
    return df 


def distribution (df):
    '''
    takes in a df and plot individual variable distributions excluding object type
    '''
    cols =df.columns.to_list()
    for col in cols:
        if df[col].dtype != 'object':
            plt.hist(df[col])
            plt.title(f'Distribution of {col}')
            plt.xlabel('values')
            plt.ylabel('Counts of customers')
            plt.show()



def miss_dup_values(df):
    '''
    this function takes a dataframe as input and returns metrics for missing values and duplicated rows.
    '''
        # Total missing values
    mis_val = df.isnull().sum()
        # Percentage of missing values
    mis_val_percent = 100 * df.isnull().sum() / len(df)
        #total of duplicated
    dup = df.duplicated().sum()  
        # Percentage of missing values
    dup_percent = 100 * dup / len(df)
        # Make a table with the results
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        # Rename the columns
    mis_val_table_ren_columns = mis_val_table.rename(columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        # Sort the table by percentage of missing descending
    mis_val_table_ren_columns = mis_val_table_ren_columns[
    mis_val_table_ren_columns.iloc[:,1] != 0].sort_values('% of Total Values', ascending=False).round(1)
        # Print some summary information
    print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
           "There are " + str(mis_val_table_ren_columns.shape[0]) +
           " columns that have missing values.")
    print( "  ")
    print (f"** There are {dup} duplicate rows that represents {round(dup_percent, 2)}% of total Values**")
        # Return the dataframe with missing information
    return mis_val_table_ren_columns
    
