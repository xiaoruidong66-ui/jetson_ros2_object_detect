import os, random, shutil

random.seed(42)

img_src = r"C:\Users\Dong Xiaorui\Desktop\all_img"
txt_src = r"C:\Users\Dong Xiaorui\Desktop\all_label"

# 输出目录
train_img = "mydataset/images/train"
val_img = "mydataset/images/val"
train_lab = "mydataset/labels/train"
val_lab = "mydataset/labels/val"

for folder in [train_img, val_img, train_lab, val_lab]:
    os.makedirs(folder, exist_ok=True)

img_list = [f for f in os.listdir(img_src) if f.lower().endswith((".jpg",".jpeg",".png"))]
random.shuffle(img_list)
split_num = int(len(img_list)*0.8)

train_files = img_list[:split_num]
val_files = img_list[split_num:]

for f in train_files:
    base,_ = os.path.splitext(f)
    shutil.copy(os.path.join(img_src,f), os.path.join(train_img,f))
    shutil.copy(os.path.join(txt_src,base+".txt"), os.path.join(train_lab,base+".txt"))

for f in val_files:
    base,_ = os.path.splitext(f)
    shutil.copy(os.path.join(img_src,f), os.path.join(val_img,f))
    shutil.copy(os.path.join(txt_src,base+".txt"), os.path.join(val_lab,base+".txt"))

print(f"训练集 {len(train_files)} 张，验证集 {len(val_files)} 张")
