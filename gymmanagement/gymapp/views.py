from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from .member import Member
from .trainer import Trainer

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

            Member.register(connection, name, email, password, fitness_goal)
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
            booking_date = request.POST.get('booking_date')
            booking_time = request.POST.get('booking_time')
            # Call the book_room method from your class
            room_number = Member.book_room(
                connection, booking_date, booking_time
            )

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
        'member_name': member_name
    })
