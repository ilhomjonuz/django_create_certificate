from django.db import models


COURSES = (
    ('frontend', "FRONTEND DEVELOPER"),
    ('backend', "BACKEND DEVELOPER"),
    ('web_design', "GRAPHIC DESIGN"),
)

class CourseCertificate(models.Model):
    fullname = models.CharField(max_length=255)
    course = models.CharField(max_length=10, choices=COURSES)
    image = models.ImageField(upload_to='certificates/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'certificates'
