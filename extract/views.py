from django.shortcuts import redirect, render
from extract import tools

from blog.models import Category, Country, Language
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def index(request):
    seo={
        "robots": "noindex, nofollow"
    }
    context = {
        'seo':seo
    }
    return render(request,'superindex.html',context)


@user_passes_test(lambda u: u.is_superuser)
def extract(request):
    postUrl=request.POST['postUrl']
    categoryId=Category.objects.get(id=request.POST['category'])
    countryId=Country.objects.get(id=request.POST['country'])
    languageId=Language.objects.get(id=request.POST['language'])
    tags=request.POST['gtags']

    print(postUrl,categoryId,countryId,languageId)
    tools.extractUrls(postUrl,categoryId,countryId,languageId,tags)
    return redirect('/superuser/')