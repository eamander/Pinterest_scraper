from imagecluster import main
import os

main.main(r"C:\Eamon\Python Studies\Pinterest_scraper\abyssinian_search", sim=0.5)


def rm_from_dir(dir, sym_dir):
    """
    removes all files from dir using the files in sym_dir as a reference
    :param dir:
    :param sym_dir:
    :return:

    """

    images = [os.path.join(dir, image) for image in os.listdir(sym_dir)]

    for image in images:
        os.unlink(image)


def rm_from_dir_deep(dir, sym_dir):
    gen = os.walk(sym_dir)
    for i in gen:
        if not i[-1] == []:
            rm_from_dir(dir, i[0])
