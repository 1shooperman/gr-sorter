''' page_utils.py '''
import os

from sorter.lib.data_handler import store_data, dump_data
from sorter.lib.parse_xml import parse
from sorter.lib.bootstrap import bootstrap
from sorter.lib.sorter_logger import sorter_logger

LOGGER = sorter_logger(__name__)

def page_loop(xml_data, db_name, new_data=False):
    ''' retrieving and storing multipage data '''
    filtered_data = parse(xml_data)

    db_file = os.path.abspath(db_name)

    if new_data is True:
        dump_data(db_file)
        bootstrap(db_name, LOGGER)

    store_data(filtered_data, db_file)
