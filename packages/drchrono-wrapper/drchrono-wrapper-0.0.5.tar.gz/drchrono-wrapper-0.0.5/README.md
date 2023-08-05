# drchrono-wrapper


## API token with .env file 
- env file structure: 
    ```
    DRCHRONO_API_TOKEN = 
    ```

## endpoints covered: 
- Example fake data generator: `f_users, f_doctors, f_patients, f_appointments = drc.FAKER.generate(20, 40, 150, 500)` 
    - this creates 4 datasets with users/doctors that have linked ID's to patients and appointments 
- *Fake data generation*:
    - Admin: 
        - Users 
        - Doctors 
    - Clinical: 
        - Patients 
        - Appointments 

- *Real data pulls*: 
    - Admin: 
        - Users 
        - Doctors 
    - Clinical: 
        - Patients 
        - Appointments 
        - Medications 

## admin: 
- To create to version: 
    - update setup.py version number 
    - re-run `python setup.py sdist` to create new distribution 
    - upload to pypi with `twine upload dist/*` 