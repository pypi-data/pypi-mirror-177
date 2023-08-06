import unittest
import warnings

import torch
import pandas as pd
from numpy import nan

from leaspy.io.data.data import Data
from leaspy.io.data.dataset import Dataset

from tests import LeaspyTestCase


class DatasetTest(LeaspyTestCase):

    def test_constructor_univariate(self):
        # no nans
        path_to_data = self.get_test_data_path('data_mock', 'univariate_data_for_dataset.csv')
        data = Data.from_csv_file(path_to_data)
        dataset = Dataset(data)

        self.assertEqual(dataset.n_individuals, 3)
        self.assertEqual(dataset.n_visits_max, 4)
        self.assertEqual(dataset.dimension, 1)
        self.assertEqual(dataset.n_visits, 9)
        self.assertEqual(dataset.n_observations, 9)  # since univariate

        values = torch.tensor([[[1.], [5.], [2.], [0.]],
                           [[1.], [5.], [0.], [0.]],
                           [[1.], [8.], [1.], [3.]]])

        mask = torch.tensor([[[1.], [1.], [1.], [0.]],
                        [[1.], [1.], [0.], [0.]],
                        [[1.], [1.], [1.], [1.]]])

        self.assertTrue(torch.equal(dataset.values, values))
        self.assertTrue(torch.equal(dataset.mask, mask))

    def test_constructor_multivariate(self):
        # no nans
        path_to_data = self.get_test_data_path('data_mock', 'multivariate_data_for_dataset.csv')
        data = Data.from_csv_file(path_to_data)
        dataset = Dataset(data)

        self.assertEqual(dataset.n_individuals, 3)
        self.assertEqual(dataset.n_visits_max, 4)
        self.assertEqual(dataset.dimension, 2)
        self.assertEqual(dataset.n_visits, 9)
        self.assertEqual(dataset.n_observations, 18)  # since bivariate without nans

        values = torch.tensor([[[1., 1.], [5., 2.], [2., 3.], [0., 0.]],
                               [[1., 1.], [5., 8.], [0., 0.], [0., 0.]],
                               [[1., 4.], [8., 1.], [1., 1.], [3., 2.]]])

        mask = torch.tensor([[[1., 1.], [1., 1.], [1., 1.], [0., 0.]],
                             [[1., 1.], [1., 1.], [0., 0.], [0., 0.]],
                             [[1., 1.], [1., 1.], [1., 1.], [1., 1.]]])

        timepoints = torch.tensor([
            [1., 2., 3., 0.],
            [1., 2., 0., 0.],
            [1., 2., 4., 5.]
        ])

        self.assertAllClose(dataset.values, values)
        self.assertTrue(torch.equal(dataset.mask, mask))
        self.assertAllClose(dataset.timepoints, timepoints)

    def test_n_observations_missing_values(self):

        path_to_data = self.get_test_data_path('data_mock', 'multivariate_data_for_dataset_with_nans.csv')
        data = Data.from_csv_file(path_to_data)
        dataset = Dataset(data)

        self.assertEqual(dataset.n_individuals, 3)
        self.assertEqual(dataset.n_visits_max, 4)
        self.assertEqual(dataset.dimension, 2)
        self.assertEqual(dataset.n_visits, 8)  # 1 row full of nans should have been dropped
        self.assertEqual(dataset.n_observations, 2*8-3)  # 3 nans

        values = torch.tensor([[[1., 1.], [2., 3.], [0., 0.], [0., 0.]],
                               [[1., 1.], [0., 8.], [0., 0.], [0., 0.]],
                               [[0., 4.], [8., 0.], [1., 1.], [3., 2.]]])

        mask = torch.tensor([[[1., 1.], [1., 1.], [0., 0.], [0., 0.]],
                             [[1., 1.], [0., 1.], [0., 0.], [0., 0.]],
                             [[0., 1.], [1., 0.], [1., 1.], [1., 1.]]])

        timepoints = torch.tensor([
            [1., 3., 0., 0.],
            [1., 2., 0., 0.],
            [1., 2., 4., 5.]
        ])

        self.assertAllClose(dataset.values, values)
        self.assertTrue(torch.equal(dataset.mask, mask))
        self.assertAllClose(dataset.timepoints, timepoints)

    def test_dataset_device_management_cpu_only(self):
        path_to_data = self.get_test_data_path('data_mock', 'multivariate_data_for_dataset_with_nans.csv')
        data = Data.from_csv_file(path_to_data)
        dataset = Dataset(data)

        self._check_dataset_device(dataset, torch.device('cpu'))

        dataset.move_to_device('cpu')
        self._check_dataset_device(dataset, torch.device('cpu'))

    @unittest.skipIf(not torch.cuda.is_available(),
                    'Device management involving GPU needs an available CUDA environment')
    def test_dataset_device_management_with_gpu(self):
        path_to_data = self.get_test_data_path('data_mock', 'multivariate_data_for_dataset_with_nans.csv')
        data = Data.from_csv_file(path_to_data)
        dataset = Dataset(data)

        self._check_dataset_device(dataset, torch.device('cpu'))

        dataset.move_to_device('cuda')
        self._check_dataset_device(dataset, torch.device('cuda'))

        dataset.move_to_device('cpu')
        self._check_dataset_device(dataset, torch.device('cpu'))

    def _check_dataset_device(self, dataset, expected_device):
        for attribute_name in dir(dataset):
            attribute = getattr(dataset, attribute_name)
            if isinstance(attribute, torch.Tensor):
                self.assertEqual(attribute.device.type, expected_device.type)

    def test_get_one_hot_encoding(self):

        nan_coding = 0 # nan -> level=0

        df = pd.DataFrame({
            'ID':     ['S1', 'S1', 'S1', 'S1', 'S2', 'S2'],
            'TIME':   [ 50.,  51.,  53.,  59., 35.3, 43.9],
            'FT_0-3': [ 1,    0,    3,    2,   1,    1   ],
            'FT_0-2': [ 1,    0,  nan,    2, nan,    1   ],
        })
        expected_masked_indices = [
            [0, 2, 1], [1, 0, 1], # nans
            [1, 2, 0], [1, 2, 1], [1, 3, 0], [1, 3, 1], # padded visits
        ]

        # create the dataset
        dataset = Dataset(Data.from_dataframe(df))

        # basic checks on it
        self.assertEqual(dataset.n_individuals, 2)
        self.assertEqual(dataset.n_visits_max, 4)
        self.assertEqual(dataset.dimension, 2)
        self.assertEqual(dataset.n_visits, 6)
        self.assertEqual(dataset.n_observations, 6*2 - 2)  # 2 nans

        masked_indices = (1 - dataset.mask).nonzero(as_tuple=False).tolist()
        self.assertEqual(masked_indices, expected_masked_indices)

        # test the ordinal encodings
        for case_name, (ordinal_infos, warnings_unexpected, warnings_missing) in {
            "'true' ordinal infos": (
                {
                    'features': [
                        {'name': 'FT_0-3', 'max_level': 3},
                        {'name': 'FT_0-2', 'max_level': 2},
                    ],
                    'max_level': 3,
                },
                None, # warnings unexpected
                None, # warnings missing
            ),
            "'true' ordinal infos for features but faking a higher max_level": (
                {
                    'features': [
                        {'name': 'FT_0-3', 'max_level': 3},
                        {'name': 'FT_0-2', 'max_level': 2},
                    ],
                    'max_level': 5, # fake to check behavior
                },
                None,
                None,
            ),
            "ordinal infos with missing code=[3, 4] for FT_0-2": (
                {
                    'features': [
                        {'name': 'FT_0-3', 'max_level': 3},
                        {'name': 'FT_0-2', 'max_level': 4}, # +2
                    ],
                    'max_level': 4,
                },
                None,
                "Some features have missing codes:\n- FT_0-2 [[0..4]]: [3, 4] are missing",
            ),
            "ordinal infos with unexpected code=[3] for FT_0-3": (
                {
                    'features': [
                        {'name': 'FT_0-3', 'max_level': 2}, # -1
                        {'name': 'FT_0-2', 'max_level': 2},
                    ],
                    'max_level': 3,
                },
                "Some features have unexpected codes (they were clipped to the maximum known level):\n- FT_0-3 [[0..2]]: [3] were unexpected",
                None,
            ),
        }.items():

            with self.subTest(case_name=case_name):

                # we encode the levels for simplicity of tests
                lvls = torch.eye(1+ordinal_infos['max_level']).long()
                sfb = (1 - lvls.cumsum(-1))[..., :-1].tolist()
                lvls = lvls.tolist()

                # the potentially clipped code
                c1 = lambda c: min(c, ordinal_infos['features'][0]['max_level'])
                c2 = lambda c: min(c, ordinal_infos['features'][1]['max_level'])

                expected_pdf = torch.tensor([
                    [[lvls[c1(1)], lvls[0], lvls[c1(3)], lvls[c1(2)]], [lvls[c1(1)], lvls[c1(1)], lvls[nan_coding], lvls[nan_coding]]], # FT1
                    [[lvls[c2(1)], lvls[0], lvls[nan_coding], lvls[c2(2)]], [lvls[0], lvls[c2(1)], lvls[nan_coding], lvls[nan_coding]]], # FT2
                ])
                expected_sf = torch.tensor([
                    [[sfb[c1(1)], sfb[0], sfb[c1(3)], sfb[c1(2)]], [sfb[c1(1)], sfb[c1(1)], sfb[nan_coding], sfb[nan_coding]]], # FT1
                    [[sfb[c2(1)], sfb[0], sfb[nan_coding], sfb[c2(2)]], [sfb[0], sfb[c2(1)], sfb[nan_coding], sfb[nan_coding]]], # FT2
                ])
                # ft, ind, vis, lvl <-> ind, vis, ft, lvl
                expected_pdf = expected_pdf.transpose(0, 1).transpose(1, 2)
                expected_sf = expected_sf.transpose(0, 1).transpose(1, 2)

                # reset the cached one-hot encoding in dataset... (otherwise no recomputation with new ordinal_infos!)
                dataset._one_hot_encoding = None

                with warnings.catch_warnings(record=True) as ws_first:
                    # some warnings may occur here depending on `ordinal_infos`!
                    warnings.simplefilter('always')
                    pdf = dataset.get_one_hot_encoding(sf=False, ordinal_infos=ordinal_infos)

                with warnings.catch_warnings(record=True) as ws_second:
                    # no warnings expected the second time we retrieve the data!
                    warnings.simplefilter('always')
                    sf = dataset.get_one_hot_encoding(sf=True, ordinal_infos=ordinal_infos)

                self.assertAllClose(pdf, expected_pdf)
                self.assertAllClose(sf, expected_sf)

                ws_second = [str(w.message) for w in ws_second]
                self.assertEqual(ws_second, [])

                expected_ws_first = []
                if warnings_unexpected is not None:
                    expected_ws_first.append(warnings_unexpected)
                if warnings_missing is not None:
                    expected_ws_first.append(warnings_missing)

                ws_first = [str(w.message) for w in ws_first]
                self.assertEqual(ws_first, expected_ws_first)

    def test_get_one_hot_encoding_with_decimals(self):

        df = pd.DataFrame({
            'ID':     ['S1', 'S1', 'S1', 'S1', 'S2', 'S2'],
            'TIME':   [ 50.,  51.,  53.,  59., 35.3, 43.9],
            'X':      [ 1,    0.5,  3,    2,   1,    1   ], # only integers allowed!
            'Y':      [ 1,    0,  nan,    2, nan,    1   ],
        })
        dataset = Dataset(Data.from_dataframe(df))
        with self.assertRaisesRegex(ValueError, "integers"):
            dataset.get_one_hot_encoding(sf=False, ordinal_infos={})

    def test_get_one_hot_encoding_bad_fts(self):

        df = pd.DataFrame({
            'ID':     ['S1', 'S1', 'S1', 'S1', 'S2', 'S2'],
            'TIME':   [ 50.,  51.,  53.,  59., 35.3, 43.9],
            'X':      [ 1,    0,    3,    2,   1,    1   ],
            'Y':      [ 1,    0,  nan,    2, nan,    1   ],
        })
        # create the dataset
        dataset = Dataset(Data.from_dataframe(df))
        err_rx = "not consistent with features"

        ordinal_infos = {
            'features': [
                # bad var order
                {'name': 'Y', 'max_level': 3},
                {'name': 'X', 'max_level': 2},
            ],
            'max_level': 3,
        }
        with self.assertRaisesRegex(ValueError, err_rx):
            dataset.get_one_hot_encoding(sf=False, ordinal_infos=ordinal_infos)

        ordinal_infos = {
            'features': [
                {'name': 'X', 'max_level': 3},
                {'name': 'Y', 'max_level': 2},
                {'name': 'Z', 'max_level': 3}, # extra var
            ],
            'max_level': 3,
        }
        with self.assertRaisesRegex(ValueError, err_rx):
            dataset.get_one_hot_encoding(sf=False, ordinal_infos=ordinal_infos)

        ordinal_infos = {
            'features': [
                {'name': 'X', 'max_level': 3},
                # missing var
            ],
            'max_level': 3,
        }
        with self.assertRaisesRegex(ValueError, err_rx):
            dataset.get_one_hot_encoding(sf=False, ordinal_infos=ordinal_infos)

    def test_get_one_hot_encoding_many_warnings(self):

        df = pd.DataFrame({
            'ID':     ['S1', 'S1', 'S1', 'S1', 'S2', 'S2'],
            'TIME':   [ 50.,  51.,  53.,  59., 35.3, 43.9],
            'X':      [ 1,    0,    5,    1,   6,    1   ],
            'Y':      [ 1,    -1,  nan,    4, nan,    -4   ],
        })
        # create the dataset
        dataset = Dataset(Data.from_dataframe(df))

        ordinal_infos = {
            'features': [
                {'name': 'X', 'max_level': 3},
                {'name': 'Y', 'max_level': 2},
            ],
            'max_level': 3,
        }

        # only check combinations of warnings (results were checked before)
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter('always')
            _ = dataset.get_one_hot_encoding(sf=False, ordinal_infos=ordinal_infos)

        ws = [str(w.message) for w in ws]
        self.assertEqual(ws, [
            "Some features have unexpected codes (they were clipped to the maximum known level):"
            "\n- X [[0..3]]: [5, 6] were unexpected"
            "\n- Y [[0..2]]: [-4, -1, 4] were unexpected",

            "Some features have missing codes:"
            "\n- X [[0..3]]: [2, 3] are missing"
            "\n- Y [[0..2]]: [2] are missing" # the day where the missing check discard nans we'll have missing 0 as well
        ])
