'''
Copy the contents of README.md to the Github Pages index.md
'''
import time
from tzlocal import get_localzone
from os.path import abspath
from tests.utils.get_element import get_file_as_string


top_copy = '''---
layout: default
---
%s

###### Last Update: %s %s
'''

readme = get_file_as_string('./README.md')


def write_file(my_file, content):
    fq_file = abspath(my_file)
    doc_file = open(fq_file, "w")
    doc_file.write(content)
    doc_file.close()


last_update = time.strftime("%c")
local_timezone = get_localzone()
write_file('./docs/index.md', top_copy % (readme, last_update, local_timezone))