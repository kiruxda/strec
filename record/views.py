from django.shortcuts import render

def test(request):
    data={
        'title':'record main page'
    }
    return render(request, 'main/index.html',data)
