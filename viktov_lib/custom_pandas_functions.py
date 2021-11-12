# weighted average
def add_w_avg(row, avg_name, weight_name):
    return (row[avg_name] * row[weight_name]).sum() / row[weight_name].sum()
