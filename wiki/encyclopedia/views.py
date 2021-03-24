from django.shortcuts import render, redirect
from django import forms
import markdown2
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries":util.list_entries()
    })

def m_title(request,title):
    
    page=util.get_entry(title)
    all_pages = util.list_entries()
    
    if title not in all_pages:
        return render(request, "encyclopedia/error.html",)
    
    
    mardowner = Markdown()
    converted_page = mardowner.convert(page)
    

    return render(request, "encyclopedia/title.html", {
        "title":title,
        "content":converted_page,
    })
    
       


class NewPageForm(forms.Form):
    
    title = forms.CharField(label="Title",required = True,
    widget= forms.TextInput
    (attrs={
    'placeholder':'Write your page title here',
    'class':'form-text',
    'style':'width:400px'
    }))

    content = forms.CharField(label="Markdown content",required= False, 
    widget= forms.Textarea
    (attrs={
    'placeholder':'Write your Markdown content here',
    'class':'form-text',
    'style':'height:200px',
    }))
    
    

def new(request):
    if request.method == "GET":
        new_page= NewPageForm()
        return render(request, "encyclopedia/new.html", {
            "new_page":new_page
        })
    else:
        new_page = NewPageForm(request.POST)
        if new_page.is_valid():

            title = new_page.cleaned_data["title"]
            content = new_page.cleaned_data["content"]


            entries = util.list_entries()
            for entry in entries:
                if title.lower() == entry.lower():
                    new_page = NewPageForm()
                    return render(request, "encyclopedia/pageexists.html", {
                        "entry":entry,
                        "new_page":new_page,
                    })

            util.save_entry(title,content)
            return m_title(request,title)

        else:
            return render(request, "encyclopedia/new.html", {
            "new_page":new_page
            })






def edit(request, title):
    if request.method == "POST":
        edit_form = NewPageForm(request.POST)
        if edit_form.is_valid():
            title = edit_form.cleaned_data ["title"]
            content = edit_form.cleaned_data ["content"]

            util.save_entry(title=title, content=content)
            return m_title(request,title)
    else:
        
        content = util.get_entry(title)
        edit_form = NewPageForm({
            "title":title,
            "content":content
            })
        return render(request, "encyclopedia/edit.html", {
            "edit_form":edit_form,
            "title":title, 
            },
        )


def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return m_title(request=request, title=random_entry)


def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()
    search_entry = [ entered_entry for entered_entry in entries if query.lower() in entered_entry.lower()]
    
    if len(search_entry) == 0:
        return render(
            request, "encyclopedia/search.html", {
            "search_entry":"",
            "query":query
            },
        )

    if query == "":
        return render(
            request, "encyclopedia/search.html", {
            "search_entry":"",
            
            },
        )
    
  
    
    if len(search_entry) == 1:
        return m_title(request, search_entry[0])

    return render(
        request, "encyclopedia/search.html", {
        "search_entry":search_entry,
        "query":query
        },
    )

