import pandas as pd

def answer_count_textchoice(df
                            , question
                            , dimension
                           ):
    """
    This function counts the values from a survey and saves them in a pandas DataFrame
    If it contains multiple answers they will be split into single ones
    :param df: pandas DataFrame with survey results
    :param question: The question of the survey you want to count
    :param dimension: The name of the output column
    :return: pandas DataFrame
    """
    # create set for answers
    answer_set = set()

    # create a list of all not empty records to populate the answer set
    answer_list = [x for x in list(df.loc[: , question].dropna())]

    # loop through and split answers
    for answer in answer_list:
        for entry in answer.split(","):
            answer_set.add(entry)

    # add total dimension
    answer_set.add("Total")

    results_dict = dict()

    for answer in answer_set:
        if answer == "Total":
            results_dict[answer] = len(df.loc[: , question].drop_na())
        else:
            results_dict[answer] = len([x for x in df.loc[: , question].dropna()])

    return pd.DataFrame.from_dict(results_dict
                                  , orient="index"
                                  , columns=[dimension]
                                  , ascending = False
                                 )
    