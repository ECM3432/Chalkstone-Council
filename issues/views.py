from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import Http404
from .models import Issue
from .forms import UserIssueForm, StaffIssueForm

User = get_user_model()

# List issues: Staff can see all, regular users can see only their own
def issue_list(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            issues = Issue.objects.all()  # Staff can see all issues
            users = User.objects.filter(is_staff=True)  # Get all staff users
        else:
            issues = Issue.objects.filter(reporter=request.user)  # Users can see only their own issues
            users = []  # No need for users if regular user
        
        return render(request, 'issues/issue_list.html', {'issues': issues, 'users': users})
    else:
        return render(request, 'issues/issue_list.html', {'issues': None, 'users': []})


# View details of an issue
def issue_detail(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if not request.user.is_staff and issue.reporter != request.user:
        raise Http404("You do not have permission to view this issue.")
    return render(request, 'issues/issue_detail.html', {'issue': issue})

# Create a new issue
@login_required
def issue_create(request):
    if request.user.is_staff:
        form = StaffIssueForm(request.POST or None)
    else:
        form = UserIssueForm(request.POST or None)

    # Handling the form submission
    if request.method == 'POST' and form.is_valid():
        issue = form.save(commit=False)
        issue.reporter = request.user  # Set the logged-in user as the reporter
        issue.status = 'Open'  # Default status for new issues
        issue.save()
        return redirect('issue_list')  # Redirect to the issue list page after creation
    
    return render(request, 'issues/issue_form.html', {'form': form})

# Edit an issue
@login_required
def issue_edit(request, pk):
    issue = get_object_or_404(Issue, pk=pk)

    # Allow only staff or the reporter to edit
    if not (request.user.is_staff or issue.reporter == request.user):
        return redirect('issue_detail', pk=issue.pk)

    if request.method == 'POST':
        if request.user.is_staff:
            form = StaffIssueForm(request.POST, instance=issue)
        else:
            form = UserIssueForm(request.POST, instance=issue)  # Regular users can only change title/description
        if form.is_valid():
            form.save()
            return redirect('issue_list')  # Redirecting to the issue list page after update
    else:
        if request.user.is_staff:
            form = StaffIssueForm(instance=issue)
        else:
            form = UserIssueForm(instance=issue)

    return render(request, 'issues/issue_edit.html', {'form': form, 'issue': issue})

# Delete an issue (only staff can delete)
@login_required
def issue_delete(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    
    if not request.user.is_staff:
        return redirect('issue_detail', pk=issue.pk)
    
    if request.method == 'POST':
        issue.delete()
        return redirect('issue_list')
    
    return render(request, 'issues/issue_confirm_delete.html', {'issue': issue})

# Filter issues by category
@login_required
def issue_category(request, category=None):
    if category:
        issues = Issue.objects.filter(category=category)
    else:
        issues = Issue.objects.all()

    categories = Issue.CATEGORY_CHOICES  # Retrieve categories from model
    return render(request, 'issues/issue_category_list.html', {'issues': issues, 'categories': categories})
