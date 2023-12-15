Dash App for Motion Capture Data Analysis
=========================================

Overview
--------

This Dash application is designed for analyzing and visualizing motion capture data, providing insights into positional and velocity data, error metrics, and comparisons between different motion capture systems.

Key Components
--------------

### Layout

The app layout is divided into three main sections:

*   **Sidebar**: Contains buttons for selecting different markers.
*   **Main Content**: Displays various plots and charts related to motion capture data.
*   **Info Section**: Shows detailed information about the selected marker and includes the save report button.

### Data Management

*   **`MoCapData` Model**: Encapsulates position and velocity data, RMSE, and absolute error dataframes, ensuring a structured and consistent data format.

### Callbacks

Callbacks in Dash drive the interactivity of the app. Here's an overview of the key callbacks:

#### Selected Marker Callback

*   **Purpose**: Manages the selection of markers within the app.
*   **Functionality**:
    *   Stores the name of the selected marker in `dcc.Store`.
    *   Responds to user interactions like clicking on a marker in the graph or a button.
    *   Other callbacks use this stored data to update plots and information cards.

#### Plot Update Callbacks

*   **Purpose**: Dynamically update the trajectory, velocity, and error plots based on the selected marker.
*   **Functionality**:
    *   Retrieves the selected marker's name from `dcc.Store`.
    *   Generates updated plots for the selected marker using the data stored in the `MoCapData` model.

#### Marker Name Callbacks

*   **Purpose**: Updates various components in the UI with the name of the currently selected marker.
*   **Functionality**:
    *   Monitors changes in the selected marker stored in `dcc.Store`.
    *   Updates elements like trajectory labels, error plot labels, etc., with the current marker name.

### Special Components

*   **`dcc.Store`**:
    *   Used to store the name of the currently selected marker.
    *   Placed outside the visible layout components, acting as a silent data holder.
    *   Enables efficient data management and inter-component communication.

### Saving Reports

*   **Save Button**:
    *   Located in the Info Section.
    *   Allows users to save a comprehensive report of the current analysis as an HTML file.
    *   The report includes RMSE and absolute error data, plots, and other relevant information.

### User Interaction

*   **Graphs and Buttons**:
    *   Users can interact with various elements like scatter plots, marker buttons, etc.
    *   These interactions trigger callbacks that update the app's content dynamically.

Usage (not updated)
-----

To run the app:

1.  Ensure all dependencies are installed.
2.  Navigate to the app directory and run `python app.py`.

