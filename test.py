from uuid import uuid1
import os
import time
text = "我要找#1234號"
# print(os.path.isfile("/static/uploadImage/0bfbfe28-1670-11ea-98c8-acde48001122.jpeg"))
# os.remove("GG.txt")
print((text.index("#")==3) and (text.index("號")==8))
print(text.split("#")[1][0:4])