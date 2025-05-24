# Master_Class: Intelligent Student Grouping System

## Overview

**Master_Class** is a Python-based application designed to optimize student groupings into balanced classes. Leveraging graph theory and clustering algorithms, it considers student friendships, academic performance, and behavioral traits to create well-balanced classroom assignments. The system aims to enhance student well-being and academic success by fostering supportive peer relationships and balanced learning environments.

## Features

- **Friendship Graph Construction**: Models student friendships as a graph to identify mutual connections.
- **Clustering Algorithms**: Groups students based on friendship clusters and compatibility.
- **Balanced Class Partitioning**: Distributes students into classes, ensuring diversity in academic and behavioral attributes.
- **Database Integration**: Utilizes a database to store and manage student information and grouping results.
- **Web Interface**: Provides a user-friendly web interface for data input and visualization of class assignments.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/shirzzz/Master_Class.git
   cd Master_Class
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare the Database**:
   - Ensure the database is set up and accessible.
   - Populate the database with student data, including names, academic scores, behavioral traits, and friendship preferences.

2. **Run the Grouping Script**:
   ```bash
   python students_to_classes_with_DB.py
   ```
   - This script will process the student data, apply clustering algorithms, and assign students to balanced classes.

3. **Access the Web Interface**:
   - Navigate to the `web` directory:
     ```bash
     cd web
     ```
   - Start the web server:
     ```bash
     python app.py
     ```
   - Open your web browser and go to `http://localhost:5000` to interact with the application.

## Project Structure

```
Master_Class/
├── db/
│   └── ...           # Database files and configurations
├── web/
│   ├── app.py        # Flask web application
│   ├── templates/    # HTML templates
│   └── static/       # CSS, JS, and image files
├── students_to_classes_with_DB.py  # Main script for student grouping
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

## Dependencies

- Python 3.x
- Flask
- pandas
- numpy
- networkx
- SQLAlchemy
- All dependencies listed in `requirements.txt`

## Future Enhancements

- Incorporate gender balance considerations into the grouping algorithm.
- Develop an admin panel for easier data management and monitoring.
- Implement advanced analytics to assess the effectiveness of class groupings.
- Expand the system to accommodate larger school districts or national education systems.

## Contributors

- Tal Rojansky
- Hila Perry
- Shir Zadok
- Yahav Marom

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
