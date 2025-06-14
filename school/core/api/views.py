from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import School 
from account.api.utils import calculate_distance  

from heapq import nsmallest

class ClosestSchoolsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.latitude is None or user.longitude is None:
            return Response({"error": "Your location is not set."}, status=400)

        schools = School.objects.exclude(latitude__isnull=True, longitude__isnull=True)
        if not schools.exists():
            return Response({"error": "No schools with coordinates found."}, status=404)

        # Calculate distance and get top 3
        school_distances = [
            (s, calculate_distance(user.latitude, user.longitude, s.latitude, s.longitude))
            for s in schools
        ]
        closest_schools = nsmallest(3, school_distances, key=lambda x: x[1])

        return Response({
            "closest_schools": [
                {
                    "id": school.id,
                    "name": school.name,
                    "latitude": school.latitude,
                    "longitude": school.longitude,
                    "distance_km": round(distance, 2)
                }
                for school, distance in closest_schools
            ]
        })

