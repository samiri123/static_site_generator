from copy_static import copy_static
from generate_page import generate_pages_recursive
import sys

def main():
    copy_static()
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    generate_pages_recursive( basepath, './content', './template.html', './docs')
    
    

if __name__ == "__main__":
    main()
