# weighted average
def add_w_avg(row, avg_name, weight_name):
    return (row[avg_name] * row[weight_name]).sum() / row[weight_name].sum()

def shares_by_dimenstion(df
                         , dimension : list
                         , split_dimension
                         , value
                         , benchmark_name = "Peer Group"
                        ):
    """
    Takes two columns of a dataframe and calculates the shares for a specific value
    :param dimension: Dimension you want to have the shares for
    :param split_dimension: The shares will be split among these two dimensions
    :param value: the metric you want to transfer into shares
    :param:benchmark_name:
    :return: pandas DataFrame
    """
    # pivot the dataframe to aggregat dimension and split dimension
    temp_df = df.pivot_table(index = dimension
                             , column = split_dimension
                             , values = value
                             , aggfunc = "sum"
                             )

    # extract different entries from split dimension
    temp_list = list(df[split_dimension]).unique())
    temp_list.sort()

    # loop throught columns to calculate each share
    for fg in temp_list:
        temp_df[f"{fg}_share"] = temp_df[fg] / temp_df[fg].sum()

    # delete obsolete columns
    temp_df.drop(temp_list, axis = 1, inplace = True)

    # rename columns
    temp_df.columns = dimension + temp_list

    return temp_df



def sort_rows_by_list(df
                      , sort_dimension
                      , sort_list
                     ):
    """
    This function takes a pandas DataFrame and sorts its rows by a given list
    :param df: pandas DataFrame you want to sort
    :param sort_dimension: The dimension you want to sort by
    :param sort_list: an ordered list how you want to sort the DataFrame
    :return: pandas DataFrame
    """
    temp_df = df.copy()

    # define the dimension to sort by as your index and sort by the given list
    temp_df.set_index(sort_dimension, inplace = True)
    temp_df = temp_df.loc[sort_list].reset_index()

    return temp_df



def transform_two_line_df_into_one_line_df(df
                                           , sort_output_by = False
                                           , second_half_name = "B_"
                                          ):
    """
    This function takes a two row pandas DataFrame and concatenates it horizontally.
    :param df: pandas DataFrame you want to transform. NEEDS TO HAVE AN INDEX
    :param sort_output_by: List of how you want the output to be sorted
    :param second_half_name: The Prefix added to the new Columns
    """
    if sort_output_by:
        index_list = sour_output_by
    else:
        index_list = list(df.index)

    temp_dict = dict()

    for index in index_list():
        temp_dict[index] = df.loc[index]
        temp_dict[index] = pd.DataFrame(temp_dict[index]).transpose()
        temp_dict[index].reset_index(drop = True, inplace = True)

    temp_dict[index_list[1]].columns = [(second_half_name + c) for c in list(temp_dict[index_list[1]].columns)]

    return pd.merge(temp_dict[index_list[0]]
                    , temp_dict[index_list[1]]
                    , left_index = True
                    , right_index = True
                   )



def dimension_as_horizontal_shares_in_columns(df
                                              , vertical_dimension
                                              , horizontal_dimension
                                              , metric
                                             ):
    """
    This function takes a pandas DataFrame as an input and transforms it so that
    one dimension is on the vertical axis and another on the horizontal
    The value shown is the share of each row adding up to 100%
    :param df: Your pandas DataFrame
    :param vertical_dimension: The dimension you wnat to see on the vertical axis
    :param horizontal_dimension: The dimension you wnat to see on the horizontal axis
    :param metric: The metric you want to transform into shares
    :return: pandas DataFrame
    """
    temp_df = df.pivot_table(index = vertical_dimension
                             , columns = horizontal_dimension
                             , values = metric
                             , aggfunc = "sum"
                            ).reset_index()

    # create a list of all relevant columns
    column_list = list(temp_df.columns)
    column_list.remove(vertical_dimension)

    # create a total column
    temp_df["Total"] = temp_df.sum(axis=1)

    # calculate shares for all columns and drop obsolete columns
    for column in columns:
        temp_df[f"{column}_share"] = temp_df[column] / temp_df["Total"]
        temp_df[f"{column}_share"].fillna(0, inplace = True)
        temp_df[f"{column}_share"] = temp_df[f"{column}_share"].astype(float).map("{:.8}".format)
        temp_df.drop(column, axis = 1, inplace = True)

    return temp_df.drop("Total", axis = 1)