from lib.FileHandler import FileHandler
def __init__():
    words = ["ar","en","nullable","success","title_ar","title_en","description",\
             "description_en","description_ar","favorites","=","user_id","place_id","title","user_id"\
                ,"keywords","status","title_ar","id"\
                'bookid' ,'order_number','date','booking_title','company_title','taxno',\
                'address','image','date_of_arrival','departure_date','num_nights','count','star5',\
                'total_price','price','saved','commission','tax','status_book','access_time','leave_time','paymentmethod_icon',\
                'paymentmethod_name','numinvoices','invoice_created_at','invoiceId']
    fun_laravel = ["view","middleware","validate","create","compact","insert","update",\
           "trans","translate","__","where","route","whereRaw","selectRaw","make",\
            "select","raw","orderBy","format"]
    fun_laravel_blade = ["view","middleware","validate","create","compact","insert","update",\
           "trans","translate","__","where","route","whereRaw","selectRaw","make",\
            "select","raw","orderBy","format","if","error","can","canany","content","push"\
                ,"yiled","section"]
    search_words =["/","{{","}}",">","<","alert","fa-","text-","col ","content-"\
                   ,"row-","row ","col-"]
    # fun = ["validate"]
    # obj = FileHandler("/work/sites/insta-prop/app/Http",words,fun_laravel)
    # obj.run()
    obj = FileHandler("/work/sites/insta-prop/resources/views",words,fun_laravel_blade,search_words)
    obj.run_blade()
    # handler.get_files()
__init__()