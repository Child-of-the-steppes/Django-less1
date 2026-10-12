from django.db import migrations


def copy_teacher_relations(apps, schema_editor):
    Student = apps.get_model('school', 'Student')
    db_alias = schema_editor.connection.alias
    through = Student.teachers.through

    relations = [
        through(student_id=student.pk, teacher_id=student.teacher_id)
        for student in Student.objects.using(db_alias).all().iterator()
    ]

    through.objects.using(db_alias).bulk_create(relations, batch_size=1000)


class Migration(migrations.Migration):
    dependencies = [
        ('school', '0002_student_teachers_alter_student_group_and_more'),
    ]

    operations = [
        migrations.RunPython(copy_teacher_relations, migrations.RunPython.noop),
    ]