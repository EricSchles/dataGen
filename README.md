# Data Gen

#What does csv_generator do?

This piece of code 'simulates' new data to look like the data provided.  This is so that a new data set can be used for testing purposes.  How does this happen you may be asking?

Well that's actually pretty simple.  Once a csv file has been sent in, csv_generator simply checks to see if the data in each column is normally distributed.  From there, it finds the first four moments of the data.  These moments are the mean, the variance, the skew and the kutorsis.  From there everything else is pretty easy.  What happens next is, new data is generated to have the same first four moments as the old data.  Higher moments are not guaranteed, but can still be roughly the same. 

From here, all that happens is the standard deviation from the mean is calculated and "fake" data is pulled from a list of numbers to lie between the nth and nth -1 standard deviation.  Finnally, the data is checked to ensure skew and kurtosis are preserved.  If they are not, the data is regenerated until skew and kurtosis match.  Finnally, the data is saved to a csv file.  You may supply the name for the new file as a command line argument.

#Expectation of the arguments:

python csv_generator.py [old csv file] [name of new csv file]
