from django.shortcuts import render
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField, Q
from issues.models import Issue
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncDay

User = get_user_model()

def analytics_home(request):
    open_count = Issue.objects.filter(status='Open').count()
    in_progress_count = Issue.objects.filter(status='In Progress').count()
    closed_count = Issue.objects.filter(status='Closed').count()
    
    # For average resolution time:
    closed_issues = Issue.objects.filter(status='Closed')
    avg_resolution = closed_issues.aggregate(
        avg_time=Avg(ExpressionWrapper(F('updated_at') - F('created_at'), output_field=DurationField()))
    )['avg_time']
    
    if avg_resolution:
        total_seconds = int(avg_resolution.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        avg_resolution_time = f"{days}d {hours}h {minutes}m"
    else:
        avg_resolution_time = "N/A"
    
    # Issues by category for open or in-progress issues
    issues_by_category = Issue.objects.filter(status__in=['Open', 'In Progress']).values('category').annotate(issue_count=Count('id')).order_by('-issue_count')
    
    context = {
        'open_issues_count': open_count,
        'in_progress_issues_count': in_progress_count,
        'closed_issues_count': closed_count,
        'avg_resolution_time': avg_resolution_time,
        'issues_by_category': issues_by_category,
    }
    return render(request, 'analytics/index.html', context)

def analytics_stats(request):
    # Aggregate count of issues by status
    status_counts = Issue.objects.values('status').annotate(count=Count('status'))
    
    # Prepare data for chart (labels and counts)
    labels = [entry['status'] for entry in status_counts]
    data = [entry['count'] for entry in status_counts]
    
    return render(request, 'analytics/analytics_stats.html', {
        'labels': labels,
        'data': data
    })

def analytics_filter(request):
     # Hard-coded statuses you want to display
    allowed_statuses = ['Open', 'In Progress', 'Closed']

    status_filter = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    assignee_filter = request.GET.get('assignee', '')
    search_query = request.GET.get('search', '')

    issues = Issue.objects.all()

    # Apply filters if provided
    if status_filter:
        issues = issues.filter(status=status_filter)

    if category_filter:
        issues = issues.filter(category=category_filter)

    if assignee_filter:
        issues = issues.filter(assignee=assignee_filter)

    if search_query:
        issues = issues.filter(Q(title__icontains=search_query))

    # Get distinct categories and staff users for the dropdowns
    categories = Issue.objects.values_list('category', flat=True).distinct()
    staff_users = User.objects.filter(is_staff=True)

    context = {
        'issues': issues,
        'allowed_statuses': allowed_statuses,  # pass the static list to the template
        'categories': categories,
        'staff_users': staff_users,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'assignee_filter': assignee_filter,
        'search_query': search_query,
    }
    return render(request, 'analytics/analytics_filter.html', context)

def analytics_issues(request):
    closed_issues = Issue.objects.filter(status='Closed')

    # Calculate the time taken for each issue
    closed_issues_data = []
    for issue in closed_issues:
        time_to_close = issue.updated_at - issue.created_at
        time_to_in_progress = issue.updated_at - issue.status_changed_at  # assuming 'status_changed_at' exists
        closed_issues_data.append({
            'issue': issue,
            'time_to_close': time_to_close,
            'time_to_in_progress': time_to_in_progress
        })

    return render(request, 'analytics/analytics_issues.html', {'closed_issues_data': closed_issues_data})

def analytics_charts(request):
    # 1. Pie Chart Data: Issues by Status
    pie_qs = Issue.objects.values('status').annotate(count=Count('id'))
    pie_labels = [entry['status'] for entry in pie_qs]
    pie_data = [entry['count'] for entry in pie_qs]

    # 2. Bar Chart Data: Issues by Category
    bar_qs = Issue.objects.values('category').annotate(count=Count('id')).order_by('category')
    bar_labels = [entry['category'] for entry in bar_qs]
    bar_data = [entry['count'] for entry in bar_qs]

    # 3. Line Chart Data: Issues Over Time
    created_qs = Issue.objects.annotate(day=TruncDay('created_at')).values('day').annotate(count=Count('id')).order_by('day')
    closed_qs = Issue.objects.filter(status='Closed').annotate(day=TruncDay('updated_at')).values('day').annotate(count=Count('id')).order_by('day')
    created_dict = {entry['day'].strftime('%Y-%m-%d'): entry['count'] for entry in created_qs}
    closed_dict = {entry['day'].strftime('%Y-%m-%d'): entry['count'] for entry in closed_qs}
    all_days = sorted(set(list(created_dict.keys()) + list(closed_dict.keys())))
    line_labels = all_days
    line_created_data = [created_dict.get(day, 0) for day in all_days]
    line_closed_data = [closed_dict.get(day, 0) for day in all_days]

    # 4. Staff Workload Data
    workload_qs = Issue.objects.filter(assignee__isnull=False).values('assignee__username').annotate(count=Count('id')).order_by('assignee__username')
    workload_labels = [entry['assignee__username'] for entry in workload_qs]
    workload_data = [entry['count'] for entry in workload_qs]

    context = {
        'pie_labels': pie_labels,
        'pie_data': pie_data,
        'bar_labels': bar_labels,
        'bar_data': bar_data,
        'line_labels': line_labels,
        'line_created_data': line_created_data,
        'line_closed_data': line_closed_data,
        'workload_labels': workload_labels,
        'workload_data': workload_data,
    }
    return render(request, 'analytics/analytics_charts.html', context)