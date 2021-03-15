from django.db import models


class Giver(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Feedback(models.Model):
    date = models.DateField(auto_now_add=True)
    ACTIVITIES = [
        ('HP', 'History and Physical'),
        ('PD', 'Prioritize Differential Diagnosis'),
        ('RI', 'Recommend and Interpret Tests'),
        ('PH', 'Perform Handover'),
        ('PP', 'Perform Procedure'),
    ]
    activity = models.CharField(max_length=255, default='HP', choices=ACTIVITIES)
    giver = models.ForeignKey(to=Giver, on_delete=models.CASCADE)
    complex = models.BooleanField(default=False)
    complicated = models.BooleanField(default=False)
    ENTRUSTABILITY_SCORES = [
        (1, 'I did it.'),
        (2, 'I talked them through it.'),
        (3, 'I directed them from time to time.'),
        (4, 'I was available just in case.'),
    ]
    entrustability = models.IntegerField(default=1, choices=ENTRUSTABILITY_SCORES)
    done_well = models.TextField()
    needs_improvement = models.TextField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.giver} reported {self.entrustability} for {self.activity} on {self.date}'
