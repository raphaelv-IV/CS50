from django import forms
from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random

class NewPage(forms.Form):
    title = forms.CharField(label= "Title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')
    
class EditPage(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class EntryForm(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Encyclopedia'}))

markdown = Markdown()

def index(request):
    search_list = []
    entries = util.list_entries()
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    convert = markdown.convert(page)
                    return render(request, "encyclopedia/entry_page.html", {
                        'title': item,
                        'form': EntryForm(),
                        'page': convert
                    })
                if item in i: 
                    search_list.append(i)
            return render(request, "encyclopedia/search.html", {
                 'form': EntryForm(),
                'searched': search_list          
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "form": EntryForm(),
            "entries": util.list_entries() 
            
        })
            
def random_page(request):
    if request.method == 'GET':
        entries = util.list_entries()
        rand = random.randint(0, len(entries) - 1)
        random1 = entries[rand]
        page = util.get_entry(random1)
        convert = markdown.convert(page)
        return render(request, "encyclopedia/entry_page.html", {
            'title': random1, 
            'form': EntryForm(),
            'page': convert
        })

def edit_page(request, title):
    if request.method == 'GET':
        result = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
            'edit': EditPage(initial={'textarea': result}),
            'form': EntryForm(),
            'title': title
        })
    else:
        form = EditPage(request.POST) 
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title, textarea)
            page = util.get_entry(title)
            convert= markdown.convert(page)
            return render(request, "encyclopedia/entry_page.html", {
                'form': EntryForm(),
                'page': convert,
                'title': title
            })

def entry_page(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        convert = markdown.convert(page) 
        return render(request, "encyclopedia/entry_page.html", {
            'page': convert,
            'title': title,
            'form': EntryForm()
        })
    else:
        return render(request, "encyclopedia/error_page.html", {
            "form": EntryForm(),
            "message": "Not found." 
        })

def new_page(request):
    if request.method == 'POST':
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error_page.html", {
                    "form": EntryForm(), 
                    "message": "Page Exists"
                })
            else:
                util.save_entry(title,textarea)
                page = util.get_entry(title)
                convert = markdown.convert(page)
                return render(request, "encyclopedia/entry_page.html", {
                    'title': title,
                    'form': EntryForm(),
                    'page': convert        
                })
    else:
        return render(request, "encyclopedia/new_page.html", {
            "post": NewPage(),
            "form": EntryForm() 
        })
