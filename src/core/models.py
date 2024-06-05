from django.db import models
from django.contrib.auth.models import User

class Partner(models.Model):
    identifier = models.TextField(blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    name = models.TextField(blank=True, null=False)
    link = models.URLField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'partner'

    def get_created_at(self):
        return self.created_at.strftime('%d/%m/%Y')

class Score(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, blank=False, null=False) 
    score_club = models.IntegerField(blank=False, null=False) 
    score = models.IntegerField(blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    
    class Meta:
        db_table = 'score'

    def get_created_at(self):
        return self.created_at.strftime('%d/%m/%Y')

User.add_to_class('followed_partners', models.ManyToManyField(Partner, related_name='followers'))
