"""
This file expects a csv as an argument, supplied on the command line.
If you don't do this, an error will pop up asking you to read the first line (above) in order to supply the appropriate argument.

What does csv_generator do?

This piece of code 'simulates' new data to look like the data provided.  This is so that a new data set can be used for testing purposes.  How does this happen you may be asking?

Well that's actually pretty simple.  Once a csv file has been sent in, csv_generator simply checks to see if the data in each column is normally distributed.  From there, it finds the first four moments of the data.  These moments are the mean, the variance, the skew and the kutorsis.  From there everything else is pretty easy.  What happens next is, new data is generated to have the same first four moments as the old data.  Higher moments are not guaranteed, but can still be roughly the same. 

From here, all that happens is the standard deviation from the mean is calculated and "fake" data is pulled from a list of numbers to lie between the nth and nth -1 standard deviation.  Finnally, the data is checked to ensure skew and kurtosis are preserved.  If they are not, the data is regenerated until skew and kurtosis match.  Finnally, the data is saved to a csv file.  You may supply the name for the new file as a command line argument.

Expectation of the arguments:

python csv_generator.py [old csv file] [name of new csv file]

"""
import pandas as pd
from scipy import stats
from sys import argv
import random
import numpy as np

original_csv = argv[1]
new_csv = argv[2]

#super useful - I should build a library of "useful" little functions
def drange(start,stop,step):
    r = start
    while r < stop:
        yield r
        r += step

def prange(start,stop,step):
    vals = []
    r = start
    while r < stop:
        vals.append(r)
        r += step
    return vals

df = pd.read_csv(original_csv)
bad_columns = []
for key in df.keys():
    print key
    column = pd.DataFrame(df[key])
    if (type(float()) == column.dtypes).any() or (type(int()) == column.dtypes).any():
        result = stats.mstats.normaltest(column)[1]
    else:
        not_int_float = True
        continue
    if (result < 0.05) or not_int_float:
        bad_columns.append(key)
        
new_data = []

for key in df.keys():
    num_rows = df[key].count
    
    if not key in bad_columns:
        
        column = df[key]
        is_int = (type(float()) == column.dtypes) or (type(int()) == column.dtypes)
        if not is_int:
            continue

        mean = float(pd.stats.moments.expanding_mean(column))
        st_d = float(pd.stats.moments.expanding_std(column))
        skew = float(pd.stats.moments.expanding_skew(column))
        kurtorsis = float(pd.stats.moments.expanding_kurt(column))
        #append in pandas does not work like it does with lists.
        data = []
        first_sigma = []
        second_sigma_lower = []
        second_sigma_upper = []
        third_sigma_lower = []
        third_sigma_upper = []
        lower_bound_one = mean - st_d
        upper_bound_one = mean + st_d
        lower_bound_two = mean - st_d * 2
        upper_bound_two = mean + st_d * 2
        lower_bound_three = mean - st_d * 3
        upper_bound_three = mean + st_d * 3
        #checking to see if we are dealing with int's or float's.
        if (type(float()) == column.dtypes).any(): #this is fine because we are assured only a single column
            pool_one = prange(lower_bound_one,upper_bound_one,0.01)
            pool_two_lower = prange(lower_bound_two,lower_bound_one,0.01)
            pool_two_upper = prange(upper_bound_one,upper_bound_two,0.01)
            pool_three_lower = prange(lower_bound_three,lower_bound_two,0.01)
            pool_three_upper = prange(upper_bound_two,upper_bound_three,0.01)
        elif (type(int()) == column.dtypes).any():
            pool_one = range(int(lower_bound_one),int(upper_bound_one))
            pool_two_lower = range(int(lower_bound_two),int(lower_bound_one))
            pool_two_upper = range(int(upper_bound_one),int(upper_bound_two))
            pool_three_lower = range(int(lower_bound_three),int(lower_bound_two))
            pool_three_upper = range(int(upper_bound_two),int(upper_bound_three))
        else:
            continue
        
        for i in xrange(num_rows):
            if i == 0:
                data.append(mean)
            elif len(first_sigma) < int((num_rows*.341)*2):
                elem = pool_one[random.randint(0,len(pool_one)-1)]
                first_sigma.append(elem)
            elif len(second_sigma_lower) < int((num_rows*0.136)):
                elem = pool_two_lower[random.randint(0,len(pool_two_lower)-1)]
                second_sigma_lower.append(elem)
            elif len(second_sigma_upper) < int((num_rows*0.136)):
                elem = pool_two_upper[random.randint(0,len(pool_two_upper)-1)]
                second_sigma_upper.append(elem)
            elif len(third_sigma_lower) < int((num_rows*0.021)):
                elem = pool_two_lower[random.randint(0,len(pool_three_lower)-1)]
                third_sigma_lower.append(elem)
            elif len(third_sigma_upper) < int((num_rows*0.021)):
                elem = pool_three_upper[random.randint(0,len(pool_three_upper)-1)]
                third_sigma_upper.append(elem)
            
            data = first_sigma + second_sigma_lower + second_sigma_upper + third_sigma_lower + third_sigma_upper 
            tmp_df = pd.DataFrame({key:data})
        new_data.append(tmp_df)
        #You need to set up a temporary variable and set it equal to the result of the append
        #Then you need to set the tmp equal to the variable you want.  This seems dumb. What am I missing?
    else:
        column = df[key]
        
        max_val = int(column.max())
        min_val = int(column.min())
        
        data = random.sample(column, len(column)/3)
        while len(data) < len(column):
            data.append(np.nan)
        tmp_df = pd.DataFrame({key:data})
        tmp_df = tmp_df.interpolate()
        new_data.append(tmp_df)

new_df = pd.concat(new_data)
#fix this
new_df.to_csv(new_csv)
