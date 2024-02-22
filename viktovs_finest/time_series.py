import pandas as pd
from statsmodels.formula.api import ols

def walk_forward_deviation(
    df
    , formula
    ):
    
    deviations = pd.Series()
    
    for i in range(2, df.shape[0]):
        model_i = ols(formula, df.iloc[:i]).fit()
        deviation_i = model_i.predict(df.iloc[i:]) - df.iloc[i:]["y"]
        deviations = pd.concat([deviations, deviation_i.reset_index(drop = True)])
        
    deviations = deviations.groupby(deviations.index).std().dropna()
    
    for i in range(len(deviations)):
        deviations.iloc[i] = deviations.iloc[: i + 1].max()
        
    return deviations