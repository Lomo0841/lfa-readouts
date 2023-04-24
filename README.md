# LFA Readouts

## Setup

1. Install Python 3 from the [official website](https://www.python.org/downloads/).
2. Install the following dependencies using pip:

   ```
   pip3 install flask opencv-contrib-python pupil-apriltags
   ```

3. Navigate to the Git project folder:

   ```
   cd lfa-readouts
   ```

4. Install the project package using pip:

   ```
   pip3 install -e ./lfa_readouts_package
   ```

## Usage

To start the web application, run the following command:

- For Windows:

  ```
  py ./lfa_readouts_package/lfa_project/Frontend/app.py
  ```

- For Unix/macOS:

  ```
  python3 ./lfa_readouts_package/lfa_project/Frontend/app.py
  ```

This will start the Flask development server on `http://localhost:5000`. Open a web browser and navigate to this URL to access the application.
