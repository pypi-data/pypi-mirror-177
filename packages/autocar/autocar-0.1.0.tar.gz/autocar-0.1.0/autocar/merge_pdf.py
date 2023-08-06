try:
    from PyPDF2 import PdfFileMerger
    import os
    import warnings
    import re
except ModuleNotFoundError:
    print('Ensure all dependencies are installed.')
    _ = input('Press Enter to exit')
    exit()

# Ignore warnings
warnings.filterwarnings('ignore')

# Input
user_name = input('Please enter your initials\n')

index_names = ['batch', 'index', 'cover', 'start']
pdfs = []
current_dir = os.path.dirname(os.path.realpath(__file__))
directory = os.fsencode(current_dir)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith('.pdf') or filename.endswith('.PDF'):
        if any(_ in filename.lower() for _ in index_names):
            index = filename
        else:
            pdfs.append(filename)

pdfs.sort()
try:
    pdfs.insert(0, index)
    list_index = re.findall(r'\d+', index)
    str_index = ''.join(list_index)
    result = user_name + ' ' + str_index + '.pdf'
except NameError:
    result = 'Merged.pdf'
merger = PdfFileMerger()
try:
    for pdf in pdfs:
        merger.append(pdf)

    merger.write(result)
    merger.close()
except Exception:
    _ = input('Error: There is a problem with a file you are trying to Merge')

_ = input('Complete! Press Enter to exit')
