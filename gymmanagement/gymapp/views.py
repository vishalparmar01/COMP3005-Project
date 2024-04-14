from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connection
from .models import Discussion, MealPlan, Image
from .member import Member
from .trainer import Trainer
from .staff import AdministrativeStaff
from django.contrib import messages

def register_member(request):
    members = None
    column_names = None
    health_metrics = None
    class_schedule = None
    member_name = None

    if request.method == 'POST':
        if 'register' in request.POST:  # Check if the request came from the "Register" button
            # Process form data here
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            fitness_goal = request.POST.get('fitness_goal')
            height = request.POST.get('height')
            weight = request.POST.get('weight')

            Member.register(connection, name, email, password, fitness_goal, weight, height)
            member_name = name  # Set the member_name to the newly registered member

        elif 'update' in request.POST:  # Check if the request came from the "Update" button
            member_name = request.POST.get('member_name')
            field = request.POST.get('field')
            value = request.POST.get('value')

            Member.update_member(connection, member_name, field, value)

    # Always get the dashboard data for the member
        elif 'display_dashboard' in request.POST:
            member_name = request.POST.get('display_dashboard')
            if member_name:  # Check if a name was entered
                health_metrics, class_schedule = Member.display_dashboard(connection, member_name)
        
        elif 'register_for_class' in request.POST:
            member_name = request.POST.get('member_name')
            class_name = request.POST.get('class_name')   
            # Call the register_for_class method from your Member class
            Member.register_for_class(connection, member_name, class_name)
                

        elif 'schedule_training' in request.POST:
            member_name = request.POST.get('member_name_session')
            trainer_name = request.POST.get('trainer_name')
            session_date = request.POST.get('session_date')
            session_time = request.POST.get('session_time')
            # Call the schedule_training_session method from your Member class
            Member.schedule_training_session(
                connection, member_name, trainer_name, session_date, session_time
            )
        
        elif 'book_room' in request.POST:
            name = request.POST.get('members_name')
            booking_date = request.POST.get('booking_date')
            booking_time = request.POST.get('booking_time')
            # Call the book_room method from your class
            room_number = Member.book_room(
                connection, name, booking_date, booking_time
            )
    trainer_schedules = Trainer.get_trainers_schedule(connection)
    print(trainer_schedules)  # Print schedules for testing

    if member_name:
        print(member_name)

        health_metrics, class_schedule = Member.display_dashboard(connection, member_name)
        print(health_metrics)
        print(class_schedule)

    # Move the database query outside of the 'if' block
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()
        column_names = [col[0] for col in cursor.description]

    # Ensure that 'members', 'column_names', 'health_metrics', and 'class_schedule' are always passed to the template
    return render(request, 'gymapp/register_member.html', {
        'members': members,
        'column_names': column_names,
        'health_metrics': health_metrics,
        'class_schedule': class_schedule,
        'member_name': member_name,
        'trainer_schedules': trainer_schedules 
    })

def register_trainer(request):
    member_profile = None

    if request.method == 'POST':
        if 'register' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            if name and email and password:  # Check if the fields are not empty
                Trainer.register(connection, name, email, password)

        if 'search_member' in request.POST:
            member_name = request.POST.get('search_member')
            if member_name:  # Check if a name was entered
                member_data = Trainer.search_member_profile_by_name(connection, member_name)
                if member_data:
                    member_profile = {
                        'id': member_data[0],
                        'name': member_data[1],
                        'email': member_data[2],
                        'fitness_goal': member_data[4],
                    }
        
        if 'manage_schedule' in request.POST:
            trainer_name = request.POST.get('trainer_name')
            available_time = request.POST.get('available_time')
            if trainer_name and available_time:  # Check if the fields are not empty
                Trainer.manage_schedule(connection, trainer_name, [available_time])

    return render(request, 'gymapp/register_trainer.html', {
        'member_profile': member_profile  # Pass the member profile to the template
    })

def register_staff(request):
    room_number = None

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if name and email and password:  # Check if the fields are not empty
            AdministrativeStaff.register(connection, name, email, password)

        if 'manage_room_booking' in request.POST:
            member_id = request.POST.get('member_id')
            booking_date = request.POST.get('booking_date')
            booking_time = request.POST.get('booking_time')
            if booking_date and booking_time:  # Check if the fields are not empty
                room_number = AdministrativeStaff.manage_room_booking(connection, member_id, booking_date, booking_time)

        if 'manage_equipment_maintenance' in request.POST:
            staff_name = request.POST.get('staff_name')
            equipment_name = request.POST.get('equipment_name')
            last_maintenance_date = request.POST.get('last_maintenance_date')
            frequency = request.POST.get('frequency')
            if equipment_name and last_maintenance_date:  # Check if the fields are not empty
                AdministrativeStaff.monitor_equipment_maintenance(connection, staff_name, equipment_name, last_maintenance_date, frequency)
        
        if 'update_class_schedule' in request.POST:
            class_name = request.POST.get('class_name')
            description = request.POST.get('description')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            recurrence = request.POST.get('recurrence')
            if class_name and description and start_time and end_time and recurrence:  # Check if the fields are not empty
                AdministrativeStaff.update_class_schedule(connection, class_name, description, start_time, end_time, recurrence)

        if 'process_payment' in request.POST:
            member_name = request.POST.get('member_name')
            amount = request.POST.get('amount')
            payment_date = request.POST.get('payment_date')
            if member_name and amount and payment_date:  # Check if the fields are not empty
                AdministrativeStaff.process_payment(connection, member_name, amount, payment_date)

    return render(request, 'gymapp/register_staff.html', {
        'room_number': room_number  # Pass the room number to the template
    })

def homepage(request):
    return render(request, 'gymapp/homepage.html')



def community_page(request):
    if request.method == 'POST':
        name = request.POST['p_name']
        image_file = request.FILES['image_file']
        caption = request.POST['caption']

        image = Image(image_file=image_file, caption=caption, name=name)
        image.save()

        return redirect('community_page')

    images = Image.objects.all()

    return render(request, 'gymapp/community_page.html', {'images': images})

