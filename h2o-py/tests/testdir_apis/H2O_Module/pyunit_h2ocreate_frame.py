from __future__ import print_function
import sys
sys.path.insert(1,"../../../")
from tests import pyunit_utils
import h2o
import random

# DISCLAMINER
#
# The main function of API tests is to make sure that changes to the API are captured
# before the customers do.  This is to prevent breaking the customer code.  If the
# changes are necessary, we will have the chance to warn them about the changes.
#
# All API tests should be short and fast to run.  The main purposes of API tests are to
# make sure that the command in its most popular forms, run correctly when user types in
# correct input arguments.  Light weight checking will be provided on the command output
# to make sure that we are getting the correct responses.
#
# For exhaustive tests using all possible combination of input arguments, making sure all
# responses of the API commands are correct, or if in error, the correct error messages
# are sent should be done elsewhere.

def h2ocreate_frame():
    """
    h2o.create_frame(frame_id=None, rows=10000, cols=10, randomize=True, real_fraction=None,
     categorical_fraction=None, integer_fraction=None, binary_fraction=None, time_fraction=None,
      string_fraction=None, value=0, real_range=100, factors=100, integer_range=100,
      binary_ones_fraction=0.02, missing_fraction=0.01, has_response=False, response_factors=2,
      positive_response=False, seed=None, seed_for_column_types=None)

    Testing the h2o.create_frame() command here.  Copied from pyunit_NOPASS_javapredict_dynamic_data_paramsDL.py

    :return: none if test passes or error message otherwise
    """

    try:
        # Generate random dataset
        dataset_params = {}
        dataset_params['rows'] = random.sample(list(range(50,150)),1)[0]
        dataset_params['cols'] = random.sample(list(range(3,6)),1)[0]
        dataset_params['categorical_fraction'] = round(random.random(),1)
        left_over = (1 - dataset_params['categorical_fraction'])
        dataset_params['integer_fraction'] = round(left_over - round(random.uniform(0,left_over),1),1)
        if dataset_params['integer_fraction'] + dataset_params['categorical_fraction'] == 1:
            if dataset_params['integer_fraction'] > dataset_params['categorical_fraction']:
                dataset_params['integer_fraction'] = dataset_params['integer_fraction'] - 0.1
            else:
                dataset_params['categorical_fraction'] = dataset_params['categorical_fraction'] - 0.1
        dataset_params['missing_fraction'] = random.uniform(0,0.5)
        dataset_params['has_response'] = False
        dataset_params['randomize'] = True
        dataset_params['factors'] = random.randint(2,5)
        print("Dataset parameters: {0}".format(dataset_params))

        distribution = random.sample(['bernoulli','multinomial','gaussian','poisson','gamma'], 1)[0]
        if   distribution == 'bernoulli': dataset_params['response_factors'] = 2
        elif distribution == 'gaussian':  dataset_params['response_factors'] = 1
        elif distribution == 'multinomial': dataset_params['response_factors'] = random.randint(3,5)
        else:
            dataset_params['has_response'] = False
        print("Distribution: {0}".format(distribution))

        train = h2o.create_frame(**dataset_params)
        return_type = "H2OFrame"
        pyunit_utils.verify_return_type("h2o.create_frame()", return_type, train.__class__.__name__)
        assert train.ncol==dataset_params['cols'], "h2o.create_frame() create frame with wrong column number."
        assert train.nrow==dataset_params['rows'], "h2o.create_frame() create frame with wrong row number."
    except Exception as e:
        assert False, "h2o.create_frame() command not is working."

if __name__ == "__main__":
    pyunit_utils.standalone_test(h2ocreate_frame)
else:
    h2ocreate_frame()
