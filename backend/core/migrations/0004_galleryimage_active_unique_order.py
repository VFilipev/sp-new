from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_galleryimage_options_galleryimage_column'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='galleryimage',
            constraint=models.UniqueConstraint(
                fields=('position', 'column', 'order'),
                condition=models.Q(is_active=True),
                name='uniq_gallery_active_position_column_order',
            ),
        ),
    ]
