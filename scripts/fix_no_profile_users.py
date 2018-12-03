from dashboard.models import Profile, User
from utils.mailer import EmailHelper


def run(*args):
    users = User.objects.filter(profile__isnull=True, is_active=False)

    for user in users:
        print(user)

        profile = Profile(user=user, reset_token=Profile.get_new_reset_token())
        profile.save()

        EmailHelper.email(
            'no_profile_email',
            user.email,
            'Openmaker Explorer - signup',
            {
                'USER_NAME': user.first_name,
                'CONFIRMATION_LINK': 'https://explorer.openmaker.eu/onboarding/confirmation/{}'.format(profile.reset_token),
            }
        )

