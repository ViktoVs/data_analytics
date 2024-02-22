import pandas as pd
import re

### to-do add some histograms for each value

def df_quick_check(df):
    # Check and count each column for:
    results_dict = {"Name": []
                    , "Missing Values": []
                    , "Numerical Values": []
                    , "Only Alphabetical Values": []
                    , "Alphanumerical Values": []
                    , "Values with Special Characters": []
                    , "Date Values": []
                   }
    
    for c in df.columns:
        results_dict["Name"].append(c)
        results_dict["Missing Values"].append(sum(df[c].isna()))
        results_dict["Numerical Values"].append(sum([str(x).isdigit() for x in list(df[c])]))
        results_dict["Only Alphabetical Values"].append(sum([str(x).isalpha() for x in list(df[c]) if str(x) != "nan"]))
        results_dict["Alphanumerical Values"].append(sum([str(x).isalnum() for x in list(df["purchase_price"]) if str(x) != "nan"])) # exclude whitespace
        results_dict["Values with Special Characters"].append(sum([not str(x).isalnum() for x in list(df["purchase_price"]) if str(x) != "nan"])) # values with special characters
        results_dict["Date Values"].append(sum(df[c].str.contains("^\d{4}-\d{2}-\d{2}").fillna(False))) # date values
    
    return pd.DataFrame.from_dict(results_dict, orient="index", columns=results_dict["Name"]).drop("Name")
