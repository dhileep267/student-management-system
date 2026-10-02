from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = ["name", "age", "email", "course", "phone"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter student name"
            }),

            "age": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "1"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter email"
            }),

            "course": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter course"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter phone number"
            }),
        }

    def clean_age(self):
        age =self.cleaned_data["age"]
        if age <15 or age> 60:
            raise forms.ValidationError( "Age must be between 15 and 60.")
        else:
            return age

    def clean_email(self):
        email = self.cleaned_data["email"]

        if not email.endswith("@gmail.com"):
            raise forms.ValidationError(
            "Please use a Gmail address."
        )

        existing_student = Student.objects.filter(
           email=email
         ).exclude(
        pk=self.instance.pk
         ).first()

        if existing_student:
          raise forms.ValidationError(
            "A student with this email already exists."
         )

        return email

    def clean_phone(self):
       phone = self.cleaned_data["phone"]

       if phone and not phone.isdigit():
        raise forms.ValidationError(
            "Phone number must contain only digits."
        )

        if phone and len(phone) != 10:
          raise forms.ValidationError(
            "Phone number must be exactly 10 digits."
          )

        return phone
    def clean(self):
        cleaned_data = super().clean()

        age = cleaned_data.get("age")
        course = cleaned_data.get("course")

        if age is not None and course:
         if course.strip().lower() == "bsc ai/ml" and age < 17:
            raise forms.ValidationError(
                "BSc AI/ML students must be at least 17 years old."
            )

        return cleaned_data