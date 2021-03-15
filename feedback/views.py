# shop/views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse
from django.shortcuts import render

from feedback.models import Feedback
from utils.charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict


@staff_member_required
def statistics_view(request):
    return render(request, 'statistics.html', {})


@staff_member_required
def statistics_view_by_giver(request):
    return render(request, 'statistics_by_giver.html', {})


@staff_member_required
def get_filter_options(request):
    grouped_feedback = Feedback.objects.annotate(name=F('giver__name')).values('giver__name').distinct()
    options = [feedback['giver__name'] for feedback in grouped_feedback]

    grouped_feedback_year = Feedback.objects.annotate(year=ExtractYear('date')).values('year').order_by('-year').distinct()
    options_year = [feedback['year'] for feedback in grouped_feedback_year]

    return JsonResponse({
        'options_giver': list(set(options)),
        'options_year': options_year,
    })


@staff_member_required
def get_year_filter_options(request):
    grouped_feedback = Feedback.objects.annotate(year=ExtractYear('date')).values('year').order_by('-year').distinct()
    options = [feedback['year'] for feedback in grouped_feedback]

    return JsonResponse({
        'options': options,
    })


@staff_member_required
def get_giver_filter_options(request):
    grouped_feedback = Feedback.objects.annotate(name=F('giver__name')).values('giver__name').distinct()
    options = [feedback['giver__name'] for feedback in grouped_feedback]

    return JsonResponse({
        'options': list(set(options)),
    })


@staff_member_required
def get_entrustability_chart(request, year):
    feedback = Feedback.objects.filter(date__year=year)
    grouped_feedback = feedback.annotate(entrustability_score=F('entrustability')).annotate(month=ExtractMonth('date')) \
        .values('month').annotate(average=Avg('entrustability')).values('month', 'average').order_by('month')

    feedback_dict = get_year_dict()

    for group in grouped_feedback:
        feedback_dict[months[group['month']-1]] = round(group['average'], 2)

    return JsonResponse({
        'title': f'Entrustability in {year}',
        'data': {
            'labels': list(feedback_dict.keys()),
            'datasets': [{
                'label': 'Average Entrustability Score',
                'borderColor': '#007bff',
                'data': list(feedback_dict.values()),
            }]
        },
    })


@staff_member_required
def activity_type_chart(request, year):
    feedback = Feedback.objects.filter(date__year=year)
    grouped_purchases = feedback.values('activity').annotate(count=Count('id')) \
        .values('activity', 'count').order_by('activity')

    feedback_dict = dict()

    for activity in Feedback.ACTIVITIES:
        feedback_dict[activity[1]] = 0

    for group in grouped_purchases:
        feedback_dict[dict(Feedback.ACTIVITIES)[group['activity']]] = group['count']

    return JsonResponse({
        'title': f'Activity type in {year}',
        'data': {
            'labels': list(feedback_dict.keys()),
            'datasets': [{
                'label': 'Amount of Feedback Received',
                'backgroundColor': generate_color_palette(len(feedback_dict)),
                'borderColor': generate_color_palette(len(feedback_dict)),
                'data': list(feedback_dict.values()),
            }]
        },
    })

@staff_member_required
def get_entrustability_chart_by_giver(request, year, giver):
    entrustability_values = Feedback.objects.filter(date__year=year).filter(giver__name=giver).values('entrustability').order_by('date')
    entrustability_dates = Feedback.objects.filter(date__year=year).filter(giver__name=giver).values('date').order_by('date')
    e_values = [values['entrustability'] for values in entrustability_values]
    e_dates = [dates['date'] for dates in entrustability_dates]
    return JsonResponse({
        'title': f'Entrustability Feedback from {giver} in {year}',
        'data': {
            'labels': e_dates,
            'datasets': [{
                'label': 'Entrustability Scores',
                'borderColor': '#007bff',
                'data': e_values,
            }]
        },
    })