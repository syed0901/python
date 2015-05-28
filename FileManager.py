__author__ = 'SRIZVI'
#File Manager copies the files in the particular directories as per the file's extensions
import os
import sys
import shutil

def file_manage(des, path,ext):
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames if
              os.path.splitext(f)[1] == ext]
    for file_name in result:
        if not os.path.isfile(des + "\\" + os.path.basename(file_name)):
            shutil.copy(file_name, des)


def create_output_dir(name):
    if not os.path.exists("C:\\"+name):
        os.makedirs("C:\\"+name)
    return "C:\\"+name

def main():
    if len(sys.argv) == 1:
        print("This program requires at least one parameter")
        sys.exit(1)
    create_output_dir("MainRepository")
    des_doc = create_output_dir("MainRepository\\docs")
    des_txt = create_output_dir("MainRepository\\txts")
    des_pdf = create_output_dir("MainRepository\\pdfs")
    des_ppt = create_output_dir("MainRepository\\ppts")
    des_jar = create_output_dir("MainRepository\\jars")
    des_xls = create_output_dir("MainRepository\\xlsx")
    des_msg = create_output_dir("MainRepository\\mails")

    for path in sys.argv:
        if os.path.isdir(path):
            file_manage(des_txt, path, '.txt')
            file_manage(des_doc, path, '.doc')
            file_manage(des_doc, path, '.docx')
            file_manage(des_pdf, path, '.pdf')
            file_manage(des_ppt, path, '.ppt')
            file_manage(des_ppt, path, '.pptx')
            file_manage(des_jar, path, '.jar')
            file_manage(des_xls, path, '.xlsx')
            file_manage(des_msg, path, '.msg')
if __name__ == '__main__':
    main()
