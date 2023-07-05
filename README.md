# finalCapstone
Name: Capstone Project II - Task_manager_17.

This repository includes the last Capstone Project I coded for my task T17.

Description:

It is a task manager program for a small business written in Python.
A program designed for a small business to manage tasks assigned to each member of a team. 
The program utilizes lists, dictionaries, functions, string handling, error handling, and refactoring concepts.

The code performs the following tasks:

- Imports necessary libraries, such as "os" for file handling and "datetime" for working with date and time.
- Defines a datetime format for string conversion.
- Provides functions to read and write tasks from/to a file called "tasks.txt".
- Implements a function to register a new user by prompting for a username and password, checking for username availability, and updating the user database.
- Implements a function to add a new task by prompting for task details (username, title, description, due date), validating inputs,
  creating a new task dictionary, appending it to the task list, and writing the updated list to the file.
- Implements a function to view all tasks, which reads the task list from the file and displays task details for each task,
  including the task number, title, assigned user, assigned date, due date, and description.
- Implements a function to view tasks assigned to a specific user, which reads the task list,
  checks if the list is empty, create a task dictionary with task indices as keys, displays details for tasks assigned to the current user,
  allows the user to choose a task to edit or mark as complete, and updates the task list accordingly.
- The program includes comments explaining the purpose and functionality of each section of code.
