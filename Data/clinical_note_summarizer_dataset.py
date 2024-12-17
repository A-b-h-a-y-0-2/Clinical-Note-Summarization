# -*- coding: utf-8 -*-
"""Clinical note summarizer dataset.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VgySdhJD-LR0h1BEpA1WHZffaJg5WPZL
"""

# Commented out IPython magic to ensure Python compatibility.
# %cd data-for-clinical-note-summarizer

!wget ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_noncomm/xml/oa_noncomm_xml.PMC001xxxxxx.baseline.2024-06-18.tar.gz
!wget ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_noncomm/xml/oa_noncomm_xml.PMC002xxxxxx.baseline.2024-06-18.tar.gz
!wget ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_noncomm/xml/oa_noncomm_xml.PMC003xxxxxx.baseline.2024-06-18.tar.gz

from google.colab import drive
drive.mount('/content/drive')

!cp -r /content/data-for-clinical-note-summarizer /content/drive/MyDrive/data-for-clinical-note-summarizer/

!mkdir /content/drive/MyDrive/data-for-clinical-note-summarizer