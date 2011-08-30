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

Basic user data that I am storing is username, hashed password and salt.

Registering
-----------

The user provides an username that is tested for uniqueness as a database constrain. Using a database constrain assures us that the database will deal with problems like concurrency and race conditions that might occur from multiple users trying to register the same login at the same time.

The user also provides a password. The password will be tested for:

  Minimum size 

Registering process is:

  #We randomly generate a salt. 
    
  #Then we mix the salt with the password provided and hash it using md5. 
 
  #We finally store the salt and hashed password in the database.

The idea behind this salt and password is that we are not as vulnerable to precomputed rainbow tables.

 

 





