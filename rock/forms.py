from django import forms
from .models import PicInfo


class FileFieldForm(forms.Form):
    file_field = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))


class NormalSerchForm(forms.Form):
    search_field = forms.CharField(max_length=100, label=False, widget=forms.TextInput(
        attrs={'class': 'form-control mb-2', 'placeholder': '功能开发中', 'disabled': True}))


class DetailedSearchForm(forms.Form):
    ORTH_CHOICE = (('', '———'),) + PicInfo.ORTH_MODE

    region_field = forms.CharField(max_length=30, label='地区', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))
    mine_field = forms.CharField(max_length=50, label='井号', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))
    # depth_field = forms.FloatField(label='井深', required=False, widget=forms.TextInput(
    #     attrs={'class': 'form-control form-control-sm'}))
    depth_field = forms.FloatField(label='井深', required=False, widget=forms.NumberInput(
        attrs={'class': 'form-control form-control-sm'}))
    lens_field = forms.IntegerField(
        label='物镜倍数', required=False, widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm'}))
    orth_field = forms.ChoiceField(
        label='正交偏光', required=False, choices=ORTH_CHOICE, widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))


class AllPhotosSearchForm(forms.Form):
    mines_selected = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'hidden': True}))
    depth_low = forms.FloatField(
        required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 1000, 'required': True}))
    depth_high = forms.FloatField(
        required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 1000, 'required': True, 'disabled': True}))
    lens_selected = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'hidden': True}))
    orths_selected = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'hidden': True}))
