from pyproj import Transformer
from sklearn.neighbors import KDTree
from sklearn.metrics import DistanceMetric
import numpy as np


class TrainingSetTooSmallError(Exception):
    pass


class ImmoNeighbors:
    """
    This object stores all necessary information for k nearest neighbor searches and obtaining rent data for those
    neighbors. There should be one such object per room category (one for 1-5 rooms each, one for 6+ rooms)
    """

    def __init__(self, x_train, max_distance: int = 2000, n_neighbors=50, area_weight=10):
        """
        Default constructor. Builds the necessary data structure for efficient nearest neighbor searches.

        :param x_train: A DataFrame having at least the following columns: [id,lat,lon,rent,area]. Column order does
        not matter. This frame will be altered inplace, so make sure that you only hand this function a copy if you
        need the original for anything
        :type x_train: pandas.DataFrame
        :param max_distance: The maximum distance of neighbors to consider. If you want to consider all regardless of
        distance, use np.inf.
        :param n_neighbors: The default parameter for k_neighbors queries
        :param area_weight: Parameter that governs how this model views distances. For k_neighbors queries we use a
        3-dim l^2 metric with weights [1,1,area_weight] on the space x,y,area
        :raises TrainingSetTooSmallError: If the training set is smaller than n_neighbors after being 'cleaned' of NaNs
        """

        self.max_dist = max_distance
        self.n_neighbors = n_neighbors

        # Make sure that x_train has all the columns necessary
        if not {'lat', 'lon', 'rent', 'area'}.issubset(set(x_train.columns)):
            raise KeyError('One or multiple necessary columns missing in ImmoNeighbors constructor.')

        # Throw out any unusable training data
        x_train['rent_m2'] = x_train['rent'] / x_train['area']
        x_train.dropna(subset=['lat', 'lon', 'rent', 'area'], inplace=True)

        # Convert WGS84 input to 1903+/LV95
        self.transformer = Transformer.from_crs('epsg:4326', 'epsg:2056')
        x_train['x'], x_train['y'] = self.transformer.transform(x_train['lon'], x_train['lat'])
        x_train.drop(columns=['lat', 'lon'], inplace=True)

        x_train.reset_index(inplace=True)
        if not n_neighbors <= len(x_train):  # not <= also catches NaNs
            raise TrainingSetTooSmallError('Either the parameter n_neighbors is too big or the training set is too '
                                           'small/contains too many NaNs')
        self.x_train = x_train

        # Construct the metric, which is l^2 metric with a weight of area_weight for the 3rd dim
        metric = DistanceMetric.get_metric('minkowski', p=2, w=[1, 1, area_weight])

        immo_array = x_train[['x', 'y', 'area']].to_numpy()
        # Leaf_size should be relatively high in our case since that keeps memory consumption low while sacrificing
        # performance for actual searches. Is built faster though
        self.tree = KDTree(immo_array, leaf_size=100, metric=metric)

    def __dists_to_weights(self, dists: np.ndarray, min_distance=50) -> np.ndarray:
        """
        Private function that computes weights for the weighted_percentiles public function.

        :param dists: An array of distances
        :param min_distance: The minimum value to set distances to. If this is too small (0 for example), 1 very close
        data point will easily dominate the whole dataset.
        :return: Weights which are inversely proportional to distance and sum to 1. If all other objects are further
        than self.max_dist away, NaN is returned for all weights
        """
        dists = np.maximum(dists, min_distance)
        dists[dists > self.max_dist] = np.inf
        weights = np.divide(1, dists)
        with np.errstate(invalid='ignore'):
            # This will trigger Runtime Warnings for dividing by NaN lines.
            # This is expected and proper behaviour
            weights = weights / np.sum(weights, axis=1, keepdims=True)
        return weights

    def k_neighbors(self, points: np.ndarray, k: int = 'default'):
        """
        Queries for the k nearest neighbors. Per default takes the n_neighbors value that was given in the constructor.
        If points contains NaN or infty, the corresponding rows will be ignored and have 0 inds and NaN rents,dists in
        the returned arrays

        :param points: An array of shape (n_points,3). Columns should be lon,lat,area in that order. Make sure that
        lon,lat are in EPSG:4326 (WGS84)
        :param k: How many neighbors to return. Default is n_neighbors that was given in the constructor
        :return: Three arrays of shape (n_point,k): The distances, indices (wrt. self.x_train) and rents (normalized to
        area of the point) of the respective input row neighbors respectively. Ordered by dists
        :rtype: (np.ndarray,np.ndarray,np.ndarray)
        :raises TrainingSetTooSmallError: If k is greater than len(self.x_train)
        """

        # Note: NaNs or bad inputs are problematic since k_neighbors of the KDTree instance doesn't handle them well.
        # Set everything to 0 so k_neighbors can handle this.
        # The corresponding rows will be set to NaN manually at the end of the function
        invalid_rows = np.max(np.logical_or(np.isnan(points), np.isinf(points)), axis=1)
        if np.any(invalid_rows):
            points[invalid_rows, :] = 0

        # Transform to LV95 coordinates:
        points[:, 0], points[:, 1] = self.transformer.transform(points[:, 0], points[:, 1])

        if k == 'default':
            k = self.n_neighbors
        else:  # Already checked this if default is chosen
            if not k <= len(self.x_train):  # if not <= (as opposed to >) also catches NaNs etc
                raise TrainingSetTooSmallError('You have chosen a value of k that is larger than the initially chosen '
                                               'n_neighbors parameter and greater than the size of the training set. '
                                               'You probably want to call this function again with a smaller k or '
                                               'k="default"')

        dists, inds = self.tree.query(X=points, k=k, return_distance=True, sort_results=True, dualtree=True)

        # Get corresponding rent values
        rent_all = self.x_train['rent_m2'].to_numpy()
        rents = rent_all[inds] * np.expand_dims(points[:, -1], axis=1)  # Go back to absolute rents instead of per m^2

        # Take care of invalid rows. Because of python limitations, we can't set the inds to NaN.
        # dists of NaN lead to NaN weights as well. If used in the percentile function,
        # these rows will be set to NaN in the end as well
        inds[invalid_rows, :] = 0
        dists[invalid_rows, :] = np.NaN
        rents[invalid_rows, :] = np.NaN

        # By default sorted already
        return dists, inds, rents

    def weighted_percentiles(self, dists: np.ndarray, rents: np.ndarray, percentiles: list) -> np.ndarray:
        """
        The function that gives output suited for the boxplot-like figure. Kind of does what it sounds like.
        Data points are weighed inversely by distance. If all neighbors are too far away or dists are NaNs,
        the corresponding row will be NaN

        :param dists: distance array, from the output of k_neighbors
        :param rents: rents array, from the output of k_neighbors. Not assumed to be sorted.
        :param percentiles: A list of the percentiles. In [0,100]
        :return: An array of shape (len(dists),len(percentiles)) with the corresponding rent values
        :raises ValueError: if dists and rents do not have the same shape. Use the output of k_neighbors directly.
        """
        # Ensure that input is legal
        if dists.shape != rents.shape:
            raise ValueError('shape mismatch: dists and rents do not have the same shape')

        # Sort by rent
        inds_sorting = np.argsort(rents, axis=1)
        rents = np.take_along_axis(rents, inds_sorting, axis=1)
        dists = np.take_along_axis(dists, inds_sorting, axis=1)

        # Calculate weights and sum over them
        weights = self.__dists_to_weights(dists)
        cum_weights = np.cumsum(weights, axis=1)

        result_array = np.zeros(shape=(len(dists), len(percentiles)))
        # Iterate through each value in percentiles and find corresponding rent value
        for perc_ind, percentile in enumerate(percentiles):
            if percentile <= 0:
                # Find the first entry with non-zero weight
                p_inds = np.argmax(weights > 0, axis=1)
            elif percentile >= 100:  # (= is important because of potential floating point errors)
                # Look for the first entry with non-zero weight in the flipped array
                p_inds = weights.shape[1] - np.argmax(weights[:, ::-1] > 0, axis=1) - 1
            else:
                # Find the next entry with cum_weight greater than the percentile
                p_inds = np.argmax(np.logical_and(cum_weights > percentile / 100, weights > 0), axis=1)
            result_array[:, perc_ind] = rents[np.arange(len(rents)), p_inds]

        # Identify and treat rows where all neighbors are further away than max_dist. Otherwise these would show up as 0
        empty_rows = np.isnan(np.max(cum_weights, axis=1))
        result_array[empty_rows, :] = np.NaN

        return result_array

    def inds_to_ids(self, inds):
        """
        Transform DataFrame index to the unique id (e.g. double1groupid) of an apartment
        :param inds: Might be the output of k_neighbors
        :return: ndarray of the same shape as inds, with the ids
        """
        return self.x_train['id'].to_numpy()[inds]
