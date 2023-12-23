from django.shortcuts import render, redirect, reverse

from . import util

from markdown2 import markdown
from random import randint

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_page(request, title):

    content = util.get_entry(title.strip())

    if content is None:
        return render(request, "encyclopedia/errorPage.html")

    content = markdown(content)
    return render(request, "encyclopedia/getEntry.html", {
        "title": title,
        "content": content
    })

def search(request):
    q = request.GET.get('q').strip()
    entries = util.list_entries()

    matched_entries = []

    for title in entries:
        if q.lower() in title.lower():
            matched_entries.append(title)

    if matched_entries:
        exact = any(q.lower() == title.lower() for title in entries)
        if exact:
            return redirect(reverse('TITLE', args=[q.lower()]))

        return render(request, "encyclopedia/searchResults.html", {
            "entries": matched_entries,
        })
    
    return render(request, "encyclopedia/searchResults.html", {
        "entries": [],
    })

def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()

        if title == "":
            return render(request, "encyclopedia/createEntry.html", {
                "message": "No title!",
                "title": title,
                "content": content
            })
        
        if title in util.list_entries():
            return render(request, "encyclopedia/createEntry.html", {
                "message": "Title already exists.",
                "title": title,
                "content": content
            })
        
        util.save_entry(title, content)
        return redirect(reverse("TITLE", args=[title.lower()]))
    
    return render(request, "encyclopedia/createEntry.html")

def edit(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        return render(request, "encyclopedia/editEntry.html", {
            'error': "No Page Found"
        })

    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/editEntry.html", {
                "message": "Content is empty, cannot save.",
                "title": title,
                "content": content
            })
        util.save_entry(title, content)
        return redirect(reverse("TITLE", args=[title.lower()]))
    
    return render(request, "encyclopedia/editEntry.html", {
        'content': content,
        'title': title
    })

def random(request):
    entries = util.list_entries()
    random_entry = entries[randint(0, len(entries)-1)]
    return redirect(reverse("TITLE", args=[random_entry.lower()]))