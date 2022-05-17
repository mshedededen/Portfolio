# WELCOME TO FRIENDLYREMINDER, V1.001
# Libraries
import secrets
# 1. Generate Friends
def generate_friends():
    # Globally define variables to use them throughout the code
    global master_friends
    global friends_uncontacted
    global friends_contacted
    # Assign properties to these variables
    master_friends = []
    friends_uncontacted = []
    friends_contacted = []
    # Code
    while True:
        answer = input('Add friends to your friends list (Press ENTER when finished): ')
        if answer == '':
            break
        else:
            master_friends.append(answer)
            continue
    friends_uncontacted = master_friends

# 2. Random
def randomise_friend(friends_uncontacted, friends_contacted):
    # 1. Generate friend
    while True:
        selected_friend = secrets.choice(friends_uncontacted)
        print('Today you should contact %s.' % selected_friend)
        # 2. Operand to ensure text input is valid
        while True:
            has_friend_been_contacted = input('Have you contacted %s? (Y/N): ' % selected_friend)
            if has_friend_been_contacted == 'Y' or has_friend_been_contacted == 'N':
                break
            else:
                print('Invalid response. Please re-enter.')
                continue
        # 3.  Remove old friend if 'Y'
        #     Add friend to 'new' list (friend will be stored here until refresh)
        #     Ensure that old friend list has been overwritten
        if has_friend_been_contacted == 'Y':
            friends_uncontacted.remove(selected_friend)
            friends_contacted.append(selected_friend)
            break
            #     Do nothing if 'N'
        elif has_friend_been_contacted == 'N':
            while True:
                try_again = input('Another time. Do you wish to generate a new friend? (Y/N)')
                if try_again == 'Y' or try_again == 'N':
                    break
                else:
                    print('Invalid response. Please re-enter.')
                    continue
            if try_again == 'Y':
                continue
            elif try_again == 'N':
                break

# 3. Add
def add_friend(master_friends, friends_uncontacted): # Friends are added to 'to be contacted friends'
    friend_to_add = input('Please type in the name of the friend you wish to get a FriendlyReminder on.')
    master_friends.append(friend_to_add)
    friends_uncontacted.append(friend_to_add)
    print('%s added as a friend!' % friend_to_add)
# 4. Remove
def remove_friend(master_friends, friends_uncontacted, friends_contacted): # Friends may be in either list, so a searchable query needs to be made. DATAFRAME format would reduce replication
    while True:
        friend_to_remove = input('Please type in the name of the friend you wish to drop from FriendlyReminder.')
        if friend_to_remove in master_friends:
            break
        else:
            print('%s not found. Please re-enter.\nSee list of friends below:' % friend_to_remove)
            print(master_friends)
            continue
    master_friends.remove(friend_to_remove)
    if friend_to_remove in friends_uncontacted:
        friends_uncontacted.remove(friend_to_remove)
    elif friend_to_remove in friends_contacted:
        friends_contacted.remove(friend_to_remove)

# 5. Reset
def reset_friends_contacted(friends_contacted, master_friends):
    # Reasign friends_uncontacted as a global variable
    global friends_uncontacted
    # Code
    friends_contacted.clear()
    friends_uncontacted = master_friends

# 6. Wipe
# This function is the same as the generate_friends function

# 7. View
def view_friends(friends_contacted, friends_uncontacted):
    print('Friends contacted: ')
    print(', '.join(friends_contacted))
    print('Friends to be contacted: ')
    print(', '.join(friends_uncontacted))

# 8. Commands
def commands_list():
    print('Welcome, what do you wish to do?',
    '\n"Random": Randomly generate a friend to contact.',
    '\n"Add": Add a friend to your list of friends.',
    '\n"Remove": Remove a friend from your list of friends.',
    '\n"Reset": Wipe log of friends contacted.',
    '\n"Wipe": Completely edit your list of friends and start afresh.',
    '\n"View": View a list of friends you can contacted and friends you have not.',
    '\n"Commands": See a list of all possible commands which can be used.')

# 7. 2nd_level_loop
def second_level_loop():
    print('Welcome, what do you wish to do?',
        '\n"Random": Randomly generate a friend to contact.',
        '\n"Add": Add a friend to your list of friends.',
        '\n"Remove": Remove a friend from your list of friends.',
        '\n"Reset": Wipe log of friends contacted.',
        '\n"Wipe": Completely edit your list of friends and start afresh.',
        '\n"View": View a list of friends you can contacted and friends you have not.',
        '\n"Commands": See a list of all possible commands which can be used.')
    while True:
        what = input('So, what do you wish to do?')
        if what == 'Random':
            randomise_friend(friends_uncontacted = friends_uncontacted, friends_contacted = friends_contacted)
        elif what == 'Add':
            add_friend(master_friends = master_friends, friends_uncontacted = friends_uncontacted)
        elif what == 'Remove':
            remove_friend(master_friends = master_friends, friends_uncontacted = friends_uncontacted, friends_contacted = friends_contacted)
        elif what == 'Reset':
            reset_friends_contacted(friends_contacted = friends_contacted, master_friends = master_friends)
        elif what == 'Wipe':
            generate_friends()
        elif what == 'View':
            view_friends(friends_uncontacted = friends_uncontacted, friends_contacted = friends_contacted)
        elif what == 'Commands':
            commands_list()
        else:
            print('%s is an invalid response. Please re-enter.' % what)

# 8. 1st_level_loop
def first_level_loop():
    # Users
    global user
    # Code
    while True:
        user = input('Are you a first-time user? (Y/N)')
        if user == 'Y' or user == 'N':
            break
        else:
            print('Invalid response. Please re-enter.')
            continue
    # New users have the option to create their list of friends.
    if user == 'Y':
        generate_friends()
        second_level_loop()
    else:
        second_level_loop()

# Testing code
first_level_loop()
