from app.services.fmcsa_service import FMCSAService
from app.services.load_service import LoadService

def get_fmcsa_service():
    return FMCSAService()

def get_load_service():
    return LoadService()