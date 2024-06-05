from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Partner, Score

@login_required
def preferences(request):
    user = request.user
    all_partners = Partner.objects.all()
    followed_partners = user.followed_partners.all()

    if request.method == "POST":
        if 'add_partner' in request.POST:
            partner_id = request.POST['add_partner']
            partner = Partner.objects.get(id=partner_id)
            user.followed_partners.add(partner)
        elif 'remove_partner' in request.POST:
            partner_id = request.POST['remove_partner']
            partner = Partner.objects.get(id=partner_id)
            user.followed_partners.remove(partner)
        return redirect('preferences')

    context = {
        'all_partners': all_partners,
        'followed_partners': followed_partners
    }
    return render(request, 'preferences.html', context)

def promotions(request):
    today = timezone.now().date()
    scores_today = Score.objects.filter(created_at__date=today)

    if scores_today:
        scores_with_partners = scores_today.select_related('partner')
        
    else:
        yesterday = today - timedelta(days=1)
        scores_yesterday = Score.objects.filter(created_at__date=yesterday)
        scores_with_partners = scores_yesterday.select_related('partner')

    context = {
            'request': request,
            'scores_with_partners': scores_with_partners
        }
    return render(request, 'promotions.html', context)