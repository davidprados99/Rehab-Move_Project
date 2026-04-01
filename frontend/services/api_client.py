import requests

class ApiClient:
    def __init__(self):
        self.base_url = "http://rehab-move-api-env-1.eba-epsm62av.us-east-1.elasticbeanstalk.com" #API URL
        self.token = None #Auth token
        self.user_role = None #User role (physio, patient)

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
    
    
    def get_patients(self, skip=0, limit=100):
        """Get the list of patients (for physios)"""
        url = f"{self.base_url}/patients/"
        
        try:
            # Make the GET request with authentication headers and pagination parameters
            response = requests.get(url, headers=self.get_headers(), params={"skip": skip, "limit": limit})
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, response.json().get("detail", "Error al obtener pacientes")
        except Exception as e:
            return False, str(e)