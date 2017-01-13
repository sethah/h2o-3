from __future__ import print_function
from builtins import str
from builtins import range
import sys, os
sys.path.insert(1,"../../../")
from tests import pyunit_utils
import h2o
import urllib.parse
from h2o.estimators.glm import H2OGeneralizedLinearEstimator

# DISCLAMINER
#
# The main function of API tests is to make sure that changes to the API are captured
# before the customers do.  This is to prevent breaking the customer code.  If the
# changes are necessary, we will have the chance to warn them about the changes.
#
# All API tests should be short and fast to run.  The main purposes of API tests are to
# make sure that the command in its most popular forms run correctly when user types in
# correct input arguments.  Light weight checking will be provided on the command output
# to make sure that we are getting the correct responses.
#
# For exhaustive tests using all possible combination of input arguments, making sure all
# responses of the API commands are correct, or if in error, the correct error messages
# are sent should be done elsewhere.

def h2osave_model():
    """
    h2o.save_model(model, path=u'', force=False)

    Testing the h2o.save_model() command here.

    :return: none if test passes or error message otherwise
    """
    try:
        training_data = h2o.import_file(pyunit_utils.locate("smalldata/logreg/benign.csv"))
        Y = 3
        X = [0, 1, 2, 4, 5, 6, 7, 8, 9, 10]

        model = H2OGeneralizedLinearEstimator(family="binomial", alpha=0, Lambda=1e-5)
        model.train(x=X, y=Y, training_frame=training_data)
        try:
            results_dir = pyunit_utils.locate("results")    # find directory path to results folder
            h2o.save_model(model, path=results_dir, force=True)       # save model
            assert os.path.isfile(os.path.join(results_dir, model._id)), "h2o.save_model() command is not working."

        except Exception as e:
            if 'File not found' in e.args[0]:
                print("Directory is not writable.  h2o.save_model() command is not tested.")
            else:
                assert False, "h2o.save_model() command is not working."
    except Exception as e:
        assert False, "h2o.save_model() command is not working."


if __name__ == "__main__":
    pyunit_utils.standalone_test(h2osave_model)
else:
    h2osave_model()
