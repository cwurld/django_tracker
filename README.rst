==============
Django Tracker
==============

**Warning: this code is not even alpha yet. **

Uses Django middleware to record page views, by user. This app is intended for Django sites, that are:

#. used by authorized (e.g. logged in) users. If the users are not authorized, then you are better off using your server log file to track page views

#. low volume. If adding 100 milliseconds or so to each page request would be a problem, then do not use this app. I have not timed


The results are written to CSV files in settings.MEDIA_PATH/tracker. A new one directory for each day. Part of the reason I do not write this data to a database is for me, it's pretty low value data. I do not want it cluttering up my database and I do not want to create a separate database for this data. Using a new file for each day makes manual searching easier. And makes it easy to delete data by date.

Also, for my uses, the data is not used very often, so the overhead of parsing the CSV file(s) it and possibly filtering it is not a problem.

The tracker does NOT track super users.

It tracks by email address, so each user should have an email address.


Installation
------------

1. Add to INSTALLED_APPS:

    INSTALLED_APPS = (
        ...
        'django_tracker',
    )

2. Add to MIDDLEWARE:

    MIDDLEWARE_CLASSES = (
        ...
        'django_tracker.tracker_middleware.TrackerManager'
    )

Django Tracker Views (e.g. stats pages)
---------------------------------------
The django_tracker views are restricted to superusers and users in the "django_tracker" Django group.


Tracker Demo
------------
Tracker demo is a minimal Django project for testing and showing the functionality of Django Tracker. After you get the database setup, run the command:

    python manage.py make_tracker_demo_data

This creates some users along with passwords. Look at the code django_tracker/management/commands/make_tracker_demo_data.py for details. You can login with any of these users and then see the results in the tracker files.

"demo_app" is for simulating a project with multiple apps.