from django.db import models
from django.utils.translation import gettext as _
from core.utils import validate_latex_file,get_unique_filename

# Modèle pour représenter un système scolaire
class SchoolSystem(models.Model):
    class Meta:
        verbose_name = _('Système Scolaire')
        verbose_name_plural = _('Systèmes Scolaire')
        
    name = models.CharField(max_length=120, unique=True, verbose_name=_('Nom'))
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('Ajouter le'),null=True)
    
    def __str__(self):
        return self.name

# Modèle pour représenter un cursus
class Cursus(models.Model):
    class Meta:
        verbose_name = _('Cursus')
        verbose_name_plural = _('Cursus')
        
    name = models.CharField(max_length=120, unique=True, verbose_name=_('Nom'))
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('Ajouter le'),null=True)
    
    def __str__(self):
        return self.name
    
# Modèle pour représenter un niveau d'étude
class Level(models.Model):
    class Meta:
        verbose_name = _('Niveau D\'étude')
        verbose_name_plural = _('Niveaux D\'étude')

    name = models.CharField(max_length=120, unique=True, verbose_name=_('Nom'))
    cursus = models.ForeignKey(Cursus, on_delete=models.SET_NULL, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('Ajouter le'),null=True)

    def __str__(self):
        return self.name

# Modèle pour représenter un diplôme
class Degree(models.Model):
    class Meta:
        verbose_name = _('Diplôme')
        verbose_name_plural = _('Diplômes')

    name = models.CharField(max_length=120, unique=True, verbose_name=_('Nom'))
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('Ajouter le'),null=True)

    def __str__(self):
        return self.name
    
# Modèle pour représenter une série liée au cursus lycéen
class Serie(models.Model):
    class Meta :
        verbose_name = _('Série')
        verbose_name_plural = _('Séries')

    name = models.CharField(max_length=120, unique=True, verbose_name=_('Nom'))
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('Ajouter le'),null=True)
    
    def __str__(self):
        return self.name
    
# Modèle pour représenter une formation liée à des diplômes,cursus et autres...
class Formation(models.Model):
    class Meta:
        verbose_name = _('Formation')
        verbose_name_plural = _('Formations')
        unique_together = ["name", "level"]
        
    name = models.CharField(max_length=120, verbose_name=_('Nom'))
    cursus = models.ForeignKey(Cursus, on_delete=models.SET_NULL, blank=False, null=True)
    serie = models.ForeignKey(Serie, on_delete=models.SET_NULL, blank=True, null=True)
    school_system = models.ManyToManyField(SchoolSystem, verbose_name=_('Systèmes scolaire'))
    level = models.ForeignKey(Level,on_delete=models.SET_NULL,blank=False, null=True, verbose_name=_('Niveaux d\'étude'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('Ajouter le'),null=True)

    def __str__(self):
        niveaux_label = "Niveau"
        if self.serie:
            return f'{self.name} {self.serie.name} - {niveaux_label}: {self.level.name}'
        return f'{self.name} - {niveaux_label}: {self.level.name}'
    
    @property
    def full_name(self):
        return self.__str__()
    
    @property
    def short_name(self) :
        if self.serie :
            return f'{self.name} {self.serie.name}'
        return f'{self.name}'
    
# Modèle pour représenter un cours liée à des foramtions,icons    
class Course(models.Model):
    class Meta :
        verbose_name = _('Cours')
        verbose_name_plural = _('Cours')
        unique_together = ["name", "formation"]
        
    name = models.CharField(max_length=120, verbose_name=_('Nom du cours'))
    formation = models.ForeignKey(Formation,on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('Ajouter le'),null=True)
    
    def __str__(self):
        niveau_label = "Niveau"
        return f'{self.name} - {niveau_label} : {self.formation.level.name}'
 
# Modèle pour représenter un chapitre d'un cours liée a des fiches de TD et examen 
class CourseChapter(models.Model):
    class Meta :
        verbose_name = _('Chapitre')
        verbose_name_plural = _('Chapitres')
        unique_together = ["name", "course"]
        
    name = models.CharField(max_length=120, verbose_name=_('Nom du chapitre'))
    course = models.ForeignKey(Course,on_delete=models.SET_NULL, blank=False, null=True,verbose_name=_('Cours'))
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('Ajouter le'),null=True)
    
    def __str__(self):
        niveau_label = "Niveau"
        return f'{self.course.name} - {self.name} - {niveau_label}: {self.course.formation.level}'
    
    
class ExamFile(models.Model):
    class Meta :
        verbose_name = _('Fiche d\'examen')
        verbose_name_plural = _('Fiches d\'examen')
        unique_together = ('course', 'exam_year')
        
    course = models.ForeignKey(Course, null=True, blank=False, on_delete=models.CASCADE,verbose_name=_('Cours'))
    exam_file = models.FileField(upload_to='exam_file/', null=True, blank=False,verbose_name=_('Fiche d\'examen'),validators=[validate_latex_file])   
    exam_year = models.IntegerField(null=False, blank=False, verbose_name=_('Année de l\'examen'))
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('Ajouter le'),null=True)
    
    def save(self, *args, **kwargs):
        if self.exam_file:
            self.exam_file.name = get_unique_filename(self.exam_file.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        niveau_label = "Niveau"
        return f'{self.course.name} - {niveau_label} : {self.course.formation.level} - Fiche de d\'examen'
    
    @property
    def name(self):
        return self.__str__()


    