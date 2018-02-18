from imagecluster import main
import os

# main.main(r"C:\Eamon\Python Studies\Pinterest_scraper\abyssinian_search", sim=0.5)
# main.main(r"C:\Eamon\Python Studies\Pinterest_scraper\bsh_search", sim=0.5)
# main.main(r"C:\Eamon\Python Studies\Pinterest_scraper\rex_sphinx_search", sim=0.5)
# main.main(r"C:\Eamon\Python Studies\Pinterest_scraper\bengal_search", sim=0.5)
# main.main(r"C:\Eamon\Python Studies\Pinterest_scraper\maine_coon_search", sim=0.5)


def rm_from_dir(target_dir, sym_dir):
    """
    removes all files from dir using the files in sym_dir as a reference
    :param target_dir:
    :param sym_dir:
    :return:

    """

    images = [os.path.join(target_dir, image) for image in os.listdir(sym_dir)]

    for image in images:
        os.unlink(image)


def rm_from_dir_deep(target_dir, sym_dir):
    gen = os.walk(sym_dir)
    for i in gen:
        if not i[-1] == []:
            rm_from_dir(target_dir, i[0])
