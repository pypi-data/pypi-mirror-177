import torch

from leaspy.models.utils.attributes.linear_attributes import LinearAttributes

from tests import LeaspyTestCase


class AttributesLinearTest(LeaspyTestCase):

    def test_constructor(self):
        """Test the initialization"""
        attributes = LinearAttributes('linear', 5, 1)
        self.assertEqual(attributes.dimension, 5)
        self.assertEqual(attributes.source_dimension, 1)
        self.assertEqual(attributes.positions, None)
        self.assertEqual(attributes.velocities, None)
        self.assertEqual(attributes.orthonormal_basis, None)
        self.assertEqual(attributes.mixing_matrix, None)
        self.assertEqual(attributes.name, 'linear')
        self.assertEqual(attributes.update_possibilities, ('all', 'g', 'v0', 'v0_collinear', 'betas'))
        self.assertRaises(ValueError, LinearAttributes, 'name', '4', 3.2)  # with bad type arguments
        self.assertRaises(TypeError, LinearAttributes)  # without argument

    def test_check_names(self):
        """Test if raise a ValueError if wrong arg"""
        wrong_arg_exemples = ['blabla1', 3.8, None]
        # for wrong_arg in wrong_arg_exemples:
        #     self.assertRaises(ValueError, attributes._check_names, wrong_arg)
        attributes = LinearAttributes('linear', 4, 2)
        self.assertRaises(ValueError, attributes._check_names, wrong_arg_exemples)

    def check_values_and_get_dimensions(self, values):
        dimension = len(values['g'])
        self.assertEqual(len(values['v0']), dimension)
        self.assertEqual(values['betas'].shape[0], dimension-1)
        source_dimension = values['betas'].shape[1]
        self.assertTrue(0 <= source_dimension <= dimension-1)
        return dimension, source_dimension

    def test_compute_orthonormal_basis(self):
        """Test the orthonormality condition"""
        names = ['all']
        values = {
            'g': torch.tensor([0.]*4),
            'v0': torch.tensor([-3., 1, 0, -1]), # as for logistic (too high v0values [exp'd] implies a precision a bit coarser)
            'betas': torch.tensor([[.1, .2, .3], [-.1, .2, .3], [-.1, .2, -.3]]), # dim=4, nb_source=3
        }

        dimension, source_dimension = self.check_values_and_get_dimensions(values)
        attributes = LinearAttributes('linear', dimension, source_dimension)
        attributes.update(names, values)

        # Test the orthonormality condition
        dgamma_t0 = attributes.velocities
        orthonormal_basis = attributes.orthonormal_basis
        for i in range(dimension-1):
            orthonormal_vector = orthonormal_basis[:, i] # column vector
            # Test normality (canonical inner-product)
            self.assertAlmostEqual(torch.norm(orthonormal_vector).item(), 1, delta=1e-6)
            # Test orthogonality to dgamma_t0 (canonical inner-product)
            self.assertAlmostEqual(torch.dot(orthonormal_vector, dgamma_t0).item(), 0, delta=1e-6)
            # Test orthogonality to other vectors (canonical inner-product)
            for j in range(i+1, dimension-1):
                self.assertAlmostEqual(torch.dot(orthonormal_vector, orthonormal_basis[:, j]).item(), 0, delta=1e-6)

    def test_mixing_matrix_utils(self):
        """Test the orthogonality condition"""
        names = ['all']
        values = {
            'g': torch.tensor([0.]*4),
            'v0': torch.tensor([-3., 1, 0, -1]),
            'betas': torch.tensor([[.1, .2, .3], [-.1, .2, .3], [-.1, .2, -.3]]), # dim=4, nb_source=3
        }

        dimension, source_dimension = self.check_values_and_get_dimensions(values)
        attributes = LinearAttributes('linear', dimension, source_dimension)
        attributes.update(names, values)

        dgamma_t0 = attributes.velocities
        mixing_matrix = attributes.mixing_matrix

        for mixing_column in mixing_matrix.permute(1, 0):
            # Test orthogonality to dgamma_t0 (canonical inner-product)
            self.assertAlmostEqual(torch.dot(mixing_column, dgamma_t0).item(), 0, delta=1e-6)


    def test_orthonormal_basis_consistency(self):

        values = {
            'g': torch.tensor([-1.1, 2.2, 0.0, 3.3], dtype=torch.float32),
            'betas': torch.tensor([[0.1, 0.2, 0.3], [-0.1, 0.2, 0.3], [-0.1, 0.2, -0.3]], dtype=torch.float32),
            'v0': torch.tensor([-4.0, -2.8, -4.5, -3.5], dtype=torch.float32)
        }
        dimension, source_dimension = self.check_values_and_get_dimensions(values)

        attributes = LinearAttributes('linear', dimension, source_dimension)
        attributes.update(['all'], values)

        old_velocities = attributes.velocities
        old_BON = attributes.orthonormal_basis
        old_A = attributes.mixing_matrix

        # check shape of BON & A
        self.assertEqual(old_BON.shape, (dimension, dimension - 1))
        self.assertEqual(old_A.shape, (dimension, source_dimension))

        # shift v0 (log of velocities), so the resulting v0 should be collinear to previous one
        # and so the orthonormal basis should be the same!
        new_v0 = values['v0'] - 0.3
        attributes.update(['v0'], {'v0': new_v0})
        new_velocities = attributes.velocities
        new_BON = attributes.orthonormal_basis
        new_A = attributes.mixing_matrix

        # velocities are different
        self.assertFalse(torch.allclose(old_velocities, new_velocities))
        # but they are collinear
        self.assertTrue(attributes._check_collinearity_vectors(old_velocities, new_velocities))
        # and the orthonormal basis (and mixing matrix) are the same!
        self.assertAllClose(old_BON, new_BON, what='ortho_basis')
        self.assertAllClose(old_A, new_A, what='mixing_matrix')

        # but orthonormal basis & mixing matrix were re-computed!
        self.assertNotEqual(id(old_BON), id(new_BON))
        self.assertNotEqual(id(old_A), id(new_A))


    def test_no_update_of_orthonormal_basis_when_using_v0_collinear_update(self):

        values = {
            'g': torch.tensor([-1.1, 2.2, 0.0, 3.3], dtype=torch.float32),
            'betas': torch.tensor([[0.1, 0.2, 0.3], [-0.1, 0.2, 0.3], [-0.1, 0.2, -0.3]], dtype=torch.float32),
            'v0': torch.tensor([-4.0, -2.8, -4.5, -3.5], dtype=torch.float32)
        }
        dimension, source_dimension = self.check_values_and_get_dimensions(values)

        attributes = LinearAttributes('linear', dimension, source_dimension)
        attributes.update(['all'], values)

        old_velocities = attributes.velocities
        old_BON = attributes.orthonormal_basis
        old_A = attributes.mixing_matrix

        # shift v0 (log of velocities), so the resulting v0 should be collinear to previous one
        # and so the orthonormal basis should be the same!
        new_v0 = values['v0'] - 0.3
        attributes.update(['v0_collinear'], {'v0': new_v0})
        new_velocities = attributes.velocities
        new_BON = attributes.orthonormal_basis
        new_A = attributes.mixing_matrix

        # velocities are different
        self.assertFalse(torch.allclose(old_velocities, new_velocities))
        # but they are collinear
        self.assertTrue(attributes._check_collinearity_vectors(old_velocities, new_velocities))
        # and the orthonormal basis (and mixing matrix) was not re-computed!
        self.assertEqual(id(old_BON), id(new_BON))
        self.assertEqual(id(old_A), id(new_A))

        # consistency when changing betas
        attributes.update(['betas'], {'betas': values['betas']+0.1})
        self.assertEqual(id(old_BON), id(attributes.orthonormal_basis))  # not recomputed BON
        self.assertFalse(torch.allclose(old_A, attributes.mixing_matrix))
