# profile file syntax:
# contact ID (for retrieval in Contact.csv
# primary email password
# secondary email password
# third email password
# Sequence of events on startup coded as three char IDs. Example: SLK (sherlock username), RIC (rickroll),
# DTE (date and time), etc.

def load(user):
    file = open('Functions/Profiles/profile.csv')
    for line in file:
        if line.__contains__(user):
            return line
    return "NO USER"


# creating a new user profile
def create(user, password, email, emailPassword):
    file = open('Functions/Profiles/profile.csv', "a")
    newProfile = user + ',' + password + ',' + email + ',' + emailPassword
    file.writelines(newProfile)
    file.close()


def isProfile(user):
    file = open('Functions/Profiles/profile.csv', "r")
    fileContent = []
    for line in file:
        fileContent.append(line)

    for line in fileContent:
        if line.__contains__(user):
            return True
    return False
