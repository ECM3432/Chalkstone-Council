# issues/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from .models import Issue
from .forms import UserIssueForm, StaffIssueForm

# Create Issue
@login_required
def issue_create(request):
    # Choose form based on user type
    if request.user.is_staff:
        form = StaffIssueForm(request.POST or None)
    else:
        form = UserIssueForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        issue = form.save(commit=False)
        issue.reporter = request.user  # Set the logged-in user as the reporter
        issue.status = 'Open'  # Default status for new issues
        issue.save()
        return redirect('issue_detail', pk=issue.pk)
    
    return render(request, 'issues/issue_form.html', {'form': form})


# List all issues (staff only) or only the user's issues
@login_required
def issue_list(request):
    if request.user.is_staff:
        issues = Issue.objects.all()  # Staff can see all issues
    else:
        issues = Issue.objects.filter(reporter=request.user)  # Users can see only their own issues
    
    return render(request, 'issues/issue_list.html', {'issues': issues})


# View details of a specific issue
def issue_detail(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    
    # If user is not staff or reporter, deny access
    if not request.user.is_staff and issue.reporter != request.user:
        raise Http404("You do not have permission to view this issue.")
    
    return render(request, 'issues/issue_detail.html', {'issue': issue})


# Edit an issue (staff only, with options to assign, change status)
@login_required
def issue_edit(request, pk):
    issue = get_object_or_404(Issue, pk=pk)

    # Allow only staff or the reporter to edit
    if not (request.user.is_staff or issue.reporter == request.user):
        return redirect('issue_detail', pk=issue.pk)

    # Use different form depending on whether the user is staff or regular user
    if request.method == 'POST':
        if request.user.is_staff:
            form = StaffIssueForm(request.POST, instance=issue)
        else:
            form = UserIssueForm(request.POST, instance=issue)  # Regular users can only change title/description
        if form.is_valid():
            form.save()
            return redirect('issue_detail', pk=issue.pk)
    else:
        if request.user.is_staff:
            form = StaffIssueForm(instance=issue)
        else:
            form = UserIssueForm(instance=issue)

    return render(request, 'issues/issue_form.html', {'form': form, 'issue': issue})


# Delete an issue (staff only)
@login_required
def issue_delete(request, pk):
    issue = get_object_or_404(Issue, pk=pk)

    # Only staff can delete issues
    if not request.user.is_staff:
        return redirect('issue_detail', pk=issue.pk)

    if request.method == 'POST':  # Confirm deletion
        issue.delete()
        return redirect('issue_list')

    return render(request, 'issues/issue_confirm_delete.html', {'issue': issue})


# Filter by category or show all categories
@login_required
def issue_category(request, category=None):
    if category:
        issues = Issue.objects.filter(category=category)  # Filter by the selected category
    else:
        issues = Issue.objects.all()  # Show all issues if no category selected
    
    categories = Issue.CATEGORY_CHOICES  # You can add this list of categories in the model
    return render(request, 'issues/issue_category_list.html', {'issues': issues, 'categories': categories})
