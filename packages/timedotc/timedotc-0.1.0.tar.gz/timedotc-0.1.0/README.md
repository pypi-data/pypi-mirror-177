# Intro
This is an experimental auth library. It has not been tested in production yet. The scope of this experiment is to provide an auth method where the user can remember a target pin (much like a cipher) and calculate a one time code (otc) relative to the current time.

## Foreword
From a security standpoint, this is not very secure, but does prevent brute forcing to some extent.

### Problem 1:
If a third party knows the code and the timestamp of the code, they can easily compute the target and validate whenever they want.

### Problem 2:
Once the code has been computed, it is incremental, meaning that depending on the method, the code increments or decrements by 1 every minute.

### Problem 3:
Every day at the same time of the day the code will be the same if the target does not change.

## How it works
Given a pin only the user knows which will be referenced as the "target", validation is done by manually computing a code based on the difference between the current time and a code they manually compute.

Depending on the method, subtracting or adding, the code is calculated differently.

### Given the method is adding
If the target is 1111 and the current time is 12:34, the code would be 0987.

### If the method is subtracting
Using the same approach, the code would be 0123.

The code is then hashed and compared to the hash of the target.

## How to use

### Install
    pip install timedotc

### Import
    from timedotc import timedotc

### Create the auth object
    method = "sub"
    auth = timedotc(
        method=method,
        secret_key=secret_key,
    )

    target = auth.hash("0000")

### Validate
    code = "1111"
    auth.verify(code, target)

## Usage scenarios
This might be useful for loggin into an admin panel where there is only one user intended.

## Improvements

### Problem 3:
The target could have a parent target which depends on the current date (month and day) which once computed would modify the initial target (calulated based on H:M). This is still susceptible to problem 1 however.
