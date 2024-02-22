### Import packages
import pandas as pd



def correlation_search_df(df, date_column, correlation_columns, metric_column):
    """
    This function takes a data frame and checks for correlation in the data over time. 
    :param df: dataframe to look at
    :param date_column: the dimension for which we are looking for correlation e.g. results over time
    :param correlation_columns: What other dimensions we want to check for correlation with thedate column
    :param metric_column: the metric of interest
    """
    # transform date column to date format and metric to numeric
    try:
        df[date_column] = pd.to_datetime(df[date_column])
    except:
        print("Datetime column contains not convertable entries")
        return None
    
    try:
        df[metric_column] = pd.to_numeric(df[metric_column])
    except:
        print("Metric column contains non numeric entries")
        return None
    
    # create overall performance dataframe
    overall_results = df[[date_column, metric_column]].groupby(date_column).sum()
    
    # run all the correlations and add to a new dataframe
    
    results_dict = {}
    for column in correlation_columns:
        
        for entry in df[column].unique():
            
            #set a filter to only look at relevant entries
            column_filter = df[column] == entry
            
            # create a dataframe in the dictionary
            results_dict[column + "_" + entry] = df[[date_column, metric_column]][column_filter].groupby(date_column).sum()
            

    # create a dict with empty lists to store names and correlations
    correlation_dict = {
        "Dimension": [],
        "Correlation": []
    }
    
    # loop through the results dict to store name and correlation in the correlation dict
    for dict_df in results_dict:
        correlation_dict["Dimension"].append(dict_df)
        correlation_dict["Correlation"].append(overall_results.corrwith(results_dict[dict_df])[0])

    # transform correlation dict into a pd dataframe
    correlation_df = pd.DataFrame(correlation_dict)
    
    return correlation_df