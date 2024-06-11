from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pathlib import Path
from django.shortcuts import redirect
import firebase_admin
from firebase_admin import credentials, db
import os
import time
from datetime import datetime
current_datetime = datetime.now()
from twilio.rest import Client
account_sid = ''
auth_token = ''
BASE_DIR = Path(__file__).resolve().parent.parent
firebase_path=os.path.join(BASE_DIR,"")
cred = credentials.Certificate(firebase_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': ''
})
firebase_admin.initialize_app(cred,name="demo")
def parking_blueprint(request):
    # Fetching data from Firebase
        firebase_ref = db.reference('/demo')
        parking_slots = firebase_ref.get()

        # Prepare context to pass to the template
        context = {'parking_slots': parking_slots}
        

        # Render the template with the fetched data
        return render(request, 'demo/html/blueprint.html', context)

def book_slot(request,floor,slot):
   
    firebase_ref = db.reference(f'/demo/{floor}/{slot}/status')
    slot_status = firebase_ref.get()

    if slot_status == 1:
        return redirect('/?message=Slot%20not%20available') 

    firebase_ref.set(1)
    return redirect('/?message=Slot%20booked%20successfully')
    
def register(request):
    # Handle form submission and user registration
    # For demonstration purposes, let's assume we save user data in Firebase
    firebase_ref = db.reference('/users')
    user_data = {
        'name': request.GET.get('name'),
        'phone': request.GET.get('phone'),
        'floor':request.GET.get('floor'),
        'slot':request.GET.get('slot'),
        'start_date':str(current_datetime)
    }
    firebase_ref.push(user_data)
    client = Client(account_sid, auth_token)
    twilio_phone_number = ''
    recipient_phone_number = user_data['phone']
    message = client.messages.create(
    body=f"Hello {user_data['name']} you have been allotted parking in {user_data['floor']} floor and {user_data['slot']} slot and OTP For verification is {563214} Thank You and link to access slot camera is www.camfloor.com" ,
    from_=twilio_phone_number,
    to=recipient_phone_number
    )
    
    
    # Redirect to main screen with success message
    return redirect('/?message=Registration%20successful')
def firebase_listener(request):
    firebase_ref = db.reference('/parking_slots')
    
    # Function to handle changes in database
    def handle_snapshot(snapshot):
        # Get updated data
        parking_slots = snapshot.val()
        
        # Prepare context to pass to the template
        context = {'parking_slots': parking_slots}
        
        # Render the template with the updated data
        html_content = render(request, 'demo/html/blueprint.html', context).content
        
        # Send HTML content as HTTP response
        return HttpResponse(html_content)

    # Add the listener
    firebase_ref.listen(handle_snapshot)



