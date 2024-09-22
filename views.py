from django.shortcuts import render
from .models import Person
from .utils import find_matching_users_with_profiles  # Import your function

def profile_list_view(request):
    current_user = request.user  # Get the current logged-in user

    # Find matching users with profiles
    matches_with_profiles = find_matching_users_with_profiles(current_user)

    return render(request, 'profile_list.html', {'matches_with_profiles': matches_with_profiles})
