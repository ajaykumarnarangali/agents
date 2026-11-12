from functions.get_file_info import get_files_info

def main():
   working_dir="calculator"

   root_content=get_files_info(working_dir)
   print("root content:",root_content)

   pkg_content=get_files_info(working_dir,"pkg")
   print("pkg content:",pkg_content)

   non_exist=get_files_info(working_dir,"test")
   print("non existant folder",non_exist)

   backtrack_folder=get_files_info(working_dir,"../")
   print("back track folder test",backtrack_folder)

main()