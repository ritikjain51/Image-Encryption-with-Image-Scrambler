from PIL import Image
import random
import os


def encrypt_image(password, filename, file_destination):
     im = Image.open(filename)
     pixelList = list(im.getdata())
     random.seed(password)
     random.shuffle(pixelList)
     img = Image.new(im.mode, im.size)
     img.putdata(pixelList)
     index = filename.rindex('/')
     count = 0
     while os.path.exists(file_destination +"/"+ filename[index:-4]+ ".encrypted" + str(count) +".RTK"):
          count += 1
     filename = file_destination+"/"+filename[index:-4]+ ".encrypted" + str(count) +".RTK"
     temp = file_destination + "/" + password+"temp.png"
     img.save(temp)
     os.rename(temp,filename)
     img.close()
     im.close()


def decrypt_image(password, filename,file_destination):
     index = filename.rindex("/")
     temp = filename[:index] + "/" + password +"temp.png"
     os.rename(filename,temp)
     im = Image.open(temp)
     pixelList = list(im.getdata())
     indexVal = list(range(len(pixelList)))
     random.seed(password)
     random.shuffle(indexVal)
     NewPixelList = [0] * (im.size[0] * im.size[1])
     for i,j in enumerate(indexVal):
         NewPixelList[j] = pixelList[i]
     out = Image.new(im.mode, im.size)
     out.putdata(NewPixelList)
     os.rename(temp,filename[:-4]+".RTK")
     count = 0
     while os.path.exists(file_destination +"/"+ filename[index:-4].split(".")[0]+ ".decrypted" + str(count) +".png"):
          count += 1
     filename = file_destination+"/"+filename[index:-4].split(".")[0]+ ".decrypted" + str(count) +".png"
     temp = file_destination + "/" + password+"temp.png"
     out.save(temp)
     os.rename(temp, filename)
     out.close()
     im.close()
