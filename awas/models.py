from django.db import models


class Location(models.Model):
    description = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    transport = models.TextField(null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    lock_no = models.TextField(null=True, blank=True)
    awas_incharge = models.TextField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    checkin_time = models.TimeField(null=True, blank=True)
    checkout_time = models.TimeField(null=True, blank=True)
    map_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.description + self.address

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'


# class Reservation(models.Model):
#     persons_reserved = models.IntegerField(null=True, blank=True)
#     location= models.ForeignKey(Location, on_delete=models.PROTECT)

#     class Meta:
#         verbose_name = 'Reservation'
#         verbose_name_plural = 'Reservations'

#     def save(self, *args, **kwargs):
#         print(f"saving reservation {self.guest_set}")
#         super(Reservation, self).save(*args, **kwargs) 

class Guest(models.Model):
    guest_name = models.TextField()
    city = models.TextField(null=True, blank=True)
    mobile_no = models.CharField(max_length=10)
    ext_reg_no = models.IntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, blank=True, null=True)
    remark = models.TextField(null=True, blank=True)
    no_of_persons = models.IntegerField(null=True, blank=True)
    arrival_date = models.DateTimeField(null=True, blank=True)
    departure_date = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    language = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    mandal = models.TextField(null=True, blank=True)
    # reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.guest_name

    class Meta:
        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'



