from lib.FileHandler import FileHandler
def __init__():
    words = ["ar","en","nullable","description","description_en","description_ar","favorites","=","user_id","place_id","title","user_id","keywords","status"]
    fun = ["view","middleware","create","compact","insert","update","trans","translate","__","where","route"]
    FileHandler("/work/sites/insta-prop/app/Http/Controllers",words,fun)
    # handler.get_files()
__init__()