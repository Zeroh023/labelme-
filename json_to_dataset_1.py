import argparse
import base64
import json
import os
import os.path as osp

import yaml
import imgviz
import PIL.Image

from labelme.logger import logger
from labelme import utils


#这个脚本是用于在labelme中进行批处理操作的py文件


def main():
    logger.warning(
        "This script is aimed to demonstrate how to convert the "
        "JSON file to a single image dataset."
    )
    logger.warning(
        "It won't handle multiple JSON files to generate a "
        "real-use dataset."
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("json_file")
    parser.add_argument("-o", "--out", default=None)
    args = parser.parse_args()

    json_file = args.json_file
    if args.out is None:
        out_dir = osp.basename(json_file).replace('.', '_')
        out_dir = osp.join(osp.dirname(json_file), out_dir)
    else:
        out_dir = args.out
    if not osp.exists(out_dir):
        os.mkdir(out_dir)
    list = os.listdir(json_file)  # 获取json文件列表


    for i in range(0,len(list)):
        path = os.path.join(json_file, list[i])  # 获取每个json文件的绝对路径
        # filename = list[i][:-5]  # 提取出.json前的字符作为文件名，以便后续保存Label图片的时候使用
        extension = list[i][-4:]
        if extension =='json':
            if os.path.isfile(path):
                data = json.load(open(path))
                imageData = data.get("imageData")  # 根据'imageData'字段的字符得到原图像
                if not imageData:
                    imagePath = os.path.join(os.path.dirname(json_file), data["imagePath"])
                    with open(imagePath, "rb") as f:
                        imageData = f.read()
                        imageData = base64.b64encode(imageData).decode("utf-8")
            img = utils.img_b64_to_arr(imageData)
            label_name_to_value = {"_background_": 0}
            for shape in sorted(data["shapes"], key=lambda x: x["label"]):
                label_name = shape["label"]
                if label_name in label_name_to_value:
                    label_value = label_name_to_value[label_name]
                else:
                    label_value = len(label_name_to_value)
                    label_name_to_value[label_name] = label_value
            lbl, _ = utils.shapes_to_label(
                img.shape, data["shapes"], label_name_to_value
            )
            label_names = [None] * (max(label_name_to_value.values()) + 1)
            for name, value in label_name_to_value.items():
                label_names[value] = name

            lbl_viz = imgviz.label2rgb(
                lbl, imgviz.asgray(img), label_names=label_names, loc="rb"
            )

            out_dir = osp.basename(list[i]).replace('.', '_')
            out_dir = osp.join(osp.dirname(list[i]), out_dir)
            if not osp.exists(out_dir):
                os.mkdir(out_dir)

            PIL.Image.fromarray(img).save(osp.join(out_dir, "img.png"))
            utils.lblsave(osp.join(out_dir, "label.png"), lbl)
            PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, "label_viz.png"))

            with open(osp.join(out_dir, "label_names.txt"), "w") as f:
                for lbl_name in label_names:
                    f.write(lbl_name + "\n")
            logger.warning('info.yaml is being replaced by label_names.txt')
            info = dict(label_names=label_names)
            with open(osp.join(out_dir, 'info.yaml'), 'w') as f:
                yaml.safe_dump(info, f, default_flow_style=False)

            logger.info("Saved to: {}".format(out_dir))


if __name__ == "__main__":
    main()
