#coding:utf-8

import json
import re
from taobaoapi import *

key='12563414'
app_secret='23392965068b9eaf0be13b6c6eeba3ee'




def get_clear_id(url=""):
    """
http://detail.tmall.com/item.htm?id=10580268189&cm_cat=50102173
http://item.taobao.com/item.htm?id=15103075639

    """ 
    if url=="":
        return None
    if not( "taobao.com"  in url or "tmall.com" in url ):
        return None
    s=re.findall('id=(\d+)',url)
    if len(s)==1: 
       return s[0]
    else:
        return None
    



def get_store_detail(num_iid):
  client = TaobaoAPI(key, app_secret)
  num_iid=num_iid
  method='taobao.item.get'
  #fields='detail_url,num_iid,title,nick,type,cid,seller_cids,props,input_pids,input_str,desc,pic_url,num,valid_thru,list_time,delist_time,stuff_status,location,price,post_fee,express_fee,ems_fee,has_discount,freight_payer,has_invoice,has_warranty,has_showcase,modified,increment,approve_status,postage_id,product_id,auction_point,property_alias,item_img,prop_img,sku,video,outer_id,is_virtual'
  fields='pic_url,price,title,nick'
  req = TaobaoRequest(method, fields=fields, num_iid=num_iid)
  source = client.execute(req)
  if s:
    s= source.get("item")
    picurl=s.get("pic_url")
    price=s.get("price")
    name=s.get("title")
    storename=s.get("nick")
    return  (picurl,price,name,storename)
  return None
 
if __name__=='__main__':
 urls=['http://detail.tmall.com/item.htm?id=10580268189&cm_cat=50102173',
'http://item.taobao.com/item.htm?id=15103075639',
'http://item.taobao.com/item.htm?id=14101536938',
'http://item.taobao.com/item.htm?id=14030822983  ']   
 for url in urls:
    iid=get_clear_id(url)
    print get_store_detail(iid)
    
