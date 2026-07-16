import pytest
import sys
import pandas as pd
import pandas.testing as pdt
import numpy as np
import numpy.testing as npt

from PyPOW.__main__ import convert_files

def mock_np_savetxt(newfile, data, **kwargs):
    test_data = np.loadtxt(newfile)
    real_data = data
    npt.assert_almost_equal(test_data, real_data)

def mock_pd_to_csv(df, file):
    print(file)
    reference_df = pd.read_csv(file, index_col=0)
    pdt.assert_frame_equal(reference_df, df, check_exact=False)

def test_file_conversion(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", [sys.argv[0], "tests/ASG1_1.XRDML",])
        m.setattr("numpy.savetxt", mock_np_savetxt)
        m.setattr("pandas.DataFrame.to_csv", mock_pd_to_csv)
        convert_files()
