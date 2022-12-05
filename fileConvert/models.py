from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from pdf2image import convert_from_path
from django.conf import settings
import os


# Create your models here.
COVER_PAGE_DIRECTORY = 'coverpage/'
PDF_DIRECTORY = 'pdf/'
COVER_PAGE_FORMAT = 'jpg'

# this function is used to rename the pdf to the name specified by filename field
def set_pdf_file_name(instance, filename):
    return os.path.join(PDF_DIRECTORY, '{}.pdf'.format(instance.filename))

# not used in this example
def set_cover_file_name(instance, filename):
    return os.path.join(COVER_PAGE_DIRECTORY, '{}.{}'.format(instance.filename, COVER_PAGE_FORMAT))

class Pdffile(models.Model):
    # validator checks file is pdf when form submitted
    pdf = models.FileField(
        upload_to=set_pdf_file_name, 
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
        )
    filename = models.CharField(max_length=20)
    pagenumforcover = models.IntegerField()
    coverpage = models.FileField(upload_to=set_cover_file_name)

def convert_pdf_to_image(sender, instance, created, **kwargs):
    if created:
        # check if COVER_PAGE_DIRECTORY exists, create it if it doesn't
        # have to do this because of setting coverpage attribute of instance programmatically
        cover_page_dir = os.path.join(settings.MEDIA_ROOT, COVER_PAGE_DIRECTORY)

        if not os.path.exists(cover_page_dir):
            os.mkdir(cover_page_dir)

        # convert page cover (in this case) to jpg and save
        cover_page_image = convert_from_path(
            pdf_path=instance.pdf.path,
            dpi=200, 
            first_page=instance.pagenumforcover, 
            last_page=instance.pagenumforcover, 
            fmt=COVER_PAGE_FORMAT, 
            output_folder=cover_page_dir,
            )[0]

        # get name of pdf_file 
        pdf_filename, extension = os.path.splitext(os.path.basename(instance.pdf.name))
        new_cover_page_path = '{}.{}'.format(os.path.join(cover_page_dir, pdf_filename), COVER_PAGE_FORMAT)
        # rename the file that was saved to be the same as the pdf file
        os.rename(cover_page_image.filename, new_cover_page_path)
        # get the relative path to the cover page to store in model
        new_cover_page_path_relative = '{}.{}'.format(os.path.join(COVER_PAGE_DIRECTORY, pdf_filename), COVER_PAGE_FORMAT)
        instance.coverpage = new_cover_page_path_relative

        # call save on the model instance to update database record
        instance.save()

post_save.connect(convert_pdf_to_image, sender=Pdffile)