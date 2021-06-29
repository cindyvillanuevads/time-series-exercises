import pandas as pd
import requests
import os


def get_url_data (url):
    '''
    take in url as string and return a data un dictionay type
    Example
    get_url_data ('https://python.zach.lol/api/v1/items')
    '''
    # use the url as part of a request in order to receive a response
    response = requests.get(url)
    # parse the response into tabular data
    data = response.json()
    return data



def get_df (key1,key2, max_page, url_page, name_csv):
   
    """
    this function return a df
    key1: key of you first dictionary 
    key2: key of you second dictionary 
    max_page : total number of pages
    url_page: url for a single page
    name_csv: a name to save you df as csv
    Example: 
    get_df ('payload','items', 3, 'https://python.zach.lol/api/v1/items?page=', 'itemexample.csv')
    """

    if os.path.isfile(name_csv):
        
        # If csv file exists, read in data from csv file.
        print("this file already exists")
        df = pd.read_csv(name_csv, index_col=0)
    else:     
        #create an empty list
        items_list = []
        #get the max number of page
        n = max_page
        #use a for loop to get all pages
        for i in range(1,n+1):
            url = url_page + str(i)
            response = requests.get(url)
            data = response.json()
            page_items = data[key1][key2]
            items_list += page_items
        df = pd.DataFrame (items_list)
        df.to_csv(name_csv)
    
    return df



