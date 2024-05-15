import streamlit as st

import base64

import os

from reportlab.platypus import SimpleDocTemplate, Image, PageBreak
from reportlab.lib.pagesizes import A4, landscape


from PIL import Image as pilImage

__allow_type = [".jpg", ".jpeg", ".bmp", ".png"]

__rootDir = ""


def convert_images2PDF_one_dir(file_dir, save_name="1.pdf", filename_sort_fn=None):
    book_pages = []

    for file_path in file_dir:

        # 是否图片
        if __isAllow_file(file_path):
            book_pages.append(file_path)


    if len(book_pages) > 0:

        __converted(save_name, book_pages, filename_sort_fn)



def __isAllow_file(filepath):

    if filepath and (os.path.splitext(filepath)[1] in __allow_type):
        return True

    return False


def __converted(save_book_name, book_pages=None, ):

    if book_pages is None:
        book_pages = []
    __a4_w, __a4_h = landscape(A4)



    bookPagesData = []

    bookDoc = SimpleDocTemplate(save_book_name, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72,
                                bottomMargin=18)

    for page in book_pages:

        img_w, img_h = ImageTools().getImageSize(page)


        if __a4_w / img_w < __a4_h / img_h:
            ratio = __a4_w / img_w
        else:
            ratio = __a4_h / img_h

        data = Image(page, img_w * ratio, img_h * ratio)
        bookPagesData.append(data)
        bookPagesData.append(PageBreak())

    try:
        bookDoc.build(bookPagesData)
    except Exception as err:
        print("[*] Exception >>>> ", err)


class ImageTools:
    def getImageSize(self, imagePath):
        img = pilImage.open(imagePath)
        return img.size


def get_binary_file_downloader_html(bin_file, file_label='file'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
    return href


def show_pdf_download_link(save_url, save_name, font_size=18, is_title=False):
    if save_url and os.path.exists(save_url):
        if is_title:
            pdf_download_link = get_binary_file_downloader_html(save_url, f'{save_name}')
            st.markdown(f'<p style="font-size:{font_size}px;text-align:center;">{pdf_download_link}</p>',
                        unsafe_allow_html=True)
        else:
            pdf_download_link = get_binary_file_downloader_html(save_url, f'{save_name}.PDF')
            st.markdown(f'<p style="font-size:{font_size}px;text-align:center;">{pdf_download_link}</p>',
                        unsafe_allow_html=True)
        return pdf_download_link
    return ""




def img2pdf(images, username, save_name):
    if "pdf_download_link" not in st.session_state:
        st.session_state["pdf_download_link"] = ""
    save_dir = os.path.join("pdf", username)
    save_url = os.path.join(save_dir, f"{save_name}.pdf")
    images = [image for image in images if image]
    os.makedirs(save_dir, exist_ok=True)
    convert_images2PDF_one_dir(images, save_url)

    return save_url,save_name
