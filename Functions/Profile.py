# profile file syntax:
# contact ID (for retrieval in Contact.csv
# primary email password
# secondary email password
# third email password
# Sequence of events on startup coded as three char IDs. Example: SLK (sherlock username), RIC (rickroll),
# DTE (date and time), etc.

def load(user):
    file = open('Functions/Profiles/' + user + '-profile.txt')
    returnList = []
    for line in file:
        returnList.append(line)
    return returnList


# creating a new user profile
def create(user, password, email, emailPassword):
    file = open('Functions/Profiles/' + user + '-profile.txt', "a")
    file.writelines([password, email, emailPassword])
    file.close()


def isProfile(user):
    if open('Functions/Profiles/' + user + '-profile.txt') == FileNotFoundError:
        return False
    else:
        return True
