from django.shortcuts import render_to_response

def get(request):
    return render_to_response('calendar.html', {})
