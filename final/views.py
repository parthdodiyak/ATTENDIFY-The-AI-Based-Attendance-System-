#from django.shortcuts import render
#from django.contrib import messages
#from django.shortcuts import render, redirect
#from django.core.files.storage import FileSystemStorage
import face_recognition
#from .models import Student
import cv2
import numpy as np
from datetime import datetime
from django.core.exceptions import MultipleObjectsReturned
from datetime import date
from django.utils import timezone 
#from datetime import timedelta
#from django.contrib.auth import authenticate,login
#from .models import Student
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from .models import Student
from .models import Faculty
from django.core.files.storage import FileSystemStorage 
import face_recognition
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import AttendanceRecord
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib.styles import getSampleStyleSheet





User = get_user_model()









# Create your views here.
def index(request):
	return render(request,'index.html')

def student(request):
	return render(request,'student.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Construct the email body with name, email, and message
        email_body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        
        # Send email
        send_mail(
            f'New Contact Message from {name}',
            email_body,
            email,  # Use the email provided by the user as the sender
            ['parthd5556@gmail.com'],  # Replace with your own email
            fail_silently=False,
        )

        # Redirect after successful submission
        return HttpResponseRedirect(reverse('contact'))

    return render(request, 'contact.html')


def register_user(request):
    if request.method == 'POST':
        enrollmentNumber = request.POST['enrollmentNumber']
        department=request.POST['department']
        user_name = request.POST['user_name']
        email = request.POST['email']
        raw_password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        image_file = request.FILES.get('avatar')

        # Check if passwords match
        if raw_password != confirmPassword:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        hashed_password = make_password(raw_password)

        # Check if enrollment number already exists
        if Student.objects.filter(enrollmentNumber=enrollmentNumber).exists():
            messages.error(request, "Enrollment number already exists.")
            return redirect('register')

        # Save the uploaded image and process it if provided
        if image_file:
            fs = FileSystemStorage()
            filename = fs.save(image_file.name, image_file)
            image_path = fs.path(filename)

            # Read the face encoding from the uploaded image
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)

            if not face_encodings:
                messages.error(request, "No face detected in the uploaded image.")
                fs.delete(filename)
                return redirect('register')

            face_encoding = face_encodings[0].tolist()
            fs.delete(filename)
        else:
            face_encoding = None

        # Create a new student with the provided data
        student = Student.objects.create(
            enrollmentNumber=enrollmentNumber,
            department=department,
            user_name=user_name,
            email=email,
            password=hashed_password,  # Keep password as plain text
            face_encoding=face_encoding
        )
        student.save()

        return redirect('register')

    return render(request, 'student.html')

def signin(request):
    if request.method == 'POST':
        enrollmentNumber = request.POST.get('enrollmentNumber')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(enrollmentNumber=enrollmentNumber)
        except Student.DoesNotExist:
            messages.error(request, "Invalid enrollment number.")
            return redirect('signin')

        if not check_password(password, student.password):
            messages.error(request, "Invalid password.")   
            return redirect('signin')

        # Authentication successful
        request.session['student_id'] = student.id
        return redirect('attendance')  # Redirect to the dashboard upon successful signin

    return render(request, 'signin.html')


def attendance(request):
    student_id = request.session.get('student_id')
    if student_id:
        student = Student.objects.get(pk=student_id)
        # Retrieve attendance records based on the enrollment number
        attendance_records = AttendanceRecord.objects.filter(student=student)
        return render(request, 'attendance.html', {'attendance_records': attendance_records})
    else:
        return redirect('signin')


def change_pass(request):
    return render(request,'change_pass.html')

def forgot_pass(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            student = Student.objects.get(email=email)  # Use the Student model
        except Student.DoesNotExist:
            messages.error(request, 'Email not found')
            return redirect('forgot_pass')

        # Generate a token for the user
        uid = urlsafe_base64_encode(force_bytes(student.pk))
        token = default_token_generator.make_token(student)

        # Construct the reset link
        reset_link = request.build_absolute_uri(
            f'/reset_password/{uid}/{token}/'
        )

        # Send the reset link to the user's email
        send_reset_link_email(email, reset_link)

        # Redirect the user to a page indicating that the reset link has been sent
        return render(request, 'reset_link_sent.html', {'reset_link': reset_link})

    return render(request, 'forgot_pass.html')

def send_reset_link_email(email, reset_link):
    subject = 'Password Reset'
    message = f'Click this link to reset your password: {reset_link}'
    sender_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, sender_email, recipient_list)


def change_pass(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
    except (TypeError, ValueError, OverflowError):
        uid = None

    try:
        student = Student.objects.get(pk=uid)
    except Student.DoesNotExist:
        student = None

    if student is not None and default_token_generator.check_token(student, token):
        if request.method == "POST":
            # Retrieve password from POST data
            password = request.POST.get('password')
            confirm_password = request.POST.get('reconfirm_password')

            # Validate password and confirm_password
            if password and confirm_password and password == confirm_password:
                # Update student's password
                student.set_password(password)
                student.save()  # Save the updated student object
                messages.success(request, 'Password has been reset successfully.')
                return redirect('signin')  # Redirect to login page after successful password change
            else:
                # Passwords do not match or are empty
                messages.error(request, 'Passwords do not match.')
        
        # Render the change password page
        return render(request, 'change_pass.html')
    else:
        return render(request, 'invalid_reset_link.html')

def secreate(request):
    return render(request,'secreate.html')

def faculty(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        email = request.POST['email']
        raw_password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        department = request.POST['department']

        # Check if passwords match
        if raw_password != confirmPassword:
            messages.error(request, "Passwords do not match.")
            return redirect('faculty_registration')

        # Hash the password before saving
        hashed_password = make_password(raw_password)

        # Check if email already exists
        if Faculty.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('faculty_registration')

        # Create faculty instance and save
        faculty = Faculty.objects.create(
            user_name=user_name,
            email=email,
            password=hashed_password,
            department=department,
        )
        faculty.save()

        return redirect('faculty_registration')

    return render(request, 'faculty.html')



def faculty_sign(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Retrieve faculty record based on the provided email
            faculty = Faculty.objects.get(email=email)
        except Faculty.DoesNotExist:
            # If faculty record does not exist, display error message and redirect to sign-in page
            messages.error(request, "Invalid email.")
            return redirect('faculty_sign')

        # Check if the provided password matches the stored password for the faculty
        if not faculty.check_password(password):
            # If password does not match, display error message and redirect to sign-in page
            messages.error(request, "Invalid password.")
            return redirect('faculty_sign')
        
        request.session['faculty_department'] = faculty.department
        request.session['faculty_username'] = faculty.user_name
        # If password matches, log the user in and redirect based on the faculty's department
        if faculty.department.lower() == 'mechanical':
            return redirect('mechanical')
        elif faculty.department.lower() == 'it':
            return redirect('it')
        elif faculty.department.lower() == 'civil':
            return redirect('civil')
        elif faculty.department.lower() == 'electrical':
            return redirect('electrical')
        # Add more departments as needed
        else:
            # If the department is unrecognized, redirect to a default page
            messages.error(request, "Unrecognized department.")
            return redirect('faculty_sign')
    else:
        # If the request method is not POST, render the sign-in page
        return render(request, 'faculty_sign.html')

def electrical(request):
    return render(request, 'electrical.html')

def it(request):
    return render(request,'it.html')


def civil(request):
    return render(request, 'civil.html')


def mechanical(request):
    return render(request, 'mechanical.html')

def view_attendance(request):
    # Check if faculty username is stored in the session
    if 'faculty_username' in request.session:
        faculty_username = request.session['faculty_username']
        
        # Retrieve attendance records for the faculty member
        attendance_records = AttendanceRecord.objects.filter(faculty_name=faculty_username)
        
        return render(request, 'view_attendance.html', {'attendance_records': attendance_records})
    else:
        # Handle the case where faculty username is not stored in the session
        # You may want to redirect to a login page or display an error message
        return HttpResponse("Faculty username not found in session.")


def take_attendance(request):
    # Initialize variables
    known_face_encodings = []
    known_face_names = []
    known_enrollment_numbers = []

    # Get all students from the database
    students = Student.objects.all()

    faculty_department = request.session.get('faculty_department', None)
    faculty_username = request.session.get('faculty_username')

    # Populate known face encodings, names, and enrollment numbers
    for student in students:
        try:
            face_encoding = np.array(eval(student.face_encoding), dtype=np.float64)
            known_face_encodings.append(face_encoding)
            known_face_names.append(student.user_name)
            known_enrollment_numbers.append(student.enrollmentNumber)
        except (ValueError, TypeError, SyntaxError):
            print(f"Failed to convert face encoding for student: {student.user_name}")

    # Initialize variables for form data
    semester = ''
    time_slot = ''
    lecture_name = ''

    # Check if the form is submitted
    if request.method == 'POST':
        # Get form data
        semester = request.POST.get('semester', '')
        faculty_name = request.POST.get('faculty_name', '')
        time_slot = request.POST.get('time_slot', '')
        lecture_name = request.POST.get('lecture_name', '')

        request.session['selected_time_slot'] = time_slot

    # Initialize attendance tracking dictionary
    attendance_tracker = defaultdict(set)

    # Open the webcam
    video_capture = cv2.VideoCapture(0)

    while True:
        # Read a frame from the webcam
        ret, frame = video_capture.read()

        # Find face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Initialize matches variable
        face_names = []

        for face_encoding in face_encodings:
            # Compare the current face encoding with known face encodings
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"
            enrollment_number = ""

            # Check if any match is found
            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]
                enrollment_number = known_enrollment_numbers[match_index]

                # Check if attendance is already recorded for the student in this time slot
                if (name, time_slot) not in attendance_tracker:
                    # Attempt to get the student from the database
                    try:
                        student = Student.objects.get(user_name=name)

                        # Record attendance for the matched student
                        AttendanceRecord.objects.create(
                            student=student,
                            enrollmentNumber=enrollment_number,
                            semester=semester,
                            faculty_name=faculty_username,
                            time_slot=time_slot,
                            lecture_name=lecture_name,
                            department=faculty_department
                        )

                        # Add the student to the attendance tracker
                        attendance_tracker[(name, time_slot)].add(student.id)

                    except Student.DoesNotExist:
                        print(f"No student found with the name: {name}")

            face_names.append(f"{name} ({enrollment_number})")

        # Draw rectangles and display names on the frame
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Display the frame
        cv2.imshow('Video', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all windows
    video_capture.release()
    cv2.destroyAllWindows()

    return redirect('faculty_view')


def generate_attendance_pdf(request):
    # Retrieve faculty username from the session
    faculty_username = request.session.get('faculty_username')
    selected_time_slot = request.session.get('selected_time_slot')

    if not faculty_username:
        return HttpResponse("Faculty not authenticated.", status=403)

    today = timezone.now().date()

    # Retrieve attendance records for the specific faculty from the database
    attendance_records = AttendanceRecord.objects.filter(faculty_name=faculty_username,time_slot=selected_time_slot,attendance_date=today)
    
    if not attendance_records:
        return HttpResponse("No attendance records found for the specified faculty.", status=404)
    
    # Generate PDF content using ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{faculty_username}_attendance_report.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)
    
    # Include semester, faculty name, and subject name in the PDF header
    header = f"Semester: {attendance_records.first().semester}\nFaculty: {faculty_username}\nSubject: {attendance_records.first().lecture_name}"
    header_paragraph = Paragraph(header, getSampleStyleSheet()["Normal"])
    
    # Create a table with attendance data
    table_data = [['Enrollment Number', 'Name', 'Lecture Name', 'Date', 'Time slot']]
    for record in attendance_records:
        table_data.append([
            record.student.enrollmentNumber,
            record.student.user_name,
            record.lecture_name,
            str(record.attendance_date),  # Convert date to string
            record.time_slot
        ])
    
    # Create a table and apply styling
    table = Table(table_data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Build the PDF
    content = [header_paragraph, table]  # Combine header and table
    pdf.build(content)

    return response

def faculty_view(request):
    # Simulated faculty username retrieved from session
    faculty_username = request.session.get('faculty_username')

    if faculty_username:
        # Retrieve the selected time slot from session
        selected_time_slot = request.session.get('selected_time_slot')

        if selected_time_slot:
            # Filter attendance records for the current day, faculty, and selected time slot
            today = date.today()
            attendance_records = AttendanceRecord.objects.filter(
                attendance_date=today,
                faculty_name=faculty_username,
                time_slot=selected_time_slot,
            )
            
            return render(request, 'faculty_view.html', {'attendance_records': attendance_records})
        else:
            # If no time slot is selected, render a message to the user
            return render(request, 'no_time_slot_selected.html')  # Corrected template name
    else:
        # Render an error message if faculty username is not found in session
        return render(request, 'error.html', {'error_message': 'Faculty username not found in session'})


def succesful(request):
    return render(request,'succesful.html')

def change_pass1(request):
    return render(request,'change_pass1.html')

def forgot_pass1(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            faculty = Faculty.objects.get(email=email)  # Use the Student model
        except Faculty.DoesNotExist:
            messages.error(request, 'Email not found')
            return redirect('forgot_pass1')

        # Generate a token for the user
        uid = urlsafe_base64_encode(force_bytes(faculty.pk))
        token = default_token_generator.make_token(faculty)

        # Construct the reset link
        reset_link = request.build_absolute_uri(
            f'/reset_password1/{uid}/{token}/'
        )

        # Send the reset link to the user's email
        send_reset_link_email(email, reset_link)

        # Redirect the user to a page indicating that the reset link has been sent
        return render(request, 'reset_link_sent.html', {'reset_link': reset_link})

    return render(request, 'forgot_pass1.html')

def send_reset_link_email(email, reset_link):
    subject = 'Password Reset'
    message = f'Click this link to reset your password: {reset_link}'
    sender_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, sender_email, recipient_list)

def change_pass1(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
    except (TypeError, ValueError, OverflowError):
        uid = None

    try:
        faculty = Faculty.objects.get(pk=uid)
    except Faculty.DoesNotExist:
        faculty = None

    if faculty is not None and default_token_generator.check_token(faculty, token):
        if request.method == "POST":
            # Retrieve password from POST data
            password = request.POST.get('password')
            confirm_password = request.POST.get('reconfirm_password')

            # Validate password and confirm_password
            if password and confirm_password and password == confirm_password:
                # Update student's password
                faculty.set_password(password)
                faculty.save()  # Save the updated student object
                messages.success(request, 'Password has been reset successfully.')
                return redirect('faculty_sign')  # Redirect to login page after successful password change
            else:
                # Passwords do not match or are empty
                messages.error(request, 'Passwords do not match.')
        
        # Render the change password page
        return render(request, 'change_pass1.html')
    else:
        return render(request, 'invalid_reset_link.html')

def option(request):
    return render(request,'option.html')

def fdetail(request):
    return render(request,'fdetail.html')