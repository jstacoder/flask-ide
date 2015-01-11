import os

def get_files(dirname,exclude):
    data = os.walk(dirname)
    rtn = {}
    for dn,dl,fl in data:
        if dn in exclude:    
            pass
        else:
            dn = os.path.abspath(dn)
            if all(map(lambda x: x not in dn,exclude)):
                rtn[dn] = fl
    return rtn

if __name__ == "__main__":
    from pprint import pprint
    pprint(get_files(os.getcwd(),exclude=['static','ckeditor','.git']),indent=2)
