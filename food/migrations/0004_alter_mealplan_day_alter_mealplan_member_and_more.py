# Generated by Django 4.0.2 on 2022-02-25 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_mealplan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealplan',
            name='day',
            field=models.CharField(choices=[('MON', 'MONDAY'), ('TUE', 'TUESDAY'), ('WED', 'WEDNESDAY'), ('THU', 'THURSDAY'), ('FRI', 'FRIDAY'), ('SAT', 'SATURDAY'), ('SUN', 'SUNDAY')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='food.member'),
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='food.recipe'),
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
