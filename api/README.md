# Development Setup for API

This project is built using [FastAPI](https://fastapi.tiangolo.com/). It uses Python 3.12.6, `black` for code formatting, and `isort` for import sorting.

## Prerequisites

- [Python 3.12.6](https://www.python.org/downloads/release/python-3126/)
- [Pyenv](https://github.com/pyenv/pyenv) (Optional but recommended for managing Python versions)
- [VSCode](https://code.visualstudio.com/) (Optional, for development)

## Step 1: Set Up Virtual Environment

1. Create and activate virtual environment for the project. You can check out `pyenv` for more information on how to do that.

2. Install requirements

   ```bash
   pip install -r requirements.txt
   ```

## Step 3: Set Up VSCode for Development (Optional)

If you're using VSCode, follow these steps for a better development experience:

1. Install the Python extension:

   Open VSCode and install the Python, Black and Isort extensions from the marketplace. In VSCode, press Ctrl+P, then type:

   ```bash
   ext install ms-python.python

   ext install ms-python.black-formatter

   ext install ms-python.isort
   ```
