"""Assignment 3 - Medical Treatment Planning
"""

from typing import Dict, List, TextIO
from constants import (NA, TREATMENT, PATIENT_ID_INDEX, NAME_TO_VALUE,
                       ID_TO_ATTRIBUTES, VALUE_TO_IDS, ID_TO_SIMILARITY)
from constants import (THREE_PATIENTS, PATIENTS_WITH_NA, NEW_PATIENT_INFO,
                       NEW_PATIENTS, NEW_PATIENTS_RECOMMENDATIONS)

#Student-created Helper Functions
def get_file_lines(file: TextIO) -> list:
    """Return a nested list of cosnisting of the rows of the of the file passed
    through.
    
    Preconditions: file is a TSV file,
                   file is open for reading
                   
    >>> new_file = 'medical_data_three.tsv'
    >>> data_file = open(new_file)
    >>> first_line = data_file.readline()
    >>> get_file_lines(data_file)
    [['tcga.5l.aat0', '42', 'female', 't2', 'n0', 'm0', 'h_t_1', '0', 'plan_1'], ['tcga.aq.a54o', '51', 'male', 't2', 'n0', 'm0', 'h_t_2', '0', 'plan_2'], ['tcga.aq.a7u7', '55', 'female', 't2', 'n2a', 'm0', 'h_t_1', '4', 'plan_4']]
    """
    
    all_data = []
    file_lines = []
    
    for line in file:
        all_data.append(line.split('\n'))
    
    for line in all_data:
        file_lines.append(line[0].split('\t'))
        
    return file_lines


def get_num_to_values(file_lines: list, info_type: list) -> list:
    """Return a list consisting of dictionaries made up of the attributes of 
    all patients.
    """

    values = {}
    to_values_list = []
            
    for patient in file_lines:
        for patient_info in range(1, len(info_type)):
            values[info_type[patient_info]] = patient[patient_info]

        values_updated = values.copy()
        to_values_list.append(values_updated)

    return to_values_list


def sort_similarity(id_with_similarity: list) -> None:
    """Sort a list contaning patient ids in terms of descending order of 
    similarity using a bubble sort.
    
    >>> ids_similarity = [('tcga.5l.aat0', 5.28), ('tcga.aq.a54o', 3.67),\
    ('tcga.aq.a7u7', 4.67)]
    >>> sort_similarity(ids_similarity)
    >>> ids_similarity
    [('tcga.aq.a54o', 3.67), ('tcga.aq.a7u7', 4.67), ('tcga.5l.aat0', 5.28)]
    >>> ids_similarity = [('tcga.5l.aat0', 2.2), ('tcga.aq.a54o', 2.21), ('tcga.aq.a7u7', 3.55)]
    >>> sort_similarity(ids_similarity)
    >>> ids_similarity
    [('tcga.5l.aat0', 2.2), ('tcga.aq.a54o', 2.21), ('tcga.aq.a7u7', 3.55)]
    """
    end = len(id_with_similarity) - 1
    
    while end != 0:
        for id_key in range(end):
            if id_with_similarity[id_key][1] == \
            id_with_similarity[id_key + 1][1]: 
                if id_with_similarity[id_key][0] < \
                id_with_similarity[id_key + 1][0]: id_with_similarity[id_key], \
                id_with_similarity[id_key + 1] = \
                id_with_similarity[id_key + 1], id_with_similarity[id_key]
            
            if id_with_similarity[id_key][1] > id_with_similarity \
            [id_key + 1][1]:
                id_with_similarity[id_key], id_with_similarity[id_key + 1] = \
                id_with_similarity[id_key + 1], id_with_similarity[id_key]

        end -= 1    

    
def read_patients_dataset(patients_file: TextIO) -> ID_TO_ATTRIBUTES:
    """Return an ID_TO_ATTRIBUTES dictionary that contains all
    information from patients_file.

    Preconditions: patients_file is a TSV file,
                   patients_file is open for reading.

    >>> patients_file = open("medical_data_three.tsv")
    >>> id_to_attributes = read_patients_dataset(patients_file)
    >>> patients_file.close()
    >>> id_to_attributes == THREE_PATIENTS
    True
    """
    
    first_line = patients_file.readline()
    info_type = first_line.split()

    total_patient_info = get_file_lines(patients_file)
    total_num_to_values = get_num_to_values(total_patient_info, info_type)

    all_patient_data = {}
    patients_file.seek(0)
    patients_file.readline()
    
    patient_num = 0
    
    for line in patients_file:
        all_patient_data[line[0: line.find('\t')]] = \
        total_num_to_values[patient_num]
        patient_num += 1

    return all_patient_data


def build_value_to_ids(id_to_attributes: ID_TO_ATTRIBUTES,
                       name: str) -> VALUE_TO_IDS:
    """Return a VALUE_TO_IDS dictionary, in which the keys are all
    possible values of an attribute with name name that appear in
    id_to_attributes, and the values are lists of all patient IDs that
    have that value for this attribute name.

    Precondition: name is a name of an attribute that appears in
                  id_to_attributes.

    >>> value_to_ids = build_value_to_ids(THREE_PATIENTS, 'Gender')
    >>> expected = {'male': ['tcga.aq.a54o'],
    ...             'female': ['tcga.5l.aat0', 'tcga.aq.a7u7']}
    >>> same_key_to_list_dicts(expected, value_to_ids)
    True
    """

    values_to_ids = {}

    for id_key in id_to_attributes:
        placeholder = []
        values_to_ids[id_to_attributes[id_key][name]] = placeholder

    for value in values_to_ids:
        for id_key in id_to_attributes:
            if id_to_attributes[id_key][name] == value:
                values_to_ids[value].append(id_key)

    return values_to_ids


def patients_with_missing_values(id_to_attributes: ID_TO_ATTRIBUTES,
                                 name: str) -> List[str]:
    """Return a list consisting of patient ID's who are missing a value (i.e 
    have 'NA' for a value) for the given attribute, indicated by 'name'.
    
    Preconditions: name is a valid attribute in id_to_attributes
    
    >>> patients_with_missing_values(THREE_PATIENTS, TREATMENT)
    []
    >>> patients_with_missing_values(NEW_PATIENTS, 'Lymph_Nodes')
    ['tcga.uu.a93s']
    """

    patients_missing_value = []

    for id_key in id_to_attributes:
        if id_to_attributes[id_key][name] == NA:
            patients_missing_value.append(id_key)

    return patients_missing_value


def similarity_score(name_to_value_1: NAME_TO_VALUE,
                     name_to_value_2: NAME_TO_VALUE) -> float:
    """Return the total similarity score, rounded to 2 places after the
    decimal point, for the two patients with data name_to_value_1 and
    name_to_value_2, respectively. Ignore attribute TREATMENT in the 
    calculation.

    The total similarity score is the sum of the similarity scores for each
    of the patient's attributes. The total similarity score is to be rounded
    to 2 places after the decimal point. Do not round each individual
    attribute similarity score, only round the total.

    Each attribute similarity score is determined as follows:

    For each attribute other than TREATMENT:
      1. If either patient has an attribute value of NA, the similarity
         score for the attribute is 0.5.
      2. If the two attribute values are numeric, the similarity score for
         the attribute is 1 / ( (the absolute difference of the values) + 1 ).
      3. Otherwise, the similarity score for the attribute is 0.0 if the
         two patient attribute values are different or 1.0 if the two
         patient attribute values are the same.

    >>> p1 = THREE_PATIENTS['tcga.5l.aat0']
    >>> p2 = THREE_PATIENTS['tcga.aq.a54o']
    >>> abs(similarity_score(p1, p2) - 4.1) < 0.01
    True
    >>> p1 = PATIENTS_WITH_NA['tcga.5l.aat0']
    >>> p2 = PATIENTS_WITH_NA['tcga.aq.a7u7']
    >>> abs(similarity_score(p1, p2) - 4.07) < 0.01
    True
    """

    total_score = 0.0

    for attribute in name_to_value_1:
        if attribute != TREATMENT:
            if name_to_value_1[attribute] == NA or name_to_value_2[attribute] \
            == NA:
                total_score += 0.5

            elif name_to_value_1[attribute].isdigit() and \
            name_to_value_2[attribute].isdigit():
                value_1 = float(name_to_value_1[attribute])
                value_2 = float(name_to_value_2[attribute])
                total_score += (1.0 / (abs(value_1 - value_2) + 1.0))

            elif name_to_value_1[attribute] == name_to_value_2[attribute]:
                total_score += 1.0

    return round(total_score, 2)

def patient_similarities(id_to_attributes: ID_TO_ATTRIBUTES,
                         name_to_value: NAME_TO_VALUE) -> ID_TO_SIMILARITY:
    """Calculate and return the similarities mapped between the given patients, 
    name_to_value, and patients with data, id_to_attributes in dictionary of 
    the type ID_TO_SIMILARITY.
    
    >>> patient_similarities(THREE_PATIENTS, NEW_PATIENT_INFO)
    {'tcga.5l.aat0': 5.28, 'tcga.aq.a54o': 3.67, 'tcga.aq.a7u7': 4.67}
    >>> patient_similarities(THREE_PATIENTS, NEW_PATIENTS['tcga.uu.a93s'])
    {'tcga.5l.aat0': 1.55, 'tcga.aq.a54o': 1.58, 'tcga.aq.a7u7': 1.61}
    """

    id_to_similarity = {}

    for id_key in id_to_attributes:
        id_to_similarity[id_key] = similarity_score(id_to_attributes[id_key],
                                                    name_to_value)

    return id_to_similarity


def patients_by_similarity(id_to_attributes: ID_TO_ATTRIBUTES,
                           name_to_value: NAME_TO_VALUE) -> List[str]:
    """Return a list of patient ids with a decreasing order of similarities of 
    patients data, id_to_attributes, with the patient data given in, 
    name_to_value.
    
    >>> patients_by_similarity(THREE_PATIENTS, NEW_PATIENT_INFO)
    ['tcga.5l.aat0', 'tcga.aq.a7u7', 'tcga.aq.a54o']
    >>> patients_by_similarity(THREE_PATIENTS, NEW_PATIENTS['tcga.uu.a93s'])
    ['tcga.aq.a7u7', 'tcga.aq.a54o', 'tcga.5l.aat0']
    """

    id_by_similarity = []
    id_with_similarity = list(patient_similarities(id_to_attributes, 
                                                   name_to_value).items())
    
    sort_similarity(id_with_similarity)
    
    for id_key in range(len(id_with_similarity) - 1, -1, -1):
        id_by_similarity.append(id_with_similarity[id_key][0])  

    return id_by_similarity
    

def treatment_recommendations(id_to_attributes: ID_TO_ATTRIBUTES,
                              name_to_value: NAME_TO_VALUE) -> List[str]:
    """Return a list of unique values for TREATMENT according to similarities
    between the patients data, id_to_attributes, and another patients data, 
    name_to_value.
    
    >>> treatment_recommendations(THREE_PATIENTS, NEW_PATIENT_INFO)
    ['plan_1', 'plan_4', 'plan_2']
    >>> treatment_recommendations(THREE_PATIENTS, NEW_PATIENTS['tcga.uu.a93s'])
    ['plan_4', 'plan_2', 'plan_1']
    """

    treatments = []
    id_by_similarity = patients_by_similarity(id_to_attributes, name_to_value)

    for patient in id_by_similarity:
        if id_to_attributes[patient][TREATMENT] != NA and id_to_attributes \
        [patient][TREATMENT] not in treatments:
            treatments.append(id_to_attributes[patient][TREATMENT])

    return treatments


def make_treatment_plans(id_to_attributes: ID_TO_ATTRIBUTES,
                         new_id_to_attributes: ID_TO_ATTRIBUTES) -> None:
    """Modify new_id_to_attributes by replacing the values of the
    TREATMENT attribute with the first recommended treatment for each patient,
    according to the existing patient data in id_to_attributes.

    >>> new_id_to_attributes = NEW_PATIENTS.copy()
    >>> make_treatment_plans(THREE_PATIENTS, new_id_to_attributes)
    >>> new_id_to_attributes == NEW_PATIENTS_RECOMMENDATIONS
    True
    """
    
    patient_similarity_list = []
    
    treatment_counter = 0
    
    for id_key in new_id_to_attributes:
        patient_similarity_list.append(treatment_recommendations
                                       (id_to_attributes, 
                                        new_id_to_attributes[id_key]))
        
        new_id_to_attributes[id_key][TREATMENT] = \
        patient_similarity_list[treatment_counter][0]
        
        treatment_counter += 1
        

# Provided helper functions - can be used to test two objects for `sameness'.

def same_key_to_list_dicts(key_to_list1: Dict[str, List[str]],
                           key_to_list2: Dict[str, List[str]]) -> bool:
    """Return True if and only if key_to_list1 and key_to_list2 are equal
    dictionaries, regardless of the order in which elements occur in the 
    dictionaries' values.

    >>> same_key_to_list_dicts({'a': [], 'b': ['x'], 'c': ['x', 'y', 'z']},
    ...                        {'a': [], 'b': ['x'], 'c': ['y', 'z', 'x']})
    True
    >>> same_key_to_list_dicts({'a': [], 'b': ['x'], 'c': ['x', 'y', 'z']},
    ...                        {'a': [], 'b': ['x'], 'c': ['y', 'z', 'w']})
    False
    >>> same_key_to_list_dicts({'a': [], 'b': ['x'], 'd': ['x', 'y', 'z']},
    ...                        {'a': [], 'b': ['x'], 'c': ['y', 'z', 'x']})
    False
    """

    if key_to_list1.keys() != key_to_list2.keys():
        return False

    for key in key_to_list1:
        if not same_lists(key_to_list1[key], key_to_list2[key]):
            return False

    return True


def same_lists(list1: list, list2: list) -> bool:
    """Return True if and only if list1 and list2 are equal lists, regardless 
    of the order in which elements occur.

    >>> same_lists(['x', 'y', 'z'], ['y', 'z', 'x'])
    True
    >>> same_lists(['x', 'y', 'k'], ['y', 'z', 'x'])
    False
    """

    return sorted(list1) == sorted(list2)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    medical_data_file = 'medical_data.tsv'
    patients_data_file = open(medical_data_file)
    patient_id_to_attributes = read_patients_dataset(patients_data_file)
    patients_data_file.close()

    medical_data_file = 'new_patients.tsv'
    new_patients_data_file = open(medical_data_file)
    new_patient_id_to_attributes = read_patients_dataset(new_patients_data_file)
    new_patients_data_file.close()

    make_treatment_plans(patient_id_to_attributes, 
                         new_patient_id_to_attributes)
    
    for new_patient_id in new_patient_id_to_attributes:
        recommend_str = (
            'The recommended treatment for patient {} is {}.'.format(
                new_patient_id,
                new_patient_id_to_attributes[new_patient_id][TREATMENT]))
        ##Uncomment the line below to view the treatment plans but
        ##re-comment out before submitting solution.
        print(recommend_str)
