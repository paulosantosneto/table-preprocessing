# Table Preprocessing

The objective is to perform pre-processing on documents that contain tables, performing rotations and noise removal. In this way, it is possible to improve the results of detection and structural recognition of tables even for large tabular extraction models.

# Instalation

Create a virtual environment.
```
virtualenv venv
```
Activate the virtual environment.
- Linux
```
source venv/bin/activate
```
- Windows
```
venv/Scripts/Activate
```
Install the necessary dependencies.
```
pip install -r requirements.txt
```

# Main functionality
The main function allows you to do bulk pre-processing. In it, it is possible to select the source directory with the images to be pre-processed, as well as the destination directory. In addition, you can select from the available methods: rotation and denoise.

- Run the main file.
```
python main.py --methods rotation noise --data_root testdataset --data_output testoutput
```

# Test with streamlit

To use the application with [streamlit](https://streamlit.io), run the 'app.py' file. The application aims to demonstrate the results of pre-processing by image.