import requests

class ApiClient:
    def __init__(self):

        self.base_url = "http://rehab-move-api-env-1.eba-epsm62av.us-east-1.elasticbeanstalk.com" #API URL
        self.token = None #Auth token
        self.user_role = None #User role (physio, patient)
        self.user_id = None #User ID (for fetching related data)
        self.name = None #User name (for display purposes)

    def _make_request(self, method, endpoint, json=None, params=None):
        """Method to make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        
        try:
            response = requests.request(method, url, headers=headers, json=json, params=params)
            
            # 204 No Content (for Deletes)
            if response.status_code == 204:
                return True, None
            
            # Successful responses
            if 200 <= response.status_code < 300:
                return True, response.json()
            
            # Error responses
            error_detail = response.json().get("detail", "Unknown error")
            return False, error_detail

        except Exception as e:
            return False, f"Connection error: {str(e)}"
        
        
    #--- Authentication and User Management ---


    def login(self, email, password):
        """
        Send credentials if the login is successful
        """
        url = f"{self.base_url}/login"
        payload = {
            "email": email,
            "password": password
        }
        
        try:
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.user_role = data.get("role")
                self.user_id = data.get("user_id")
                self.name = data.get("name")
                return True, data
            else:
                return False, response.json().get("detail", "Unknown error")
                
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"


    # --- Patient Management (for Physios) ---


    def add_patient(self, patient_data):
        """Add a new patient (for physios)"""
        return self._make_request("POST", "/patients/", json=patient_data)


    def get_patients_by_physio(self, skip=0, limit=100, id_physio=None):
        """Get the list of patients (for physios)"""
        return self._make_request("GET", f"/physios/{id_physio}/patients", params={"skip": skip, "limit": limit})


    def update_patient(self, id_patient, patient_data):
        """Update patient information (for physios)"""
        return self._make_request("PATCH", f"/patients/{id_patient}", json=patient_data)


    def delete_patient(self, id_patient):
        """Delete a patient (for physios)"""
        return self._make_request("DELETE", f"/patients/{id_patient}")


    #--- Appointments management ---


    def create_appointment(self, appointment_data):
        """Create a new appointment (for physios)"""
        return self._make_request("POST", "/appointments/", json=appointment_data)


    def get_appointments(self, id=None):
        """Get appointments for the current user (physio or patient)"""
        if self.user_role == "physio":
            return self._make_request("GET", f"/appointments/physio/{self.user_id}")
        else:
            return self._make_request("GET", f"/appointments/patient/{self.user_id}")


    def update_appointment(self, id_appointment, appointment_data):
        """Update an existing appointment (for physios)"""
        return self._make_request("PATCH", f"/appointments/{id_appointment}", json=appointment_data)


    def delete_appointment(self, id_appointment):
        """Delete an appointment (for physios)"""
        return self._make_request("DELETE", f"/appointments/{id_appointment}")


    #--- Pain Records management ---


    def create_pain_record(self, pain_data):
        """Create a new pain record (for patients)"""
        return self._make_request("POST", "/pain-records/", json=pain_data)


    def get_pain_records(self, id_patient):
        """Get pain records for a patient (for physios and patients)"""
        return self._make_request("GET", f"/pain-records/patient/{id_patient}")


    def get_pain_records_id(self, id_pain_record):
        """Get a specific pain record by ID (for physios and patients)"""
        return self._make_request("GET", f"/pain-records/{id_pain_record}")


    def update_pain_record(self, id_pain_record, pain_data):
        """Update an existing pain record (for patients)"""
        return self._make_request("PATCH", f"/pain-records/{id_pain_record}", json=pain_data)  


    def delete_pain_record(self, id_pain_record):
        """Delete a pain record (for patients)"""
        return self._make_request("DELETE", f"/pain-records/{id_pain_record}")


    # --- Exercises management ---


    def create_exercise(self, exercise_data):
        """Create a new exercise (for physios)"""
        return self._make_request("POST", "/exercises/", json=exercise_data)


    def get_exercises(self):
        """Get the list of exercises (for physios and patients)"""
        return self._make_request("GET", "/exercises/")


    def get_exercise_id(self, id_exercise):
        """Get a specific exercise by ID (for physios and patients)"""
        return self._make_request("GET", f"/exercises/{id_exercise}")


    def update_exercise(self, id_exercise, exercise_data):
        """Update an existing exercise (for physios)"""
        return self._make_request("PATCH", f"/exercises/{id_exercise}", json=exercise_data)


    def activate_exercise(self, id_exercise):
        """Activate an exercise (for physios)"""
        return self._make_request("POST", f"/exercises/{id_exercise}/activate")


    def inactivate_exercise(self, id_exercise):
        """Inactivate an exercise (for physios)"""
        return self._make_request("POST", f"/exercises/{id_exercise}/inactivate")


    def delete_exercise(self, id_exercise):
        """Delete an exercise (for physios)"""
        return self._make_request("DELETE", f"/exercises/{id_exercise}")


    # --- Exercise Plan management ---


    def create_exercise_assignment(self, assignment_data):
        """Create a new exercise assignment (for physios)"""
        return self._make_request("POST", "/assignments/", json=assignment_data)


    def get_exercise_assignments(self, id_patient):
        """Get exercise assignments for a patient (for physios and patients)"""
        return self._make_request("GET", f"/assignments/patient/{id_patient}")


    def update_exercise_assignment(self, id_assignment, assignment_data):
        """Update an existing exercise assignment (for physios)"""
        return self._make_request("PATCH", f"/assignments/{id_assignment}", json=assignment_data)


    def delete_exercise_assignment(self, id_assignment):
        """Delete an exercise assignment (for physios)"""
        return self._make_request("DELETE", f"/assignments/{id_assignment}")


    # --- Exercise Done management ---


    def create_exercise_done(self, id_assignment):
        """Create an exercise done record for an assignment (for patients)"""
        return self._make_request("POST", "/exercises_done", json={"assignment_id": id_assignment})


    def get_exercises_done(self, id_assignment):
        """Get exercises marked as done for a specific assignment (for patients)"""
        return self._make_request("GET", f"/exercises_done/assignment/{id_assignment}")


    def update_exercise_done(self, id_exercise_done, done_data):
        """Update an exercise done record (for patients)"""
        return self._make_request("PATCH", f"/exercises_done/{id_exercise_done}", json=done_data)


    def delete_exercise_done(self, id_exercise_done):
        """Delete an exercise done record (for patients)"""
        return self._make_request("DELETE", f"/exercises_done/{id_exercise_done}")


    #--- Logout ---


    def logout(self):
        """Clear the authentication data to log out the user."""
        self.token = None
        self.user_role = None
        self.user_id = None
        self.name = None
    
