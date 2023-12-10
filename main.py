from image_loader import ImageLoader
from sys import argv

def main():
    app = None
    if len(argv) == 2:
        app = ImageLoader(argv[1])
    else:
        app = ImageLoader('')
    app.mainloop()

if __name__ == '__main__':
    main()