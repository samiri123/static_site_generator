from copy_static import copy_static
from generate_page import generate_pages_recursive
import sys

def main():
    copy_static()
    basepath = sys.argv[0]
    if basepath == "":
        basepath = "/"
    generate_pages_recursive( '/', 'content', './template.html', 'docs')
    
    

if __name__ == "__main__":
    main()
