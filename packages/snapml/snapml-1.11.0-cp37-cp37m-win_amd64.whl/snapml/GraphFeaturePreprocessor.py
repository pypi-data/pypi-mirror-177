# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2022. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# ******************************************************************

import numpy as np

from snapml._import import import_libsnapml
from .version import __version__

libsnapml = import_libsnapml(False)


class GraphFeaturePreprocessor:

    """
    Graph-pattern-based feature engineering preprocessor.

    This preprocessor is used to enrich the feature vectors with additional
    features based on graph patterns and graph vertex statistics. The preprocessor
    maintains an internal dynamic graph representation based on the forwarded feature
    vectors. Each feature vector forwarded to the preprocessor represents a graph
    edge and it should contain at least the following raw features: edge ID, source
    vertex ID, target vertex ID, and timestamp. The internal graph representation
    is updated with the forwarded feature vectors and the graph-based feature
    engineering is performed using the updated graph. To reduce the memory footprint
    of the preprocessor, old edges are removed from the graph after performing feature
    engineering, as explained in ``transform()``.

    There are two types of graph-based features that this preprocessor computes:

    1) graph patterns - for each forwarded feature vector, this preprocessor searches for
    graph patterns it takes part in. The graph patterns that can be used are: fan in/out,
    degree in/out, scatter-gather, temporal cycle, and length-constrained simple cycle.

    2) graph vertex statistics - for each vertex in each forwarded feature vector,
    the preprocessor computes various statistical properties based on the selected raw
    features of the outgoing or incoming edges. The statistical properties that can be
    computed are: number of neighboring vertices (fan), number of incident edges (degree),
    fan/degree ratio, as well as average, sum, minimum, maximum, median, var, skew, and
    kurtosis of the selected raw features.

    Attributes
    ----------
    params : dict
        Parameters of this graph preprocessor.

        These parameters are used to define which graph pattern and graph vertex statistics
        features are going to be computed in ``transform()``. Valid parameter keys can be
        listed with ``get_params()`` and can be modified using ``set_params()``. The description
        of the given parameters are:

        num_threads : int, default=12
            Number of threads used in the computation
        time_window : int, default=10*3600
            Default time window value used if no graph pattern has been enabled

        vertex_stats : bool, default=False
            Enable generation of features based on vertex statistics
        vertex_stats_cols : array-like of int, default: [3]
            Columns of the raw feature vectors used for generating vertex statistics features
        vertex_stats_feats : array-like of int, default: [0, 1, 2, 3, 4, 8, 9, 10]
            Array indicating which vertex statistics properties are computed. The mapping
            between the values of this array and the statistical properties is the following:
            0:fan, 1:degree, 2:ratio, 3:average, 4:sum, 5:minimum,
            6:maximum, 7:median, 8:var, 9:skew, 10:kurtosis

        In the following parameters, <pattern-name> denotes one of the following graph
        pattern names: fan, degree, scatter-gather, temp-cycle, lc-cycle. These graph pattern
        names correspond to fan in/out, degree in/out, scatter-gather, temporal cycle,
        and length-constrained simple cycle patterns, respectively.

        <pattern-name> : bool
            Enable generation of graph pattern features based on <pattern-name> pattern
        <pattern-name>_tw : int
            Time window used for computing the <pattern-name> patterns. Increasing the time
            window enables finding more patters, but it also makes the problem more time consuming.
        <pattern-name>_bins : array-like of int
            Array used for describing the bin sizes. Bin i contains patterns of size S,
            where bin[i] >= S > bin[i+1]. The last bin contains the patterns of size greater than or
            equal to bin[i].

        lc-cycle_len : int, default=10
            Length constraint used when searching for length-constrained simple cycles. Increasing
            the value of this parameter enables finding longer cycles, but it also makes the problem
            more  time consuming.

    """

    def __init__(self):
        self.preproc = libsnapml.gf_allocate()

        self.params = {
            "num_threads": 12,  # number of software threads to be used
            "time_window": 10 * 3600,  # time window used if no pattern was specified
            "vertex_stats": True,  # produce vertex statistics
            "vertex_stats_cols": [
                3
            ],  # produce vertex statistics using the selected input columns
            # features: 0:fan,1:deg,2:ratio,3:avg,4:sum,5:min,6:max,7:median,8:var,9:skew,10:kurtosis
            "vertex_stats_feats": [
                0,
                1,
                2,
                3,
                4,
                8,
                9,
                10,
            ],  # fan,deg,ratio,avg,sum,var,skew,kurtosis
            # fan in/out parameters
            "fan": True,
            "fan_tw": 12 * 3600,
            "fan_bins": [
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                26,
                27,
                28,
                29,
                30,
            ],
            # in/out degree parameters
            "degree": False,
            "degree_tw": 12 * 3600,
            "degree_bins": [
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                26,
                27,
                28,
                29,
                30,
            ],
            # scatter gather parameters
            "scatter-gather": False,
            "scatter-gather_tw": 120 * 3600,
            "scatter-gather_bins": [
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                26,
                27,
                28,
                29,
                30,
            ],
            # temporal cycle parameters
            "temp-cycle": False,
            "temp-cycle_tw": 480 * 3600,
            "temp-cycle_bins": [
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                26,
                27,
                28,
                29,
                30,
            ],
            # length-constrained simple cycle parameters
            "lc-cycle": False,
            "lc-cycle_tw": 240 * 3600,
            "lc-cycle_len": 10,
            "lc-cycle_bins": [2, 3, 4, 5, 6, 7, 8, 9, 10],
        }
        libsnapml.gf_set_params(self.preproc, self.params)

    def __setstate__(self, state):
        self.params = state[1]
        preproc = libsnapml.gf_allocate()
        libsnapml.gf_set_params(preproc, self.params)
        libsnapml.gf_import_graph(preproc, state[0])
        self.preproc = preproc

    def __getstate__(self):
        out_dims = libsnapml.gf_get_output_array_dims(self.preproc)
        features = np.zeros((out_dims[0], out_dims[1]), dtype="float64")
        libsnapml.gf_export_graph(self.preproc, features)
        state = [features, self.params]
        return state

    #######################################
    # GET PARAMETERS
    def get_params(self):

        """
        Get the parameters of this graph preprocessor.

        Returns
        -------
        params : dict
        """

        return self.params

    #######################################
    # SET PARAMETERS
    def set_params(self, params):

        """
        Set the parameters of this graph preprocessor.

        Valid parameter keys can be listed with ``get_params()``.

        Invoking this function clears the existing internal graph representation.

        Returns
        -------
        params : dict
        """

        for key in params:
            if key in self.params:
                self.params[key] = params[key]
            else:
                raise KeyError("Unsupported key: " + key)
        libsnapml.gf_set_params(self.preproc, self.params)

    #######################################
    # LOAD THE GRAPH FROM NUMPY ARRAY
    def fit(self, features):

        """
        Create the internal graph representation based on the feature vectors in ``features``.

        This function clears the existing internal graph representation before creating a new
        graph representation based on the input feature vectors.

        Parameters
        ----------
        features : array-like of float, shape = (n_samples, n_raw_features)
            Input feature vectors representing graph edges with raw features. Each feature vector
            should have the following format:
            [Edge ID, Source Vertex ID, Target Vertex ID, Timestamp, <other raw features>]
        """

        libsnapml.gf_import_graph(self.preproc, features)

    #######################################
    # UPDATE THE GRAPH
    def partial_fit(self, features):

        """
        Update the internal graph representation based on the batch of feature vectors ``features``.

        This method inserts the edges defined by the feature vectors from ``features`` into the internal
        graph of the preprocessor and removes "old" edges from it. "Old" edges are defined as the edges
        older than a time window value that is equal to the maximum time window value specified for graph
        patterns in ``params``, or, if no graph pattern was enabled in ``params``, is equal to
        ``time_window`` from ``params``.

        Parameters
        ----------
        features : array-like of float, shape = (n_samples, n_raw_features)
            Input feature vectors representing graph edges with raw features. Each feature vector should
            have the following format:
            [Edge ID, Source Vertex ID, Target Vertex ID, Timestamp, <other raw features>]
        """

        libsnapml.gf_partial_fit(self.preproc, features)

    #######################################
    # ENRICH FEATURE VECTORS
    def transform(self, features_in):

        """
        Generate the graph-based features for the current batch of feature vectors ``features_in``.

        This method inserts the edges defined by the feature vectors from ``features_in`` into the internal
        graph of the preprocessor and computes the graph-based features on such an updated graph. The input
        feature vectors are updated with the graph-based features and are returned as the output. After the
        computation, "old" edges are removed from the internal graph representation. "Old" edges are defined
        as the edges older than a time window value that is equal to the maximum time window value specified
        for graph patterns in ``params``, or, if no graph pattern was enabled in ``params``, is equal to
        ``time_window`` from ``params``.

        The parameters ``params`` of this preprocessor determine how many graph-based features are generated.

        For graph-pattern features, the number of additional features generated depends on the number of
        bins specified. Enabling ``scatter-gather``, ``temp-cycle``, or  ``lc-cycle`` increases the number
        of generated patterns by the number of bins specified for each pattern. Because enabling
        ``fan``(``degree``)` results in generating fan-in and fan-out patterns (degree-in and degree-out
        for ``degree``), enabling ``fan`` or ``degree`` increases the number of generated features by
        2x the number of bins specified for each pattern.

        For graph vertex statistics features, the number of additional features generated depends on both
        the selected vertex statistics properties in ``vertex_stats_feats`` and the number of raw feature
        columns ``vertex_stats_cols`` used for generating those statistics. Specifying 0 (fan), 1 (degree),
        or 2 (ratio) in ``vertex_stats_feats`` increases the number of graph features computed by 4. The
        reason for this is because each vertex statistics feature is computed for the incoming and outgoing
        edges of the source and target vertex of each forwarded feature vector in ``features_in``.
        Because the statistical features other than fan, deg, and ratio are computed using each column specified
        in ``vertex_stats_cols``, each such statistical feature increases the number of graph features
        by ``4 x vertex_stats_cols.size``.

        Parameters
        ----------
        features_in : array-like of float, shape = (n_samples, n_raw_features)
            Input feature vectors representing graph edges with raw features. Each feature vector should have
            the following format:
            [Edge ID, Source Vertex ID, Target Vertex ID, Timestamp, <other raw features>]

        Returns
        -------
        features_out: array-like of float, shape = (n_samples, n_raw_features + n_eng_features)
            Feature vectors with additional n_eng_features graph-based features. The features that
            are computed can be defined using ``set_params()`` function. The format of each output feature
            vector is the following:
            [Edge ID, Source Vertex ID, Target Vertex ID, Timestamp, <other raw features>, <graph-based features>]
        """

        num_out_features = (
            libsnapml.gf_get_num_engineered_features(self.preproc)
            + features_in.shape[1]
        )
        features_out = np.zeros(
            (features_in.shape[0], num_out_features), dtype="float64"
        )

        libsnapml.gf_transform(self.preproc, features_in, features_out)

        return features_out

    #######################################
