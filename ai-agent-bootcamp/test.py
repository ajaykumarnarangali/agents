from functions.get_file_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def main():
    working_dir = "calculator"

    # file info test cases 
    # root_content=get_files_info(working_dir)
    # print("root content:",root_content)

    # pkg_content=get_files_info(working_dir,"pkg")
    # print("pkg content:",pkg_content)

    # non_exist=get_files_info(working_dir,"test")
    # print("non existant folder",non_exist)

    # read funtion test cases
    # backtrack_folder=get_files_info(working_dir,"../")
    # print("back track folder test",backtrack_folder)

    # lorem_file = get_file_content(working_dir, "lorem.txt")
    # print("lorem content:", lorem_file)

    # missing_file = get_file_content(working_dir, "missing.py")
    # print("Missing file:", missing_file)

    # directory = get_file_content(working_dir, "pkg")
    # print("Directory test:", directory)
    
    # write funciotn test cases
    # dummy_content = (
    #     "The hospital management system provides a centralized platform for managing hospital"
    #     " information, doctors, patients, appointments, departments, and medical services."
    # )

    # write_outer_workingdir = write_file(
    #     working_dir, "../../dummy_content.txt", dummy_content
    # )
    # print(write_outer_workingdir)

    # success_full_write = write_file(
    #     working_dir, "pkg/dummy.txt", dummy_content
    # )
    # print(success_full_write)

    out_put=run_python_file("calculator","test.py")
    print(out_put)


main()
