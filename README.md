The Challenge: Sample Auth system
================================================

a backend that possesses the following

main functions:
===============

Setting New Users
-----------------

A new user can register with their e-mail address and a password of choice. Once the
registration process is complete, the user will receive a confirmation e-mail. This e-mail will
contain a link that needs to be clicked on within a fixed period of time in order to activate
the account.

Authentication
--------------


Users enter their e-mail address and password to log in. The account will be locked
automatically for a certain period of time after repeated attempts at logging in with an
incorrect password.

Authorization
---------------
Access to specified resources is only possible for users who have registered and possess an
adequate account.



The necessary data should be stored in an SQL database. Please develop a suitable
schema and create a python module that provides the functionality described above.
Python Database API v2.0 will be available in order to connect to the database.
It is not part of the task to connect to a website (or even to write HTML for the site), to
maintain web sessions via cookies or the like, or to integrate authorization with other
modules.
Please record your solution in an appropriate way. We are especially interested in a
discussion of your chosen implementation as compared with other possible approaches,
and in any potential extensions.

My solution:
============

Database
---------

As a proof of concept I'm using a simple sqlite database.

But, I am placing all sql specific code inside a dbutils file so that later it can be changed for a more robust full blown sql backend.

User table
-----------

Basic user data that I am storing is email, hashed password, salt, creation date, a token(for activating) and activated date.

Registering and Activating
---------------------------

The user provides an email that is tested for uniqueness as a database constrain. Using a database constrain assures us that the database will deal with problems like concurrency and race conditions that might occur from multiple users trying to register the same login at the same time.

The email will be also validated against the following rules

  * no spaces

  * only letters, numbers and ".-_%" in the username
  
  * only letters, numbers and ".-" in the domain 
  
  * The top level domain (TLD) should exist and have between 2 and 4 letters 

The user also provides a password. The password will be tested for:

  * Minimum size of 6 characters 

Registering process is:

  * We randomly generate a salt. 
    
  * Then we mix the salt with the password provided and hash it using SHA1. 
 
  * We finally store the salt and hashed password in the database.

The idea behind this salt and password is that we are not as vulnerable to precomputed rainbow tables.

Using SHA1 lets us be platform independent, if we used some database specific crypt method changing databases would be more of a challenge. The way it is we can quickly convert the data for all of the major databases.

Also during the register process a 16 char token will be generated and sent in a email.
 
If the token is not validated in the amount of days setted in the settings.DAYS_TO_ACTIVATE property it becomes invalid.

A method that can be called by a cron process deletes invalid users

Authentication
--------------

Authentication is done by email and password. Every wrong try increases a counter by one. If the number is higher than the settings.MAX_PWD_TRIES property the authentication is not done and a exception is returned.

When a successful authentication is done the number of tries is reset.

The authentication returns a auth_token that is used by the authorization processes

A method that can be called by a cron process lowers from time to time the number of failed tries.


Authorization
--------------

Based on the auth_token received from the authentication the system returns a True or False if the user is valid.

In a web application the auth_token should be saved in a crypted cookie and send to the backend once per request or when necessary.

Cleanup
-------

Cleanup is a task that should be run periodically, usually from a cron task

Cleanup does two things.

First it decreases the number of failed passwords attempts. So that the user can try again.

Second it removes users that have not activated the account after the link expired.

Usage
======


    import auth

To create the database

    db = auth.dbutils.DB()
    db.create_database()

to Create an user


    auth.register("root@localhost.ada", "cheese")

Email received:

    Date: Thu,  1 Sep 2011 05:38:42 -0300 (BRT)
    From: noreply@localhost
    To: root@localhost.ada
    Subject: [auth] Account Activation

    Welcome! please activate your account with the code: dorjo0zevckbfwqkfpmugukme6mcwjeh

To activate the account 
    
    auth.activate("dorjo0zevckbfwqkfpmugukme6mcwjeh")

To login:

    auth.authenticate("root@localhost.ada", "cheese")

"HXEx8xaDO5OWzalClzED4k5amm0a780v"

Returns the auth_token that you use toto check if you have authorization

    auth.authorize("HXEx8xaDO5OWzalClzED4k5amm0a780v")

Authorization returns True or False if the auth_token is valid

The clean up can be called directly from bash

    $ auth/cleanup.py



 





