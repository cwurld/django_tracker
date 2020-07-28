==============
Django Tracker
==============

Uses Django middleware to record page views, by user. This app is intended for Django sites, that are:

#. used by authorized (e.g. logged in) users. If the users are not authorized, then you are better off using your server log file to track page views

#. low volume. If adding 100 milliseconds or so to each page request would be a problem, then do not use this app. I have not timed it.


The results are written to CSV files in settings.MEDIA_PATH/tracker. A new one directory for each day. Part of the reason I do not write this data to a database is for me, it's pretty low value data. I do not want it cluttering up my database and I do not want to create a separate database for this data. Using a new file for each day makes manual searching easier. And makes it easy to delete data by date.

Also, for my uses, the data is not used very often, so the overhead of parsing the CSV file(s) it and possibly filtering it is not a problem.

**The tracker does NOT track super users.**

It tracks by email address, so each user should have an email address.


Installation
------------

#. Add to INSTALLED_APPS in settings::

    INSTALLED_APPS = (
        ...
        'django_tracker',
        ...
    )

#. Add to MIDDLEWARE in settings::

    MIDDLEWARE = (
        ...
        'django_tracker.tracker_middleware.TrackerManager'
        ...
    )

#. Make sure you have this line in your TEMPLATES in settings::

    TEMPLATES = {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                ]
         }
    }

#. Add pattern to url patterns::

    urlpatterns = patterns(
        '',
        ...
        url(r'^django_tracker/', include('django_tracker.urls', namespace='django_tracker')),
        ...
    )

#. Add "tracker" folder to settings.MEDIA_ROOT

#. If you want users who are not superusers to be able to see the stats, then add "django_tracker" to Django groups. I do that using Django Admin.

#. The default is to not geo-locate the ip addresses. If you want to use the ipinfo.io geo-locator, then get an access token from them and put it in settings.IPINFO_TOKEN. If you want to provide your own geo-locator, then create a function named "geo_locate" that accepts an ip address and returns the location as a string. Also when the ip address is "help" return a string a non-null string. Set settings.GEO_LOCATE_FUNC to a string that contains the import path to the module with your function.


Django Tracker Views (e.g. stats pages)
---------------------------------------
The django_tracker views are restricted to superusers and users in the "django_tracker" Django group.


Django Tracker in Templates
---------------------------
To put this in an HTML list (e.g. a bootstrap navbar dropdown), you can use this template include::

    {% include 'django_tracker/menu_include.html' %}

For more fine-grained control, there is a template filter that can be used to only show a link to the tracker to users who are permitted to see it::

    {% load django_tracker_tags %}

    {% if request|show_django_tracker %}
        <a href="{% url 'django_tracker:stats_selector' %}">Tracker</a>
    {% endif %}

If you are wondering about the somewhat odd form of this code, see: `Stackoverflow <http://stackoverflow.com/questions/19998912/django-templatetag-return-true-or-false>`_


Tracker Demo
------------
Tracker demo is a minimal Django project for testing and showing the functionality of Django Tracker. To run it,  install the requirements and run the command to setup the data base:

    python manage.py migrate

Next run:

    python manage.py make_tracker_demo_data

This creates some users along with passwords. Look at the code /django_tracker/management/commands/make_tracker_demo_data.py for details. You can login with any of these users and then see the results in the tracker files.

"another_app" is for simulating a project with multiple apps.

If you want to geo locate anonymous users, you will need to add the setting: IPINFO_TOKEN. You can get the token from ipinfo.io.