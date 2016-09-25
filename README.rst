==============
Django Tracker
==============

Uses Django middleware to record page views, by user. This app is intended for Django sites, that are:

#. used by authorized (e.g. logged in) users. If the users are not authorized, then you are better off using your server log file to track page views

#. low volume. If adding 100 milliseconds or so to each page request would be a problem, then do not use this app. I have not timed


The results are written to CSV files in settings.MEDIA_PATH/tracker. A new one directory for each day. Part of the reason I do not write this data to a database is for me, it's pretty low value data. I do not want it cluttering up my database and I do not want to create a separate database for this data. Using a new file for each day makes manual searching easier. And makes it easy to delete data by date.

Also, for my uses, the data is not used very often, so the overhead of parsing the CSV file(s) it and possibly filtering it is not a problem.

**The tracker does NOT track super users.**

It tracks by email address, so each user should have an email address.


Installation
------------

1. Add to INSTALLED_APPS in settings::

    INSTALLED_APPS = (
        ...
        'django_tracker',
        ...
    )

2. Add to MIDDLEWARE in settings::

    MIDDLEWARE_CLASSES = (
        ...
        'django_tracker.tracker_middleware.TrackerManager'
        ...
    )

3. Make sure you have this line in your TEMPLATE_CONTEXT_PROCESSORS in settings::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.core.context_processors.request',
        ...
    )

4. Add pattern to url patterns::

    urlpatterns = patterns(
        '',
        ...
        url(r'^django_tracker/', include('django_tracker.urls', namespace='django_tracker')),
        ...
    )

5. If you want users who are not superusers to be able to see the stats, then add "django_tracker" to Django groups. I do that using Django Admin.


Django Tracker Views (e.g. stats pages)
---------------------------------------
The django_tracker views are restricted to superusers and users in the "django_tracker" Django group.


Django Tracker in Templates
---------------------------
If you want to make template content depend on whether or not a user is permitted to see the tracker stats, use this
template filter::

    {% load django_tracker_tags %}
    ...

    {% if request|show_django_tracker %}
        <li><a href="{% url 'django_tracker:stats_selector' %}">Tracker</a></li>
    {% endif %}

Where "request" is the context variable provided by 'django.core.context_processors.request'. If you are wondering about the somewhat odd form of this code, see: `Stackoverflow <http://stackoverflow.com/questions/19998912/django-templatetag-return-true-or-false>`_


Tracker Demo
------------
Tracker demo is a minimal Django project for testing and showing the functionality of Django Tracker. After you get the database setup, run the command:

    python manage.py make_tracker_demo_data

This creates some users along with passwords. Look at the code /django_tracker/management/commands/make_tracker_demo_data.py for details. You can login with any of these users and then see the results in the tracker files.

"demo_app" is for simulating a project with multiple apps.