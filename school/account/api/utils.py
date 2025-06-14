from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import math

User = get_user_model()

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # distance in kilometers


def generate_user_response(user):
    token, _ = Token.objects.get_or_create(user=user)
    return {"data":{
        "success": True,
        "token": token.key,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "national_id": user.national_id,
        "is_active": user.is_active,}
    }