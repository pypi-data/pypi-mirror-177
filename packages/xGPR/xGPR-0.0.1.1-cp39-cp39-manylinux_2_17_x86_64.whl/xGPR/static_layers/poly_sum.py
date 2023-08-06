"""Provides the PolySumStatLayer for faster implementation of a
PolySum kernel.
"""
import sys
import os

import numpy as np
try:
    import cupy as cp
except:
    pass

from ..kernels.convolution_kernels.graph_polysum import GraphPolySum
from ..data_handling.offline_data_handling import OfflineDataset

class PolySumStatLayer:
    """Provides tools for implementing a kernel that is a sum of polynomial
    kernels across all vertices in two input graphs. The input dataset should
    have x-values that are 3d arrays where shape[1] is vertices and shape[2]
    is num features per vertex. The outputs can be used as inputs to
    a LinearKernel, preferably with 'intercept' set to False since this
    preprocessing includes a y-intercept.

    Attributes:
        poly_kernel: The polynomial kernel object that generates the
            features.
        device (str): One of ['cpu', 'gpu']. Indicates the current device.
        seq_width (int): The anticipated width (number of features) of
                each input sequence / series.
        num_features (int): The number of random features to generate.
            More = improved performance but slower feature extraction
            and slower model training.
        zero_arr: A convenience reference to either np.zeros or cp.zeros,
            depending on device.
    """

    def __init__(self, seq_width, device = "cpu",
            polydegree = 2, random_seed = 123,
            num_features = 512):
        """Constructor for the PolySum class.

        Args:
            seq_width (int): The anticipated width (number of features) of
                each input sequence / series.
            device (str): Must be one of ['cpu', 'gpu']. Indicates the current
                device for the feature extractor.
            polydegree (int): The degree of the polynomial. Currently only
                allowed to be in range 2 - 4 (higher values could lead to
                numerical instability and are seldom advisable).
            random_seed (int): The seed to the random number generator.
                Defaults to 123.
            num_features (int): The number of random features to generate.
                More = improved performance but slower feature extraction
                and slower model training. Defaults to 512.

        Raises:
            ValueError: If an unrecognized kernel type or other invalid
                input is supplied.
        """
        self.zero_arr = np.zeros
        if polydegree > 4 or polydegree < 2:
            raise ValueError("Currently only polynomial degrees in the "
                    "range 2-4 are allowed.")

        self.seq_width = seq_width
        self.num_features = num_features
        self.num_features = num_features
        xdim = (1, 1, seq_width)
        self.poly_kernel = GraphPolySum(xdim, self.num_features, random_seed,
                device = device, kernel_spec_parms = {"polydegree":polydegree})
        self.device = device




    def dataset_feat_extract(self, input_dataset, output_dir):
        """Performs feature extraction,
        saves the results to a specified location, and returns an
        OfflineDataset. This function should be used if it is
        desired to generate features for sequence / timeseries data
        prior to training. The resulting features should be used as
        input to a LinearKernel. Note that when
        making predictions, you should use x_feat_extract,
        which takes an x-array as input rather than a dataset.

        Args:
            input_dataset: Object of class OnlineDataset or OfflineDataset.
                You should generate this object using either the
                build_online_dataset, build_offline_fixed_vector_dataset
                or build_offline_sequence_dataset functions under
                data_handling.dataset_builder.
            output_dir (str): A valid directory filepath where the output
                can be saved.

        Returns:
            output_dataset (OfflineDataset): An OfflineDataset containing
                the xfiles and yfiles that resulted from the feature
                extraction operation. You can feed this directly to
                the hyperparameter tuning and fitting methods of a
                LinearKernel.

        Raises:
            ValueError: If the inputs are not valid a detailed ValueError
                is raised explaining the issue.
        """
        start_dir = os.getcwd()
        try:
            os.chdir(output_dir)
        except:
            raise ValueError("Invalid output directory supplied to the "
                    "feature extractor.")


        input_dataset.device = self.device
        xfiles, yfiles = [], []
        fnum = 0
        for xbatch, ybatch in input_dataset.get_chunked_data():
            xfile, yfile = f"CONV1d_FEATURES_{fnum}_X.npy", f"CONV1d_FEATURES_{fnum}_Y.npy"
            xtrans = self.zero_arr((xbatch.shape[0], self.num_features))
            xtrans[:] = self.poly_kernel.transform_x(xbatch)
            if self.device == "gpu":
                ybatch = cp.asnumpy(ybatch)
                xtrans = cp.asnumpy(xtrans)
            np.save(xfile, xtrans)
            np.save(yfile, ybatch)
            xfiles.append(xfile)
            yfiles.append(yfile)
            fnum += 1

        xdim = (input_dataset.get_ndatapoints(), self.num_features)
        updated_dataset = OfflineDataset(xfiles, yfiles,
                            xdim, input_dataset.get_ymean(),
                            input_dataset.get_ystd())

        os.chdir(start_dir)
        return updated_dataset


    def x_feat_extract(self, x_array, chunk_size = 1000):
        """Performs feature extraction using a 1d convolution kernel
        and returns an array containing the result. This function should
        be used if it is desired to generate features for sequence /
        timeseries data AFTER training (i.e. when making predictions).
        Note that when training, you should use dataset_feat_extract,
        which takes a dataset as input rather than an array.

        Args:
            x_array: A numpy array. Should be a 3d array with same shape[1]
                and shape[2] as the training set.
            chunk_size (int): The batch size in which the input data array
                will be processed. This limits memory consumption.

        Returns:
            x_features: A 2d numpy array of shape (N, M) for
                N datapoints, M features that results from applying
                the feature extraction operation to the input.

        Raises:
            ValueError: If the inputs are not valid a detailed ValueError
                is raised explaining the issue.
        """

        x_features = []
        for i in range(0, x_array.shape[0], chunk_size):
            cutoff = min(x_array.shape[0], i + chunk_size)
            xtrans = self.zero_arr((cutoff - i, self.num_features))
            if xtrans.shape[0] == 0:
                continue
            if self.device == "gpu":
                x_in = cp.asarray(x_array[i:cutoff,:,:]).astype(cp.float32)
            else:
                x_in = x_array[i:cutoff,:,:]
            xtrans[:] = self.poly_kernel.transform_x(x_in)

            if self.device == "gpu":
                xtrans = cp.asnumpy(xtrans).astype(np.float64)
            x_features.append(xtrans)

        x_features = np.vstack(x_features)
        return x_features


    @property
    def device(self):
        """Property definition for the device attribute."""
        return self.device_



    @device.setter
    def device(self, value):
        """Setter for the device attribute."""
        if value not in ["cpu", "gpu"]:
            raise ValueError("Device must be in ['cpu', 'gpu'].")

        if "cupy" not in sys.modules and value == "gpu":
            raise ValueError("You have specified the gpu fit mode but CuPy is "
                "not installed. Currently CPU only fitting is available.")

        if value == "cpu":
            self.zero_arr = np.zeros
        else:
            self.zero_arr = cp.zeros
        self.poly_kernel.device = value
        self.device_ = value
