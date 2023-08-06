from leaspy.models.utils.attributes import LinearAttributes, LogisticAttributes

from tests import LeaspyTestCase


class AttributesUnivariateTest(LeaspyTestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the object for all the tests"""
        # for tmp handling
        super().setUpClass()

        cls.to_test = {
            'univariate_logistic': LogisticAttributes,
            'univariate_linear': LinearAttributes
        }

    def test_constructor(self):

        """Test the initialization"""
        for attr_name, klass in self.to_test.items():
            attr = klass(attr_name, dimension=1, source_dimension=None)
            self.assertEqual(attr.positions, None)
            self.assertFalse(hasattr(attr, 'velocities'))
            self.assertEqual(attr.name, attr_name)
            self.assertEqual(attr.update_possibilities, ('all', 'g'))
            #self.assertRaises(TypeError, AttributesUnivariate, 5, 2)  # with arguments for dimension & source_dimension

            """Test if raise a ValueError if asking to update a wrong arg"""
            self.assertRaises(ValueError, attr._check_names, ['blabla1', 3.8, None]) # totally false
            self.assertRaises(ValueError, attr._check_names, ['betas']) # false iff univariate
            self.assertRaises(ValueError, attr._check_names, ['deltas']) # false if univariate
            self.assertRaises(ValueError, attr._check_names, ['xi_mean']) # was USELESS so removed
            self.assertRaises(ValueError, attr._check_names, ['v0']) # only for multivariate
            self.assertRaises(ValueError, attr._check_names, ['v0_collinear']) # only for multivariate

    def test_bad_name(self):
        with self.assertRaises(ValueError):
            LogisticAttributes(name=['should-be-a-str'], dimension=1, source_dimension=None)

    def test_bad_dim(self):
        with self.assertRaisesRegex(ValueError, '`dimension`'):
            LogisticAttributes(name='univariate_logistic', dimension=0, source_dimension=None)
        with self.assertRaisesRegex(ValueError, '`dimension`'):
            LogisticAttributes(name='univariate_logistic', dimension=0.5, source_dimension=None)
        with self.assertRaisesRegex(ValueError, '`dimension`'):
            LogisticAttributes(name='univariate_logistic', dimension=-1, source_dimension=None)

    def test_bad_sources_for_univariate(self):
        with self.assertRaisesRegex(ValueError, 'source'):
            LogisticAttributes(name='univariate_logistic', dimension=1, source_dimension=1)

        # this is tolerated
        LogisticAttributes(name='univariate_logistic', dimension=1, source_dimension=0)
