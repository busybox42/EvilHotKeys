# EvilHotKeys

EvilHotKeys is a Python script that allows you to automate key presses for various games.  It's intent for me is to replace AutoHotKey as python is compatible on multiple operating systems.

## Installation

1. Clone the repository: `git clone https://github.com/your-username/EvilHotKeys.git`
2. Install the required packages: `pip install -r requirements.txt`

## Usage

1. Navigate to the `EvilHotKeys` directory.
2. Run the script: `python main.py`
3. Follow the on-screen instructions to select a game and a spec.
4. The script will start running the selected spec. Press `Ctrl+C` to stop the script.

## Adding a new game

1. Create a new directory for the game in the `games` directory.
2. Create a `specs` directory inside the game directory.
3. Create a new Python file for each spec in the `specs` directory.
4. Implement the spec logic in the Python file.


## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature-branch`
3. Make your changes and commit them: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-feature-branch`
5. Create a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.