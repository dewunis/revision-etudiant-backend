from django.contrib import admin
from .models import (
    Cursus,
    SchoolSystem,
    Level,
    Formation,
    Degree,
    Serie,
    Course,
    CourseChapter,
    ExamFile,
)

admin.site.register(Cursus,)
admin.site.register(Course,)
admin.site.register(CourseChapter,)
admin.site.register(Level,)
admin.site.register(Formation,)
admin.site.register(SchoolSystem,)
admin.site.register(Serie,)
admin.site.register(Degree,)
admin.site.register(ExamFile,)
