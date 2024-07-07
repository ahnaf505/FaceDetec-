<p align="center">
  <a>
    <img src="src/FaceDetec-logo.png" alt="Logo" width=150 height=150>
  </a>
</p>

## 
FaceDetec is a cutting-edge project aimed at precise face similarity detection and analysis.

## 🔍 Features

- **Command Line Interface**: Built with `colorama` for better interaction.
- **Deeface Library Integration**: Harnesses advanced facial recognition capabilities.
- **MediaPipe Library Integration**: Integrating advanced facial contour detection capabilities.
- **Facial Feature Extraction**: Identifies eyes 👀, nose 👃, and mouth 👄 for manual review.
- **HTML Report Generation**: Automatically generates detailed reports for analyzed faces.

## 🚀 Status

FaceDetec is currently usable for production in a CLI-only mode. Stay tuned for upcoming releases to leverage the full functionality of FaceDetec. Contributions and feedback are welcome as we work towards a GUI mode.

## 📝 Usage

**Python Project Setup Guide**

This guide will help you set up and run 'FaceDetec'' on your machine.

### Prerequisites

- Python installed on your machine (version 3.9 or higher is recommended).
- `pip` (Python package installer) installed.

#### Step 1: Clone the Project Repository

1. Open a terminal or command prompt.
2. Navigate to the directory where you want to clone the project.
3. Run the following command to clone the repository (replace `repository_url` with the actual URL of your project repository):

    ```sh
    git clone https://github.com/ahnaf505/FaceDetec-.git
    ```

4. Navigate into the FaceDetec- directory

#### Step 2: Create a Virtual Environment (Optional but recommended)

1. Run the following command to create a virtual environment (replace `venv` with your preferred environment name):

    ```sh
    python -m venv venv
    ```

2. Activate the virtual environment:

    - On Windows:

        ```sh
        .\venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```sh
        source venv/bin/activate
        ```

#### Step 3: Install the Requirements

1. Ensure you are in the project directory.
2. Run the following command to install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

#### Step 4: Run the app.py

1. Run the main Python file 'app.py':

    ```sh
    python app.py
    ```

2. Press 'enter' and input the path for the first and second image.
3. Wait to make sure there's no error until the report is generated
4. Congrats! you have made a face comparison report with **FaceDetec'**

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

© Ahnaf | ahnaf505/FaceDetec-
