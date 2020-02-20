# medical-treatment-planner
Assignment for CSC108 desgined to read a tsv file, analyze its contents, and make a decision based on contents and pre-existing conditions to recommend cancer treatment.

1. medical_data sheet is first read, and a dictionary is built to store the values of the sheet in the form of ID:Attributes, where ID = patient number and attributes = the characteristics of cancer of the patient
2. new treatment plans are conducted by replacing the treatment attribute: new patient tsv is compared to existing patient tsv to come up with the new treatment methods
