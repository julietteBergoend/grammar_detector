# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Entrees(models.Model):
    id_entree = models.AutoField(primary_key=True)
    entree = models.TextField()

    class Meta:
        managed = False
        db_table = 'Entrees'

    def __str__(self):
        return self.entree


class Mots(models.Model):
    id_mots = models.AutoField(primary_key=True)
    mots = models.TextField()

    class Meta:
        managed = False
        db_table = 'Mots'

    def __str__(self): #on affiche nos objets dans Admin avec leur contenu
        return self.mots

class Phrases(models.Model):
    id_phrases = models.AutoField(primary_key=True)
    phrase = models.TextField()
    nombre_mots = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Phrases'

    def __str__(self): #on affiche nos objets dans Admin avec leur contenu
        return self.phrase


class PhrasesHasMots(models.Model):
    phrases_id_phrases = models.ForeignKey(Phrases, models.DO_NOTHING, db_column='Phrases_id_phrases', primary_key=True)  # Field name made lowercase.
    mots_id_mots = models.ForeignKey(Mots, models.DO_NOTHING, db_column='Mots_id_mots')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Phrases_has_Mots'
        unique_together = (('phrases_id_phrases', 'mots_id_mots'),)


class Prononciations(models.Model):
    id_prononciation = models.AutoField(primary_key=True)
    prononciation = models.TextField()

    class Meta:
        managed = False
        db_table = 'Prononciations'

    def __str__(self): #on affiche nos objets dans Admin avec leur contenu
        return self.prononciation


class Tags(models.Model):
    id_tags = models.AutoField(primary_key=True)
    suite_tags = models.TextField()

    class Meta:
        managed = False
        db_table = 'Tags'

    def __str__(self): #on affiche nos objets dans Admin avec leur contenu
        return self.suite_tags


class TagsHasPhrases(models.Model):
    tags_id_tags = models.ForeignKey(Tags, models.DO_NOTHING, db_column='Tags_id_tags', primary_key=True)  # Field name made lowercase.
    phrases_id_phrases = models.ForeignKey(Phrases, models.DO_NOTHING, db_column='Phrases_id_phrases')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tags_has_Phrases'
        unique_together = (('tags_id_tags', 'phrases_id_phrases'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
