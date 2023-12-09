from django.db import models

class Expense(models.Model):

    title = models.CharField(max_length=1024)
    amount = models.IntegerField()
    

    class Meta:
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Expense_detail", kwargs={"pk": self.pk})
