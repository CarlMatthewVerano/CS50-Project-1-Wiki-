from django.shortcuts import render, redirect

from . import util

from markdown2 import markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_page(request, title):

    content = util.get_entry(title.strip())

    if content is None:
        return render(request, "encyclopedia/errorPage.html")

    content = markdown(content)
    return render(request, "encyclopedia/titleEntry.html", {
        "title": title,
        "content": content
    })