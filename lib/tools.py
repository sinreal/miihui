#coding:utf-8

#some tools

from PIL import Image

storelist={
"tuan.baidu.com": "百度团购",
"taobao.com": "淘宝网",
"tmall.com": "淘宝商城",
"360buy.com": "京东商城",
"dangdang.com": "当当网",
"amazon.cn": "卓越网",
"china.alibaba.com": "阿里巴巴",
"paipai.com": "拍拍网",
"m18.com": "麦考林",
"zhekou.hao123.com": "hao123折扣",
"vancl.com": "凡客诚品",
"fclub.cn": "聚尚网",
"shishangqiyi.com": "时尚起义",
"yintai.com": "银泰网",
"vjia.com": "V+服饰",
"masamaso.com": "玛萨玛索",
"pb89.com": "太平鸟",
"ihush.com": "俏物悄语",
"banggo.com": "邦购网",
"shopin.net": "上品折扣",
"lamiu.com": "兰缪",
"dazhe.cn": "名品打折网",
"yohobuy.com": "有货",
"yaodian100.com": "耀点100",
"vipstore.com": "佳品网",
"suning.com": "苏宁易购",
"gome.com.cn": "国美电器",
"51buy.com": "易迅网",
"coo8.com": "库巴购物网",
"139shop.com": "北斗手机网",
"newegg.com.cn": "新蛋网",
"xiaomi.com": "小米手机官网",
"lusen.com": "绿森数码",
"appserver.lenovo.com.cn/shop": "联想网上商城",
"okbuy.com": "好乐买",
"letao.com": "乐淘",
"yougou.com": "优购网",
"s.cn": "名鞋库",
"mbaobao.com": "麦包包",
"paixie.net": "拍鞋网",
"lafaso.com": "乐蜂网",
"tiantian.com": "天天网",
"sephora.cn": "丝芙网",
"dhc.net.cn": "DHC化妆品",
"jxdyf.com": "金象大药房",
"cn.strawberrynet.com": "草莓网",
"hitao.com": "嗨淘网",
"guopi.com": "果皮网",
"buy.caomeipai.com": "草莓派",
"redbaby.com.cn": "红孩子",
"muyingzhijia.com": "母婴之家",
"leyou.com": "乐友",
"aiyingshi.com": "爱婴室",
"lijiababy.com.cn": "丽家宝贝",
"yihaodian.com": "一号店",
"womai.com": "我买网",
"ocj.com.cn": "东方cj",
"kongfz.com": "孔夫子旧书网",
"quwan.com": "趣玩网",
"happigo.com": "快乐购",
"zbird.com": "钻石小鸟",
"yesmywine.com": "也买酒",
"keede.com.cn": "可得眼镜网",
"binggo.com": "缤购网",
"mogujie.com": "蘑菇街",
"meilishuo.com": "美丽说",
"51fanli.com": "返利网",
"55bbs.com": "55BBS",
"shop.qq.com": "QQ商城",
"kfc.com.cn/kfccda": "肯德基优惠劵",
"youhui.pizzahut.com.cn": "必胜客优惠券",
"eachnet.com": "易趣网",
"egou.com": "易购网",
"fanli.qq.com": "QQ 返利网",
"mizhe.com": "米折网",
"lashou.com": "拉手",
"ju.taobao.com": "聚划算",
"meituan.com": "美团",
"nuomi.com": "糯米网",
"manzuo.com": "满座",
"55tuan.com": "窝窝团",
"t.58.com": "58团购",
"t.dianping.com": "大众点评团",
"etao.com":"一淘",
}



def get_stores():
 data=urllib2.urlopen("http://gouwu.hao123.com/sc/").read()
 links=re.findall("<a href=.*?\/a>",data)
 storelist=[]
 for l in links:
   url=re.findall('//(.*?)/"',l)
   name=re.findall('>(.*?)<',l)
   if len(url)>0:
      if "www." not in url[0]:
        print '"'+url[0]+'":','"'+name[0]+'",'
      else:
        print '"'+url[0][4:]+'":','"'+name[0]+'",'


def  get_store(url=""):
     #需要考虑的更周到，也许需要细分C店
     #手工加etao
     if url=="":return ""
     for k in storelist.keys():
         if k in url:
             return storelist.get(k)
     return ""  


def  cut_item_picture(STATIC_FILE="",ID=0,filename=""):
     
     """
返回  首位为pic info信息 后为处理信息
图片规则备注
纵向为长  横向为宽
上传要求  长宽比不大于2，否则不使用 长宽都要大于120px
图片分为原图 以下大于都取长宽中的较大者
o+ID.jpg大图 如果图大于500px,压缩到500px,是大图，不到500的原图就是大图
m+ID.jpg中图 用于在展示页面展示，以220为限，不到的就是原图
s+ID.jpg小图 更小 以100为限，所有图压缩到100 可以用于手机
vs+ID.jpg迷你图 最小为70

图片类型  如果
picinfo=0 表示未处理，picurl为原始地址 处理后为大图地址
picinfo=-1 图片处理失败
picinfo=3 图大于500px
        2 大于220px 小于500
        1 大于120px 小于220
        101 表示在网上

     """
     im = Image.open(filename)
     (width,height)=im.size
     if width/height>2 or height/width>2:
          return -1,"width/height should<2"
     if max([width,height])<120:
          return -1,"too small width should >120"
     #保存原图
     im.save(STATIC_FILE+'/o'+str(ID)+".jpg") 
     #竖直巨型，此时固定宽
     if width>=height:
        if width>500:
              ratio=1.0*height/width
              im.resize((500,int(ratio*500.0)),Image.ANTIALIAS).save(STATIC_FILE+'/b'+str(ID)+".jpg",quality=100)
              im.resize((220,int(ratio*220.0)),Image.ANTIALIAS).save(STATIC_FILE+'/m'+str(ID)+".jpg",quality=100)
              im.resize((100,int(ratio*100.0)),Image.ANTIALIAS).save(STATIC_FILE+'/s'+str(ID)+".jpg",quality=100)
              im.resize((70,int(ratio*70.0)),Image.ANTIALIAS).save(STATIC_FILE+'/vs'+str(ID)+".jpg",quality=100)
              picinfo=3        
        elif (width <=500 and width >=220):
              ratio=1.0*height/width
              im.save(STATIC_FILE+'/b'+str(ID)+".jpg") 
              im.resize((220,int(ratio*220.0)),Image.ANTIALIAS).save(STATIC_FILE+'/m'+str(ID)+".jpg",quality=100)
              im.resize((100,int(ratio*100.0)),Image.ANTIALIAS).save(STATIC_FILE+'/s'+str(ID)+".jpg",quality=100)
              im.resize((70,int(ratio*70.0)),Image.ANTIALIAS).save(STATIC_FILE+'/vs'+str(ID)+".jpg",quality=100)
              picinfo=2    
        else :
             ratio=1.0*height/width
             im.save(STATIC_FILE+'/b'+str(ID)+".jpg")
             im.save(STATIC_FILE+'/m'+str(ID)+".jpg")
             im.resize((100,int(ratio*100.0)),Image.ANTIALIAS).save(STATIC_FILE+'/s'+str(ID)+".jpg",quality=100)
             im.resize((70,int(ratio*70.0)),Image.ANTIALIAS).save(STATIC_FILE+'/vs'+str(ID)+".jpg",quality=100)
             picinfo=1
     else:
        if height>500:
              ratio= 1.0*width/height
              im.resize((int(ratio*500.0),500),Image.ANTIALIAS).save(STATIC_FILE+'/b'+str(ID)+".jpg",quality=100)
              im.resize((int(ratio*220.0),220),Image.ANTIALIAS).save(STATIC_FILE+'/m'+str(ID)+".jpg",quality=100)
              im.resize((int(ratio*100.0),100),Image.ANTIALIAS).save(STATIC_FILE+'/s'+str(ID)+".jpg",quality=100)
              im.resize((int(ratio*70.0),70),Image.ANTIALIAS).save(STATIC_FILE+'/vs'+str(ID)+".jpg",quality=100)
             
              picinfo=3        
        elif (height <=500 and height >=220):
              ratio= 1.0*width/height
              im.save(STATIC_FILE+'/b'+str(ID)+".jpg") 
              im.resize((int(ratio*220.0),220),Image.ANTIALIAS).save(STATIC_FILE+'/m'+str(ID)+".jpg",quality=100)
              im.resize((int(ratio*100.0),100),Image.ANTIALIAS).save(STATIC_FILE+'/s'+str(ID)+".jpg",quality=100)
              im.resize((int(ratio*70.0),70),Image.ANTIALIAS).save(STATIC_FILE+'/vs'+str(ID)+".jpg",quality=100)
              picinfo=2        
        else :
             ratio= 1.0*width/height
             im.save(STATIC_FILE+'/b'+str(ID)+".jpg")
             im.save(STATIC_FILE+'/m'+str(ID)+".jpg")
             im.resize((int(ratio*100.0),100),Image.ANTIALIAS).save(STATIC_FILE+'/s'+str(ID)+".jpg",quality=100)
             im.resize((int(ratio*70.0),70),Image.ANTIALIAS).save(STATIC_FILE+'/vs'+str(ID)+".jpg",quality=100)
             picinfo=1
     
     return picinfo,"done"



"""

ns=Node.objects()
for n in ns:
   if n.picurl and n.picurl[0]=='h':
     # file=urllib2.urlopen(n.picurl).read()
     # open(str(n.ID)+".jpg","wb").write(file)
     # tools.cut_item_picture(STATIC_FILE="",ID=n.ID,filename=str(n.ID)+".jpg")
       n.picinfo=1
       n.save()
"""




 
         
    
