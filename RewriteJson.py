import json
import os

def rewrite(json_in,json_out):

    j = open(json_in,'r+',encoding='utf-8').read()  # json文件读入成字符串格式

    jj = json.loads(j)

    # jj = json.loads(j)  载入字符串，json格式转python格式

    print(len(jj["shapes"]))  # 获取标签的个数，shapes包含所有的标签

    print(jj["shapes"][0])  # 输出第一个标签信息

    for i in range(len(jj['shapes'])):
        jj["shapes"][i]["label"] = 'chromosome'  # 把所有label的值都改成‘chromosome’
        print(jj["shapes"][i]["label"])

    # 把修改后的python格式的json文件，另存为新的json文件
    with open(json_out, 'w') as f:
        json.dump(jj, f, indent=2)  # indent=4缩进保存json文件
if __name__ == "__main__":
    json_in = "E:/BaiduNetdiskDownload/TorchVision_Maskrcnn/Maskrcnn/PennFudanPed/chromsome/"  # 原json文件路径
    json_out = "E:/BaiduNetdiskDownload/TorchVision_Maskrcnn/Maskrcnn/PennFudanPed/new_chromo/"  # 修改后json文件路径
    files = os.listdir(json_in)
    for file in files:
        print('file is ', file)
        filepath =os.path.join(json_in,file)
        print('filepath is ',filepath)
        savepath = os.path.join(json_out, file)
        print('savepath is ', savepath)
        rewrite(filepath,savepath)
        print(file+'is done!')

