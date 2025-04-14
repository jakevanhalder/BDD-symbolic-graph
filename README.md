# BDD-symbolic-graph

## Project Overview
A python program designed to verify that for each node u in [prime], there exists a node v in [even] such that u can reach v in a positive even number of steps.

The key technologies include:

* **Python**: The primary programming language for the project.
* **Pyeda**: A library used for electronic design automation which provides the tools to work with Boolean expressions and Binary Decision Diagrams.

## Development Setup
This section guides developers on how to set up, configure, and run the application.

### Prerequisites
1. **Install Python**: Download and install [Python](https://www.python.org/downloads/)
2. **Install VS Code**: Download and install [VS Code](https://code.visualstudio.com/).
3. **Clone Repository**:
```bash
git clone https://github.com/jakevanhalder/BDD-symbolic-graph.git
cd BDD-symbolic-graph
```

### Usage
1. **Create and Activate Venv**: Run the following commands to create and activate python venv
```bash
# Create the virtual environment
python -m venv venv

# On Windows, activate the venv
venv\Scripts\activate

# On macOS/Linux, activate the venv
source venv/bin/activate
```
2. **Install Required Packages**:
```bash
# Install from the requirements.txt file
pip install -r requirements.txt

# Otherwise, install Pyeda directly:
pip install pyeda
```
3. **Run Program**: Run the python program with the following command:
```bash
python projectBDD.py
```

## Additional Notes
* This project was built in a Windows environment and hasn't been tested on other operating systems.
* If you run into any dependency issues or bugs, consider checking the [Pyeda](https://pyeda.readthedocs.io/en/latest/index.html) documentation for troubleshooting tips.
