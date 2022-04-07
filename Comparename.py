import os


root_path = r'E:/BaiduNetdiskDownload/TorchVision_Maskrcnn/Maskrcnn/PennFudanPed/'



def contrastDir(file_dir):
    jpg_list = []
    xml_list = []
    for root, dirs, files in os.walk(file_dir+'PNGImages'):
        for file in files:
            if os.path.splitext(file)[1] == '.png':
                jpg_list.append(os.path.splitext(file)[0])
    for root, dirs, files in os.walk(file_dir+'PedMasks'):
        for file in files:
            if os.path.splitext(file)[1] == '.png':
                xml_list.append(os.path.splitext(file)[0])
    print('jpg has:',len(jpg_list))
    print('mask has:', len(xml_list))
#对比xml与jpg
    diff = set(xml_list).difference(set(jpg_list))
    print(len(diff))
    for name in diff:
        print("No corresponding image file", name + ".png")
# 对比jpg与xml
    diff2 = set(jpg_list).difference(set(xml_list))
    print(len(diff2))
    for name in diff2:
        print("No corresponding mask file", name + ".png")
#删除没有的对应xml的图像
#        os.remove(file_dir+'JPEGImages/'+ name+'.jpg')
    return jpg_list,xml_list

if __name__ == '__main__':

    contrastDir(root_path)
