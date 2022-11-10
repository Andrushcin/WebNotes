from django.db import models

class InfoPart(models.Model):
    header = models.CharField(max_length=150, blank=False)
    text_block = models.TextField(blank=True)

    class Meta:
        verbose_name = "Информационный блок"
        verbose_name_plural = "Информационные блоки"

