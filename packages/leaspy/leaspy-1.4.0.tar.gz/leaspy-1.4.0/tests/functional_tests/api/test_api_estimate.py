import pandas as pd

from tests import LeaspyTestCase

class LeaspyEstimateTest_Mixin(LeaspyTestCase):

    def check_almost_equal_for_all_ind_tpts(self, a, b, *, tol=1e-5):
        return self.assertDictAlmostEqual(a, b, atol=tol)

    def batch_checks(self, ip, tpts, models, expected_ests, *, ordinal_method="MLE"):
        for model_name in models:
            with self.subTest(model_name=model_name):
                leaspy = self.get_hardcoded_model(model_name)

                estimations = leaspy.estimate(tpts, ip, ordinal_method=ordinal_method)

                self.check_almost_equal_for_all_ind_tpts(estimations, expected_ests, tol=1e-4)


class LeaspyEstimateTest(LeaspyEstimateTest_Mixin):

    def test_estimate_multivariate(self):

        ip = self.get_hardcoded_individual_params('ip_save.json')

        timepoints = {
            'idx1': [78, 81],
            'idx2': [71]
        }

        # first batch of tests same logistic model but with / without diag noise (no impact in estimation!)
        models = ('logistic_scalar_noise', 'logistic_diag_noise_id', 'logistic_diag_noise')
        expected_ests = {
            'idx1': [[0.99641526, 0.34549406, 0.67467   , 0.98959327],
                     [0.9994672 , 0.5080943 , 0.8276345 , 0.99921334]],
            'idx2': [[0.13964376, 0.1367586 , 0.23170303, 0.01551363]]
        }

        self.batch_checks(ip, timepoints, models, expected_ests)

        # TODO logistic parallel?

        # TODO linear model?

    def test_estimate_ordinal(self):

        ip = self.get_hardcoded_individual_params('ip_save.json')

        timepoints = {
            'idx1': [71, 81],
            'idx2': [71]
        }

        # loss is not involved in estimation so all expected outputs are the same for those 2 models
        model = ('logistic_ordinal', 'logistic_ordinal_ranking_same',)

        # MLE
        expected_ests = {
            'idx1': [[2,0,1,4],   # before saturation
                     [3,4,6,10]], # saturation
            'idx2': [[0,0,0,0]]
        }
        self.batch_checks(ip, timepoints, model, expected_ests, ordinal_method='MLE')

        # Expectation (E)
        expected_ests = {
            'idx1': [[ 1.7107,  0.7169,  1.8397,  3.9503],
                     [ 3.    ,  3.9864,  5.9822, 10.    ]],
            'idx2': [[1.8477e-05, 1.3745e-01, 4.5545e-01, 1.7405e-05]]
        }
        self.batch_checks(ip, timepoints, model, expected_ests, ordinal_method='expectation')

        # Probabilities (P)
        expected_ests = {
            'idx1': {
                ('Y0', 0):  [0.    , 0.    ],
                ('Y0', 1):  [0.2893, 0.    ],
                ('Y0', 2):  [0.7107, 0.    ],
                ('Y0', 3):  [0.    , 1.    ],

                ('Y1', 0):  [0.6068, 0.0008],
                ('Y1', 1):  [0.2569, 0.0024],
                ('Y1', 2):  [0.0427, 0.0017],
                ('Y1', 3):  [0.    , 0.    ], # too rare
                ('Y1', 4):  [0.0937, 0.9952],

                ('Y2', 0):  [0.2375, 0.0003],
                ('Y2', 1):  [0.4202, 0.0014],
                ('Y2', 2):  [0.1227, 0.0014],
                ('Y2', 3):  [0.0478, 0.0011],
                ('Y2', 4):  [0.    , 0.    ], # too rare
                ('Y2', 5):  [0.    , 0.    ], # too rare
                ('Y2', 6):  [0.1718, 0.9958],

                ('Y3', 0):  [0.    , 0.    ],
                ('Y3', 1):  [0.    , 0.    ],
                ('Y3', 2):  [0.0305, 0.    ],
                ('Y3', 3):  [0.    , 0.    ],
                ('Y3', 4):  [0.9638, 0.    ],
                ('Y3', 5):  [0.    , 0.    ],
                ('Y3', 6):  [0.0057, 0.    ],
                ('Y3', 7):  [0.    , 0.    ],
                ('Y3', 8):  [0.    , 0.    ],
                ('Y3', 9):  [0.    , 0.    ],
                ('Y3', 10): [0.    , 1.    ],
            },
            'idx2': {
                ('Y0', 0):  [1.],
                ('Y0', 1):  [0.],
                ('Y0', 2):  [0.],
                ('Y0', 3):  [0.],

                ('Y1', 0):  [0.9143],
                ('Y1', 1):  [0.0634],
                ('Y1', 2):  [0.0076],
                ('Y1', 3):  [0.    ], # too rare
                ('Y1', 4):  [0.0147],

                ('Y2', 0):  [0.7146],
                ('Y2', 1):  [0.2246],
                ('Y2', 2):  [0.0270],
                ('Y2', 3):  [0.0087],
                ('Y2', 4):  [0.],
                ('Y2', 5):  [0.],
                ('Y2', 6):  [0.0252],

                ('Y3', 0):  [1.],
                ('Y3', 1):  [0.],
                ('Y3', 2):  [0.],
                ('Y3', 3):  [0.],
                ('Y3', 4):  [0.],
                ('Y3', 5):  [0.],
                ('Y3', 6):  [0.],
                ('Y3', 7):  [0.],
                ('Y3', 8):  [0.],
                ('Y3', 9):  [0.],
                ('Y3', 10): [0.],
            },
        }
        self.batch_checks(ip, timepoints, model, expected_ests, ordinal_method='probabilities')

    def test_estimate_ordinal_dataframe(self):

        lsp = self.get_hardcoded_model('logistic_ordinal_ranking')
        ip = self.get_hardcoded_individual_params('ip_save.json')

        timepoints = pd.MultiIndex.from_frame(pd.DataFrame({
            'ID':   ['idx1', 'idx2', 'idx1'],
            'TIME': [71,      71,     81],
        }))

        # no precise check of values (part of previous check): just a check of shape & index here
        df_ests = lsp.estimate(timepoints, ip, ordinal_method='MLE')
        self.assertIsInstance(df_ests, pd.DataFrame)
        self.assertTrue(df_ests.index.equals(timepoints))
        self.assertEqual(df_ests.columns.tolist(), lsp.model.features)
        self.assertTrue(((0 <= df_ests) & (df_ests <= lsp.model.ordinal_infos['max_level'])).all(axis=None))

        df_ests = lsp.estimate(timepoints, ip, ordinal_method='E')
        self.assertIsInstance(df_ests, pd.DataFrame)
        self.assertTrue(df_ests.index.equals(timepoints))
        self.assertEqual(df_ests.columns.tolist(), lsp.model.features)
        self.assertTrue(((0 <= df_ests) & (df_ests <= lsp.model.ordinal_infos['max_level'])).all(axis=None))

        df_ests = lsp.estimate(timepoints, ip, ordinal_method='P')
        self.assertIsInstance(df_ests, pd.DataFrame)
        self.assertTrue(df_ests.index.equals(timepoints))
        self.assertEqual(df_ests.columns.nlevels, 2)  # 2D columns
        expected_cols = [(d_ft['name'], lvl) for d_ft in lsp.model.ordinal_infos['features']
                         for lvl in range(0, d_ft['max_level'] + 1)]
        self.assertEqual(df_ests.columns.tolist(), expected_cols)
        self.assertTrue(((0 <= df_ests) & (df_ests <= 1)).all(axis=None))

    def test_estimate_univariate(self):

        ip = self.get_hardcoded_individual_params('ip_univariate_save.json')

        timepoints = {
            'idx1': [78, 81],
            'idx2': [71]
        }

        # first batch of tests same logistic model but with / without diag noise (no impact in estimation!)
        models = ('univariate_logistic',)
        expected_ests = {
            'idx1': [
                [0.999607],
                [0.9999857]
            ],
            'idx2': [[0.03098414]]
        }

        self.batch_checks(ip, timepoints, models, expected_ests)
