# Melon analytics pricing

This package provides one class: ImmoNeighbors.
You should train one such instance per floor(number_of_rooms) from 1 to 6+.
Example code:

'''
no_of_rooms = 3

training_data = immo[np.floor(immo["rooms"]) == no_of_rooms]
neighbors = ImmoNeighbors(training_data.copy())

apartments = apartments_to_benchmark[['lon','lat','area']].to_numpy()
dists,inds,rents = neighbors.k_neighbors(apartments)

rent_percentiles = neighbors.weighted_percentiles(dists,rents,percentiles=[10,50,90])
'''

Usually, problematic inputs will be ignored and have a corresponding row of NaNs in the output.
More details about that can be found in the documentation of the respective function.