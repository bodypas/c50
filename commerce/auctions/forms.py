from .models import *
from django.forms import ModelForm, Textarea

# I know, there are some spelling mistakes through all this project, but left them, because didn't want to be confused later.

class ListningForm(ModelForm):
    class Meta:
        model = Listning
        fields = ['title', 'category', 'description', 'image', 'price', ]
       

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 10}),
        }

class AuctionForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']