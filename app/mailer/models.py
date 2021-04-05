#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .managers import OrderInfoAnnotateManager

import logging
logger = logging.getLogger("mylogger")


class Company(models.Model):
    name = models.CharField(max_length=150)
    bic = models.CharField(max_length=150, blank=True)
    # Managers
    objects = models.Manager()
    with_order_info = OrderInfoAnnotateManager()

    def contact_data(self):
        # Return all related contacts with annotated order info
        return Contact.with_order_info.filter(
            company=self)


class Contact(models.Model):
    company = models.ForeignKey(
        Company, related_name="contacts", on_delete=models.PROTECT)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    # Managers
    objects = models.Manager()
    with_order_info = OrderInfoAnnotateManager()


@python_2_unicode_compatible
class Order(models.Model):
    order_number = models.CharField(max_length=150)
    company = models.ForeignKey(Company, related_name="orders")
    contact = models.ForeignKey(Contact, related_name="orders")
    total = models.DecimalField(max_digits=18, decimal_places=9)
    order_date = models.DateTimeField(null=True, blank=True)
    # for internal use only
    added_date = models.DateTimeField(auto_now_add=True)
    # for internal use only
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.order_number
