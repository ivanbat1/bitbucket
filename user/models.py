from django.db import models
# import mptt
# from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.


class GeneralR(models.Model):
    name = models.CharField(max_length=32, blank=False, null=True)
    position = models.CharField(max_length=32, blank=True, null=True)
    salary = models.CharField(max_length=32, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='children')
    # create_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    image = models.ImageField(upload_to='image/', default='image/images.jpg',null=True, blank=True)


    def __str__(self):
        return '{}'.format(self.name)



