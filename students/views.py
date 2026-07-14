from django.contrib import messages 
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Student
from .forms import StudentForm


def home(request):
    query = request.GET.get('q')

    if query:
        students = Student.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(course__icontains=query)
        )
    else:
        students = Student.objects.all()

    return render(request, 'home.html', {'students': students})


def add_student(request):
    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():
         form.save()
        messages.success(request, "Student updated successfully!")
        return redirect('home')

    else:
        form = StudentForm()

    return render(request, 'add_student.html', {'form': form})


def update_student(request, id):
    student = Student.objects.get(id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('home')

    else:
        form = StudentForm(instance=student)

    return render(request, 'update_student.html', {'form': form})


def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect('home')