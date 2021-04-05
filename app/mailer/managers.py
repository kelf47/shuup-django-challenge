from django.db import models
from django.db.models import Sum, Count


class OrdersAnnotationQuerySet(models.QuerySet):

    def annotate_order_info(self):
        return self.annotate(
            order_sum=Sum('orders__total')).annotate(
                order_count=Count('orders'))


class OrderInfoAnnotateManager(models.Manager):

    """
    Manager to annotate order_sum and order_count in Company and
    Contact querysets, using 'with_order_info' manager.
    """

    def get_queryset(self):
        return OrdersAnnotationQuerySet(
            self.model, using=self._db).annotate_order_info()
