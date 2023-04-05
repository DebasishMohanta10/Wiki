from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import util
from django import forms
import random

class NewEntryForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea(),max_length=500)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request,title):
    entry = util.get_entry(title)
    return render(request,"encyclopedia/entry.html",{"entry": entry,"title": title})

def search(request):
    title = request.GET.get('q')
    if title in util.list_entries():
        entry = util.get_entry(title)
        return render(request,"encyclopedia/entry.html",{"entry": entry})
    else:
        if len([entry for entry in util.list_entries() if title in entry]):
            entries = [entry for entry in util.list_entries() if title in entry]
            return render(request, "encyclopedia/index.html", {
                "entries": entries
            })
        else:
            entries = []
            return render(request, "encyclopedia/index.html", {
                "entries": entries
            })

def new_page(request):
    form = NewEntryForm()
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            if title not in util.list_entries():
                util.save_entry(title,content)
                return redirect('index')
            else:
                return HttpResponse("Error")
    return render(request,"encyclopedia/newentry.html",{"form": form})

def edit_page(request,title):
    if request.method == 'GET':
        if title in util.list_entries():
            entry = util.get_entry(title)
            initial_dict = {
                "title": title,
                "content": entry
            }
            form = NewEntryForm(initial=initial_dict)
        return render(request,"encyclopedia/editentry.html",{"form": form,"title": title})
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title,content)
            return redirect('index')

def random_wiki(request):
    query=random.choice(util.list_entries())
    return redirect('entry',title=query)

                
