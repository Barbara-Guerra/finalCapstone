# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
"""
-This is a program designed for a small business to help it
to manage tasks assigned to each member of a team.
-This program will contain the use of: lists, dictionaries, functions,
string handling and error handling; as well as applying the concept of refactoring.
"""

#=====importing libraries===========
import os
from datetime import datetime, date

# Define the format for datetime strings. 
DATETIME_STRING_FORMAT = "%Y-%m-%d"

def read_tasks():
    # Check if the tasks.txt exists, if not create it.
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    # Read task data from the tasks.txt file.
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}
        
        # Split the task components by semicolon (;)
        task_components = t_str.split(";")

        # Extract and store the task attributes in a dictionary.
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        
        # Determine the due date and assigned date using the specified datetime format.
        try:
            curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
            curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        except ValueError:
            print("Invalid datetime format in tasks.txt. Please check the file.")
            continue
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        
        # Append the task dictionary to the task_list.
        task_list.append(curr_t)

    return task_list

def write_tasks(task_list):
    # Write the task_list to the tasks.txt file.
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

# This function allows you to register a new user. 
def reg_user():
    username_password = read_username_password()
    new_username = input("New Username: ")

    if new_username in username_password:
        print("Username already exists. Please try a different username.")
        return
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    #Check if the passwords match and add the new user. 
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        write_username_password(username_password)
    else:
        print("Passwords do not match")

# This function allows you to add a new task. 
def add_task():
    task_list = read_tasks()
    # Prompt for the username of the person assigned to the task.
    task_username = input("Name of person assigned to task: ")
    username_password = read_username_password()
    
    # Check if the username exists in the user database. 
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        task_due_date = input("Due date of task (YYYY-MM-DD): ")
        try:
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    # Add the new task to the task_list.
    task_list.append(new_task)
    # Write the updated task_list to the tasks.txt file. 
    write_tasks(task_list)
    print("Task successfully added.")

# This function allows the admin to view all the taks in the team. 
def view_all():
    # Read the task_list from the tasks.txt file.
    task_list = read_tasks()

    # Iterates over each task in the task_list ans display its details.
    for index, t in enumerate(task_list, start=1):
        disp_str = f"Task Number: \t {index}\n"
        disp_str += f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"

        # Print the tasks details.
        print(disp_str)

""" 
The view_mine() function allow the users to view 
all the tasks that have been assigned to them.
"""
def view_mine(curr_user):
    task_list = read_tasks()

    # Check if the task_list is empty. 
    if not task_list:
        print("You don't have any task assigned yet.")
        return
    
    # Create a dictionary to store task indices as keys and tasks as values.
    task_dict = {}
    # Iterate over each task in the task_list and populate the task_dict.
    for index, t in enumerate(task_list, start=1):
        task_dict[index] = t

        # Check if the current task is assigned to the current user.
        if t['username'] == curr_user:
            # Prepare the string to display the task details.
            disp_str = f"Task Number: \t {index}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            # Print the above task details.
            print(disp_str)

    # Continue asking for user input until -1 is entered.
    while True:      
        task_choice = input("Please enter -1 to return to the main menu or enter the task number to edit: ")
        if task_choice == "-1":
            return
        try:
            task_choice = int(task_choice)
            # Check if the chosen task exists in the task_dict.
            if task_choice in task_dict:
                chosen_task = task_dict[task_choice]
                print(chosen_task)

                while True:
                    edit_choice = input("Enter 'm' to mark the task as complete, 'e' to edit the task, or '-1' to go back: ")
                    # Check if the user wants to mark the task as complete.
                    if edit_choice == "m":
                        # Check is the task is not already marked as complete
                        if not chosen_task['completed']:
                            chosen_task['completed'] = True
                            write_tasks(task_list)  # Write the updated task list to the "tasks.txt" file
                            print("Task marked as completed.")
                        else:
                            print("Task is already marked as complete.")
                        break
                    # Check if the user wants to edit the task.
                    elif edit_choice == "e":
                        # Check if the task is not already marked as complete.
                        if not chosen_task['completed']:
                            new_username = input("Enter new username (leave empty to keep the current username): ")
                            if new_username:
                                username_password = read_username_password()
                                if new_username not in username_password:
                                    print("User does not exist. Please enter a valid username.")
                                    continue
                                chosen_task['username'] = new_username

                            new_due_date = input("Enter new due date (YYYY-MM-DD) (leave empty to keep the current due date): ")
                            if new_due_date:
                                try:
                                    due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                                    chosen_task['due_date'] = due_date_time
                                except ValueError:
                                    print("Invalid datetime format. Please use the format specified.")
                                    continue

                            write_tasks(task_list)
                            print("Task updated successfully.")
                        else:
                            print("Cannot edit a completed task.")
                        break
                    # Check if the user wants to go back.
                    elif edit_choice == "-1":
                        break

                    else:
                        print("Invalid option. Please try again.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Invalid input. Please enter a number")     

""" 
The function "display_stats" provides a summary 
of the current state of the task management system 
by showing the number of users and the number of tasks.
"""
def display_stats():
    username_password = read_username_password()
    task_list = read_tasks()
    num_users = len(username_password.keys())
    num_tasks = len(task_list)
    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")

def read_username_password():
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")
    # Create an empty dictionary to store username-password pairs. 
    username_password = {}
    # Iterate over each line of user data and extract the username and password.
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    return username_password

def write_username_password(username_password):
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_password:
            user_data.append(f"{k};{username_password[k]}")
        out_file.write("\n".join(user_data))
"""
With login() function we can authenticate user by verifying
their entered username and password against the stored 
credentials in the user.txt file. It ensures that users
with the correct credentials are allowed to log in to the 
task management system.
"""
def login():
    username_password = read_username_password()
    while True:
        curr_user = input("Username: ")
        curr_pass = input("Password: ")

        # Check if the entered user name already exist. 
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        # Check if the entered password matches the password associated with the entered user name.
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            return curr_user

"""
The generate_reports() function perfoms calculations and 
is responsible for analyzing the task user and data, generating
comprehensive reports with various statistics, and saving those 
reports in separate text files for future reference and analysis.
This function can be only accessed by the admin login. 
"""
def generate_reports():
    tasks = read_tasks()
    users = list(read_username_password().keys())
    
    # Calculate task-related statistics.
    total_tasks = len(tasks)
    completed_tasks = sum(task["completed"] for task in tasks)
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(task["due_date"] < datetime.now() and not task["completed"] for task in tasks)
    
    # Generate task report.
    task_report = f"Total tasks: {total_tasks}\n" \
                  f"Completed tasks: {completed_tasks}\n" \
                  f"Uncompleted tasks: {uncompleted_tasks}\n" \
                  f"Overdue tasks: {overdue_tasks}\n" \
                  f"Percentage of incomplete tasks: {uncompleted_tasks / total_tasks * 100:.2f}%\n" \
                  f"Percentage of overdue tasks: {overdue_tasks / total_tasks * 100:.2f}%"
    
    # Generate user- related statistics.
    user_report = f"Total users: {len(users)}\n" \
                  f"Total tasks: {total_tasks}\n"

    for user in users:
        assigned_tasks = sum(task["username"] == user for task in tasks)
        completed_assigned_tasks = sum(task["username"] == user and task["completed"] for task in tasks)
        uncompleted_assigned_tasks = assigned_tasks - completed_assigned_tasks
        overdue_assigned_tasks = sum(
            task["username"] == user and task["due_date"] < datetime.now() and not task["completed"]
            for task in tasks
        )

        user_report += f"\nUser: {user}\n" \
                       f"Total tasks assigned: {assigned_tasks}\n"

        if assigned_tasks != 0:
            percentage_assigned = assigned_tasks / total_tasks * 100
            percentage_completed = completed_assigned_tasks / assigned_tasks * 100
            percentage_uncompleted = uncompleted_assigned_tasks / assigned_tasks * 100
            percentage_overdue = overdue_assigned_tasks / assigned_tasks * 100

            user_report += f"Percentage of tasks assigned: {percentage_assigned:.2f}%\n" \
                           f"Percentage of completed tasks: {percentage_completed:.2f}%\n" \
                           f"Percentage of uncompleted tasks: {percentage_uncompleted:.2f}%\n" \
                           f"Percentage of overdue tasks: {percentage_overdue:.2f}%"
        else:
            user_report += "No tasks assigned.\n"
    
    # Write task report to a text file.
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(task_report)

    # Write user report to a file.
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(user_report)

    print("Reports generated successfully. Look for the text files (reports) on your computer.")

"""
This function acts as the central control hub, allowing user interaction,
excecuting requested actions, and managing the overall flow of the program. 
"""
def main():
    curr_user = login()

    while True:
        # Display the main menu and prompt the user for a menu option. 
        print()
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
ds - Display statistics
gr - Generate reports
e - Exit
: ''').lower()
        # Execute the corresponding action based on the selected menu option.
        if menu == 'r':
            reg_user()

        elif menu == 'a':
            add_task()

        elif menu == 'va':
            if curr_user != "admin":
                print("Please log in as an admin.")
            else:
                view_all()

        elif menu == 'vm':
                view_mine(curr_user)

        elif menu == 'ds':
            if curr_user != 'admin':
                print("Please log in as an admin.")
            else:
                display_stats()

        elif menu == 'gr':
            if curr_user != 'admin':
                print("Only admin is allow to access this function.")
            else:
                generate_reports()

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice. Please try again.")

if __name__ == "__main__":
    main()

"""
- In order to code my program I had to implement what I have learned in previous
modules in the course. 

- I read again all of the support material from previous tasks in order to achieve
a deeper understanding of the course content. 
- I want to thanks all the mentors that helped me with this tasks and guided me 
through it.

- Once again the book "In easy steps. Python" by Mike McGrath was a valuable source 
of information that helped me with problem solving and to understand in a deeper level 
how Python operates in a logical level.

-Note: if you want to see an updated version of "task_overview" and "user_overview" you will
need to log-in as an admin and select the option "gr" from the menu. (To see the report after
a new user or a need taks were added.)

- Conding and modifying this Capstone Project II was not an easy task and it took me 
several trial and error attempts; I am proud of my program because I learned so much 
from it during the coding process of designed it and make it work properly with the task's
specified steps. I really tried my best. Thank you :)

Bárbara Guerra Palenzuela. 

"""
