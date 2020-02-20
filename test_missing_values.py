"""A3. Tester for the function patients_with_missing_values
in treatment_functions.
"""

import unittest
import treatment_functions as tfs

ERROR_MESSAGE = "Expected {}, but returned {}"


class TestPatientsWithMissingValues(unittest.TestCase):
    """Tester for the function patients_with_missing_values in
    treatment_functions.
    """

    def test_empty(self):
        """Empty dictionary."""

        id_to_attributes = {}
        name = 'xyz'
        expected = []
        actual = tfs.patients_with_missing_values(id_to_attributes, name)

        msg = ERROR_MESSAGE.format(expected, actual)
        self.assertEqual(expected, actual, msg)

    def test_one_patient_no_missing(self):
        """One patient, with the value present."""

        id_to_attributes = {
            'Tom':  {'Pet': 'dog', 'Car': 'NA', 'Team': 'Leafs'}
        }
        name = 'Pet'
        expected = []
        actual = tfs.patients_with_missing_values(id_to_attributes, name)

        msg = ERROR_MESSAGE.format(expected, actual)
        self.assertEqual(expected, actual, msg)

    def test_empty_id_to_attributes(self):
        """"Test an empty ID_TO_ATTRIBUTES type."""
        
        id_to_attributes = {}
        
        actual = tfs.patients_with_missing_values(id_to_attributes, 
                                                  tfs.TREATMENT)
        expected = []
        
        self.assertEqual(expected, actual)
        
    def test_lowercase_NA(self):
        """Test an empty value with lowercase NA, 'na'."""
        
        id_to_attributes = {
            'patient_1': 
            {'Treatment': 'na', 'Status': 'Alive'}
        }
        
        actual = tfs.patients_with_missing_values(tfs.THREE_PATIENTS, 
                                                  tfs.TREATMENT)
        expected = []
        
        self.assertEqual(expected, actual)        
    
    def test_no_missing_values_1(self):
        """Test an ID_TO_ATTRIBUTES type with no values that are missing."""
        
        actual = tfs.patients_with_missing_values(tfs.THREE_PATIENTS, 'Gender')
        expected = []
        
        self.assertEqual(expected, actual)
        
    def test_no_missing_values_2(self):
        """Test an ID_TO_ATTRIBUTES type with no values that are missing."""
        
        actual = tfs.patients_with_missing_values(tfs.THREE_PATIENTS,
                                                  'Lymph_Nodes')
        expected = []
        
        self.assertEqual(expected, actual)
        
    def test_different_missing_values_1(self):
        """Test an ID_TO_ATTRIBUTES type with different values that are missing
        between different patients."""        
        
        actual = tfs.patients_with_missing_values(tfs.PATIENTS_WITH_NA, 
                                                  'Histological_Type')
        expected = ['tcga.5l.aat0']
        
        self.assertEqual(expected, actual)
        
    def test_different_missing_values_2(self):
        """Test an ID_TO_ATTRIBUTES type with different values that are missing
        between different patients."""
        
        actual = tfs.patients_with_missing_values(tfs.PATIENTS_WITH_NA,
                                                  tfs.TREATMENT)
        expected = ['tcga.aq.a7u7']
        
        self.assertEqual(expected, actual)
        
    def test_same_missing_values(self):
        """Test an ID_TO_ATTRIBUTES type with the same values that are missing
        among different patients."""
        
        actual = tfs.patients_with_missing_values(tfs.NEW_PATIENTS, 
                                                  tfs.TREATMENT)
        expected = ['tcga.uu.a93s', 'tcga.v7.a7hq', 'tcga.xx.a899']
        
        self.assertEqual(expected, actual)
        
    def test_middle_all_values_missing(self):
        """Test a middle attribute of an ID_TO_ATTRIBUTES type 
        with all of the values missing"""
        
        id_to_attributes = {
            'patient_1': 
            {'Drugs': 'NA', 'Meal_Plan': 'NA', 'Surgery': 'NA'},
            'patient_2':
            {'Drugs': 'NA', 'Meal_Plan': 'NA', 'Surgery': 'NA'}
        }
        
        actual = tfs.patients_with_missing_values(id_to_attributes, 'Meal_Plan')
        expected = ['patient_1', 'patient_2']
        
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main(exit=False)
