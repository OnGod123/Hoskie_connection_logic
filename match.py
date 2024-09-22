from datetime import timedelta
from django.db.models import Q
from .models import Person, UserProfile

def find_matching_users_with_profiles(current_user):
    """
    Finds up to 50 users in the database that match the given user's criteria
    based on relationship status, sexual orientation, race, location, and within a five-year age gap.
    Ensures that these users have a corresponding profile in UserProfile.
    """
    # Get the user's details
    relationship_status = current_user.relationship_status
    sexual_orientation = current_user.sexual_orientation
    race = current_user.race
    birth_date = current_user.birth_date
    location = current_user.location

    # Calculate the date range for the 5-year age gap
    five_years_ago = birth_date - timedelta(days=5*365.25)  # Account for leap years
    five_years_later = birth_date + timedelta(days=5*365.25)  # Account for leap years

    # Query the database to find matches
    matches = Person.objects.filter(
        Q(relationship_status=relationship_status) &
        Q(sexual_orientation=sexual_orientation) &
        Q(race=race) &
        Q(birth_date__range=[five_years_ago, five_years_later]) &
        Q(location=location)  # Filter by location
    ).exclude(id=current_user.id)  # Exclude the current user from the results

    # Ensure each match has a corresponding UserProfile
    profiles = UserProfile.objects.filter(user__in=matches)
    profiles_set = set(profiles.values_list('user_id', flat=True))  # Set of user IDs with profiles

    # Filter matches to only include those with a profile
    matches_with_profiles = [match for match in matches if match.id in profiles_set]

    # Limit the results to 50 users
    limited_matches_with_profiles = matches_with_profiles[:50]

    # Get the profiles for these matches
    user_profiles = UserProfile.objects.filter(user__in=limited_matches_with_profiles)

    # Create a dictionary to easily access profile data by user ID
    profile_data = {profile.user_id: profile for profile in user_profiles}

    return [(match, profile_data.get(match.id)) for match in limited_matches_with_profiles]
