# Task Manager App

## Overview
The Task Manager App is a Python-based application designed to provide users with insight into running processes on their system. It displays important process information, such as memory usage, CPU usage, Process ID (PID), and open ports. Users can also terminate unwanted processes directly from the application.

## Features
- Displays a list of currently running processes.
- Shows memory usage, CPU usage, Process ID, and ports for each process.
- Allows users to set a refresh interval for updating the displayed process information (default is 5 seconds).
- Enables users to end a selected task/process.

## System Design
The application consists of the following modules:

1. **main.py**: The entry point of the application that initializes the Tkinter GUI and handles main application logic.
   - **Tasks**:
     - `TaskManagerApp`: Main application class responsible for creating the main window and handling user interactions.
     - `__init__`: Constructor for initializing the application and its components.
     - `start_refresh`: Starts the periodic refresh of the displayed processes based on the user-defined interval.
     - `refresh_tasks`: Fetches the list of running processes and updates the display in the GUI.
     - `end_task`: Terminates a selected process based on the Process ID.

2. **process_utils.py**: Utility module for fetching and managing system processes.
   - **Tasks**:
     - `get_running_processes`: Fetches running processes using `psutil` and returns a list of process information.
     - `terminate_process`: Terminates a process given its Process ID.

3. **gui_components.py**: Module responsible for creating various GUI components and layouts.
   - **Tasks**:
     - `ProcessTable`: Class that creates and manages a table (Treeview) to display process information.
     - `__init__`: Constructor for initializing the table with column headers.
     - `update_table`: Updates the table with new data fetched from the process manager.
     - `clear_table`: Clears the current data in the table.

4. **config.py**: Configuration module for storing application settings, such as the default refresh interval.
   - **Tasks**:
     - `DEFAULT_REFRESH_INTERVAL`: Constant that holds the default refresh interval in seconds.

## Installation
To run this application, ensure you have Python installed along with the required libraries. You can set up the environment using the following steps:

1. Clone the repository:
   ```
   git clone <repository_url>
   cd task-manager-app
   ```

2. Install the required packages:
   ```
   pip install psutil tkinter
   ```

## Usage
1. Run the application:
   ```
   python main.py
   ```

2. The Task Manager App will display a window with a list of running processes and their details.
3. To end a task, select it from the list and click the 'End Task' button.
4. You may adjust the refresh interval for the process list as needed (default is 5 seconds).

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! Please submit issues or pull requests to improve the functionality or documentation of the application.