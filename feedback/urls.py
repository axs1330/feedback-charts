from django.urls import path

from . import views

urlpatterns = [
    path('statistics/', views.statistics_view, name='statistics'),
    path('statistics-by-giver/', views.statistics_view_by_giver, name='statistics-by-giver'),
    path('chart/filter-options/', views.get_filter_options, name='chart-filter-options'),
    path('chart/year-filter-options/', views.get_year_filter_options, name='chart-year-filter-options'),
    path('chart/giver-filter-options/', views.get_giver_filter_options, name='chart-giver-filter-options'),
    path('chart/entrustability/<int:year>/', views.get_entrustability_chart, name='chart-entrustability'),
    path('chart/activity-type/<int:year>/', views.activity_type_chart, name='chart-activity-type'),
    path('chart/entrustability/<int:year>/<str:giver>', views.get_entrustability_chart_by_giver, name='chart-entrustability-by-giver'),
]