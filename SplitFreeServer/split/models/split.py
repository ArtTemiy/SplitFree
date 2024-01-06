from _decimal import Decimal
from dataclasses import dataclass
from functools import reduce

import django.db.models as models
from django.contrib.auth.models import User
from rest_framework.relations import SlugRelatedField
from rest_framework import serializers

from groups.models import Group


@dataclass
class Section:
    title: str


@dataclass
class Category:
    title: str
    section: Section


class Sections:
    General = Section('General')
    Food = Section('Food')
    Utilities = Section('Utilities')
    Other = Section('Other')


_categories: dict[Category] = {
    'general': Category('General', Sections.General),

    'bar': Category('Bar', Sections.Food),
    'breakfast': Category('Breakfast', Sections.Food),
    'dinner': Category('Dinner', Sections.Food),
    'launch': Category('Launch', Sections.Food),
    'coffee': Category('Coffee', Sections.Food),

    'electricity': Category('Electricity', Sections.Utilities),
    'water': Category('Water', Sections.Utilities),
    'gas': Category('Gas', Sections.Utilities),
    'cleaning': Category('Cleaning', Sections.Utilities),
    'internet': Category('Internet', Sections.Utilities),
    'mobile': Category('Mobile', Sections.Utilities),
    'rent': Category('Rent', Sections.Utilities),

    'gifts': Category('Gifts', Sections.Other),
    'games': Category('Games', Sections.Other),
}


def _get_choices():
    return [(k, v.title) for k, v in _categories.items()]


class Split(models.Model):
    title = models.CharField(max_length=128, blank=False)
    description = models.TextField(max_length=2048, blank=True)
    category = models.CharField(max_length=64, choices=_get_choices())
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.group.name})'


class Spend(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # > 0 if borrowed, < 0 if owed
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    split = models.ForeignKey(Split, related_name='spends', on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.user.username if self.user is not None else "*deleted*"}: {self.amount})'


class SpendSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = Spend
        exclude = ['split', 'id']


class SplitSerializer(serializers.ModelSerializer):
    spends = SpendSerializer(many=True)
    amount = serializers.SerializerMethodField(method_name='_get_amount', read_only=True)

    class Meta:
        model = Split
        fields = '__all__'

    def _get_amount(self, obj: Split):
        res = reduce(
            lambda s, spend: s + (spend.amount if spend.amount > 0 else 0),
            Spend.objects.filter(split=obj),
            0
        )
        return f'{res: .2f}'

    def _create_spends(self, instance, spends_data):
        r = Spend.objects.filter(split=instance).delete()
        for spend_data in spends_data:
            Spend.objects.create(split=instance, **spend_data).save()

    def validate_spends(self, spends):
        if reduce(
            lambda s, v: s + v['amount'],
            spends,
            0
        ) != 0:
            raise serializers.ValidationError('Spends sum not equal to 0')
        return spends

    def create(self, validated_data):
        spends_data = validated_data.pop('spends')
        split = Split.objects.create(**validated_data)
        self._create_spends(split, spends_data)
        return split

    def update(self, instance: Split, validated_data):
        if 'spends' in validated_data:
            spends_data = validated_data.pop('spends')
            self._create_spends(instance, spends_data)

        return super().update(instance, validated_data)
