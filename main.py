from preprocessing import Methods
import argparse
import os

def find_files(dir_root):
    
    data_dir = os.getcwd() + '\\' + dir_root + '\\'

    name_files = []
    path_files = []

    for dir, sub, files in os.walk(data_dir):
        
        for file in files:
            path_files.append(data_dir + file)
            name_files.append(file)
    
    return path_files, name_files

def run_processing(path_files, name_files, output_dir, methods):
    
    m = Methods()
    m.run_methods(methods)
    m.run(path_files, name_files, output_dir)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog = "HelpTables", 
    description = "This program helps other table detection models by applying some pre-processing methods.")
    parser.add_argument("-dr", "--data_root", required = False, default = "testdataset", help = "Choose data root directory. Default directory is 'dataset'.")
    parser.add_argument("-m", "--methods", nargs="+", required = False, default = "rotation", help = "Select methods: rotation, noise. By default, no methods are preselected.")
    parser.add_argument("-do", "--data_output", required = False, default = "testoutput", help = "Choose data output directory. Default directory is 'output'.")
    arguments = parser.parse_args()

    path_files, name_files = find_files(arguments.data_root)
    
    run_processing(path_files, name_files, os.getcwd() + '\\' + arguments.data_output + '\\', arguments.methods)
