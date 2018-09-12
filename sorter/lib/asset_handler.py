''' asset_handler.py '''
import os

def asset(asset_path):
    '''
    Get the file contents and header_type
    return (file contents as string, headers)
    '''
    asset_file = os.path.abspath(asset_path)
    if os.path.isfile(asset_file) is True:
        if '.js' in asset_path:
            header_type = 'application/javascript; charset=utf-8'
        elif '.css' in asset_path:
            header_type = 'text/css; charset=utf-8'
        else:
            header_type = 'text/plain; charset=utf-8'

        with open(asset_file, 'r') as myfile:
            data = myfile.read()

        myfile.close()
    else:
        data = None
        header_type = 'text/plain; charset=utf-8'

    return (data, header_type)
