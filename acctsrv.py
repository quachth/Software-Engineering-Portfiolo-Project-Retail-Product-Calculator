# Name:     Theresa Quach
# Course:   CS361
# Project:  Sprint#1: Account manager program for the Retail Calculator program. For new users, program saves new user accounts that the user can use to login with, and creates
#            a new file with their username where their projects will be saved, and returns the filename. For existing users, program returns the filename for that user if a
#            matching account is found.

import time


def acct():
    """
    Function that, if it reads the line "create account" or "login in the 'acctnotif.txt' document, creates an account and file for the user
    or logs the user into the program by notifying the main program to open the user's file.
    """

    # Open and read the first line from the file and strip off newline to get action
    fd1 = open("acctnotif.txt","r+")
    action = fd1.readline()
    action = action.strip('\n')

    # Create a new account
    if (action == "create account"):
        fd2 = open("rcaccounts.txt", "r+")
        user_input = fd1.readline()                                                                                             
        user_input = user_input.strip('\n')
        account = user_input.split(':')                                                                                         # account is array: [0] = username and [1] is password from acctnotif.txt

        # Iterate through recorded user accounts to see if username is already taken
        for line in fd2:                                                                                                       
            recorded_user = line.split(':')                                                                                     # recorded_user is array: [0] = username and [1] is password from rcaccounts.txt
            if (account[0].lower() == recorded_user[0].lower()):
                    fd1.seek(0)
                    fd1.write("user exists\n")
                    fd1.truncate(len("user exists\n"))
                    break
        fd2.close()
        
        # Check acctnotif.txt for update
        fd1.seek(0)
        action = fd1.readline()  
        action = action.strip('\n')
 
        if (action != "user exists"):
            fd1.seek(0)
            fd1.truncate(0)
            fd1.write("user created\n")
            fd1.write(account[0]+'\n')

			# Save new user account to recorded accounts
            fd2 = open("rcaccounts.txt", "a+")
            fd2.write(user_input+'\n')
            fd2.close()

			# Create new text document for the user using their username - for project management
            fd3 = open(account[0]+".txt", "w+")
            fd3.close()


    # Log into an existing account
    if (action == "login"):
        fd2 = open("rcaccounts.txt", "r+")
        user_input = fd1.readline()
        account = user_input.split(':')

		# Iterate through recorded user accounts to see if username:password combo exists
        for line in fd2:
            recorded_user = line.split(':')
            recorded_user[1] = recorded_user[1].strip('\n')


            # If the user is found 
            if (account[0].lower() == recorded_user[0].lower()):
                # Password correct
                if (account[1] == recorded_user[1]):
                    fd1.seek(0)
                    fd1.truncate(0)
                    fd1.write("user found\n")
                    fd1.write(account[0]+"\n")
                    break
                # Password incorrect
                else:
                    fd1.seek(0)
                    fd1.truncate(0)
                    fd1.write("bad password\n")
                    break
        fd2.close()

        # Outside of loop; check acctnotif for updates and if username was not found, tell main program user account was not found
        fd1.seek(0)
        action = fd1.readline()
        action = action.strip('\n')
        if (action != "user found" and action != "bad password"):
            fd1.seek(0)
            fd1.truncate(0)
            fd1.write("user not found")


    fd1.close()
        

        


if __name__ == '__main__':
    print("Account Service Manager running")
    while True:
        time.sleep(1)
        acct()