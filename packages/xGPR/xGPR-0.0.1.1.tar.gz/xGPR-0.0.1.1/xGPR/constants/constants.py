"""Magic numbers for use by model classes."""
#The following are used by model classes.
MAX_VARIANCE_RFFS = 4096
MAX_TRAINING_RFFS = 10000
MAX_FINETUNING_RFFS = 8192
MAX_CLOSED_FORM_RFFS = 10000
MAX_GRID_RFFS = 4096
MAX_PRECOND_RANK = 4096

#The following are used by gridsearch and/or bayes_grid.
MAX_GRID_PTS_4D_OPT = 8
MAX_COND_VAL = 1e8

#The following are used by bayes_grid optimization.
NUM_INIT_BAYES_GRID_3D = 10
NUM_INIT_BAYES_GRID_4D = 5
NUM_ITER_PRE_RESTRICT_BAYES_GRID = 15

#The following are default settings for kernels that have
#special parameters.
DEFAULT_KERNEL_SPEC_PARMS = {"matern_nu":5/2,
        "conv_width":9, "split_points":[]}

#The following is used if an error is encountered during
#matrix decomposition.
DEFAULT_SCORE_IF_PROBLEM = 1e40
