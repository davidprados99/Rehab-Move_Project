import requests

class ApiClient:
    def __init__(self):
        self.base_url = "http://rehab-move-api-env-1.eba-epsm62av.us-east-1.elasticbeanstalk.com" #API URL
        self.token = None #Auth token
        self.user_role = None #User role (physio, patient)
        self.user_id = None #User ID (for fetching related data)
        self.name = None #User name (for display purposes)

    def login(self, email, password):
        """
        Send credentials if the login is succesful
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
                return False, response.json().get("detail", "Error desconocido")
                
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"


    def get_headers(self):
        """Return the headers needed for protected requests."""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}
    
    
    def get_patients(self, skip=0, limit=100, id_physio=None):
        """Get the list of patients (for physios)"""
        url = f"{self.base_url}/physios/{id_physio}/patients/"
        
        try:
            # Make the GET request with authentication headers and pagination parameters
            response = requests.get(url, headers=self.get_headers(), params={"skip": skip, "limit": limit})
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, response.json().get("detail", "Error al obtener pacientes")
        except Exception as e:
            return False, str(e)
    
    def add_patient(self, patient_data):
        """Add a new patient (for physios)"""
        url = f"{self.base_url}/patients/"
        
        try:
            response = requests.post(url, headers=self.get_headers(), json=patient_data)
            
            if response.status_code == 201:
                return True, response.json()
            else:
                return False, response.json().get("detail", "Error al agregar paciente")
        except Exception as e:
            return False, str(e)
    
    def delete_patient(self, id_patient):
        """Delete a patient (for physios)"""
        url = f"{self.base_url}/patients/{id_patient}"
        
        try:
            response = requests.delete(url, headers=self.get_headers())
            
            if response.status_code == 204:
                return True, "Paciente eliminado correctamente"
            else:
                return False, response.json().get("detail", "Error al eliminar paciente")
        except Exception as e:
            return False, str(e)
        
    def get_appointments(self, id=None):
        role_path = self.user_role
        url = f"{self.base_url}/appointments/{role_path}/{id}"

        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, response.json().get("detail", "Error al obtener citas")
        except Exception as e:
            return False, str(e)
    
    def logout(self):
        """Clear the authentication data to log out the user."""
        self.token = None
        self.user_role = None
        self.user_id = None
        self.name = None
    
