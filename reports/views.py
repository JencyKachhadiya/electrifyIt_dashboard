import datetime
from django.shortcuts import render
from django.db.models import Sum
from .models import Vehicle
from django.db.models.functions import ExtractWeek, ExtractMonth, ExtractYear


def test(request):
    total_miles = None

    start_date_str = request.POST.get('startDate')
    end_date_str = request.POST.get('endDate')

    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

        vehicles_within_range = Vehicle.objects.filter(date__range=[start_date, end_date])

        total_miles = vehicles_within_range.aggregate(total_miles=Sum('miles_driven'))['total_miles']

        total_miles = total_miles or 0
    except (ValueError, Vehicle.DoesNotExist):
        total_miles = 0
    return render(request, 'dashboard.html', {'total_miles': total_miles})


def index(request):
    total_miles = None
    # if request.method == 'POST':
    #     start_date_str = request.POST.get('startDate')
    #     end_date_str = request.POST.get('endDate')

    #     try:
    #         start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    #         end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

    #         vehicles_within_range = Vehicle.objects.filter(date__range=[start_date, end_date])

    #         total_miles = vehicles_within_range.aggregate(total_miles=Sum('miles_driven'))['total_miles']

    #         total_miles = total_miles or 0
    #     except (ValueError, Vehicle.DoesNotExist):
    #         total_miles = 0  

    return render(request, 'dashboard.html', {'total_miles': total_miles})

def total_miles_report(request):
    total_miles = request.GET.get('total_miles', 0)
    return render(request, 'total_miles_report.html', {'total_miles': total_miles})

def detailed_report(request):
    report_data = None
    if request.method == 'POST':
        start_date_str = request.POST.get('startDate')
        end_date_str = request.POST.get('endDate')
        group_by = request.POST.get('groupBy')

        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

            if group_by == 'daily':
                report_data = Vehicle.objects.filter(date__range=[start_date, end_date]) \
                    .values('date') \
                    .annotate(total_miles=Sum('miles_driven'))
            elif group_by == 'weekly':
                report_data = Vehicle.objects.filter(date__range=[start_date, end_date]) \
                    .annotate(week=ExtractWeek('date')) \
                    .values('week') \
                    .annotate(total_miles=Sum('miles_driven'))
            elif group_by == 'monthly':
                report_data = Vehicle.objects.filter(date__range=[start_date, end_date]) \
                    .annotate(month=ExtractMonth('date')) \
                    .values('month') \
                    .annotate(total_miles=Sum('miles_driven'))
            elif group_by == 'yearly':
                report_data = Vehicle.objects.filter(date__range=[start_date, end_date]) \
                    .annotate(year=ExtractYear('date')) \
                    .values('year') \
                    .annotate(total_miles=Sum('miles_driven'))

        except (ValueError, Vehicle.DoesNotExist):
            report_data = None  

    return render(request, 'detailed_report.html', {'report_data': report_data})


def date_range_report(request):
    data = None
    
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        
        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            data = Vehicle.objects.filter(date__range=[start_date, end_date])
        except ValueError:
            data = None  
        
    return render(request, 'date_range_report.html', {'data': data})