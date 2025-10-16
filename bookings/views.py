from django.shortcuts import render
import json
from datetime import datetime
from pathlib import Path
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
# from .storage import load_data, save_data, COFFEE, SOLUBLES, MILK, CROISSANTS, TARTS
from .storage import BOOKINGS_DATA_FILE, MENU_DATA_FILE, load_session_data, load_menu_data, load_booking_data, save_general_data, find_item_by_id


"""
class ResourceList(APIView):
    def get(self, request):
        data = load_data()
        return Response(data["resources"])

    def post(self, request):
        data = load_data()
        new_id = len(data["resources"]) + 1
        resource = {"id": new_id, "name": request.data.get("name")}
        data["resources"].append(resource)
        save_data(data)
        return Response(resource, status=status.HTTP_201_CREATED)
"""
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        return Response({"token": token.key, "user": token.user.username})

class GetSession(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        session = load_session_data()

        return Response(session["currentSession"])

class ItemList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = load_menu_data()

        return Response(items)

class BookingList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        session_date_requested = request.GET.get('session_date')

        if not session_date_requested:
            current_session_data = load_session_data()
            session_date_requested = current_session_data["currentSession"]

        booking_data = load_booking_data()

        session_key = f"bookings-{session_date_requested}"

        requested_bookings = booking_data.get(session_key, [])

        return Response(requested_bookings)

        # if request.user.is_superuser:
        #     return Response(data["bookings"])
        # else:
        #     user_bookings = [b for b in data["bookings"] if b["user"] == request.user.username]
        #     return Response(user_bookings)

    def post(self, request):
        menu_data = load_menu_data()
        booking_data = load_booking_data()
        session_data = load_session_data()
        request_data = request.data.get("items")

        if not booking_data:
            return Response({"error": "Nessun booking inviato"}, status=400)

        current_session = session_data["currentSession"]
        session = request_data.get("session")
        products = request_data.get("products")

        # Validazione item_id
        if current_session != session:
            return Response(
                {"error": "Sessione non valida"},
                status=status.HTTP_400_BAD_REQUEST
            )

        print("products" + str(products))
        # Validazione item_id
        for p in products:
            print(p.get("category"))
            if p.get("category") not in menu_data:
                return Response(
                    {"error": "Categoria prodotto non valida"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            product_category = menu_data[p.get("category")]
            found_id = False

            for item in product_category:
                if item["id"] == p.get("item_id"):
                    found_id = True

            if not found_id:
                return Response(
                    {"error": "ID prodotto non valido"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        booking_key = f"bookings-{current_session}"
        print("booking_key" + booking_key)
        
        if booking_key not in booking_data:
            booking_data[booking_key] = []

        new_id = len(booking_data[booking_key]) + 1
        new_booking = {
            "id": new_id,
            "user": request.user.username,
            "booktime": datetime.today().strftime('%d-%m-%Y, %H:%M'),
            "products": products
        }

        booking_data[booking_key].append(new_booking)

        save_general_data(booking_data, BOOKINGS_DATA_FILE)
        return Response(booking_data, status=status.HTTP_201_CREATED)
    
class BookingDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, booking_id):
        data = load_booking_data()
        booking = next((b for b in data["bookings"] if b["id"] == booking_id), None)
        if not booking:
            return Response({"error": "Prenotazione non trovata"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_superuser or booking["user"] == request.user.username:
            data["bookings"] = [b for b in data["bookings"] if b["id"] != booking_id]
            save_general_data(data, BOOKINGS_DATA_FILE)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Non autorizzato"}, status=status.HTTP_403_FORBIDDEN)


