from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Student

@login_required
def dashboard(request):
    students = Student.objects.all()
    return render(request, "dashboard.html", {"students": students})

@login_required
def student_list(request):
    query = request.GET.get("q", "").strip()
    students = Student.objects.all()
    if query:
        students = students.filter(name__icontains=query)
    return render(request, "students/list.html", {"students": students, "query": query})

@login_required
def student_create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        age = request.POST.get("age", "").strip()
        email = request.POST.get("email", "").strip()
        course = request.POST.get("course", "").strip()
        phone = request.POST.get("phone", "").strip()

        if not all([name, age, email, course]):
            messages.error(request, "Please fill all required fields.")
            return render(request, "students/form.html", {"student": None})

        if Student.objects.filter(email=email).exists():
            messages.error(request, "A student with this email already exists.")
            return render(request, "students/form.html", {"student": None})

        Student.objects.create(
            name=name, age=age, email=email, course=course, phone=phone
        )
        messages.success(request, "Student added successfully.")
        return redirect("student_list")

    return render(request, "students/form.html", {"student": None})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        age = request.POST.get("age", "").strip()
        email = request.POST.get("email", "").strip()
        course = request.POST.get("course", "").strip()
        phone = request.POST.get("phone", "").strip()

        if Student.objects.filter(email=email).exclude(pk=pk).exists():
            messages.error(request, "Another student already uses this email.")
            return render(request, "students/form.html", {"student": student})

        student.name = name
        student.age = age
        student.email = email
        student.course = course
        student.phone = phone
        student.save()

        messages.success(request, "Student updated successfully.")
        return redirect("student_list")

    return render(request, "students/form.html", {"student": student})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
    return redirect("student_list")
