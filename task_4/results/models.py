from django.db import models

class MedicalImageResult(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    device_name = models.CharField(max_length=100)
    average_before_normalization = models.FloatField(null=True, blank=True)
    average_after_normalization = models.FloatField(null=True, blank=True)
    data_size = models.IntegerField(null=True, blank=True)
    raw_data = models.JSONField()

    def save(self, *args, **kwargs):
        # Calculate averages and data size
        data_list = [list(map(int, item.split())) for item in self.raw_data.get('data', [])]
        flat_data = [item for sublist in data_list for item in sublist]
        self.data_size = len(flat_data)
        if flat_data:
            self.average_before_normalization = sum(flat_data) / len(flat_data)
            self.average_after_normalization = self.average_before_normalization / 100  # Example normalization
        super().save(*args, **kwargs)