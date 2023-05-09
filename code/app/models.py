from django.db import models


class Commands(models.Model):
    command = models.TextField(blank=True, null=True)
    technique = models.ForeignKey('Techniques', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commands'


class Reasons(models.Model):
    tactic = models.ForeignKey('Tactics', models.DO_NOTHING, blank=True, null=True)
    technique = models.ForeignKey('Techniques', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reasons'


class Tactics(models.Model):
    external_id = models.CharField(unique=True, max_length=6)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tactics'


class Techniques(models.Model):
    external_id = models.CharField(unique=True, max_length=9)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_subtechnique = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'techniques'