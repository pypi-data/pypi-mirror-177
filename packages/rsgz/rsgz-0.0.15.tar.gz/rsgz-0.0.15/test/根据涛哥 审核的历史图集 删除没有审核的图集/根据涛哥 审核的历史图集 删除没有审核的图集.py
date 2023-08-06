import shutil,os
from rsgz.mulu.dirs import compare_dir,get_dirs
from rsgz.file.files import get_base_name

dir_fu = r"\\192.168.0.200\e\李江涛\英杰PS-代码成品\VCJ01"   # 多一点的
dir_zi = r"\\192.168.0.200\e\李江涛\英杰PS-代码成品\X04"  # 少一点的
fu_set1 = set(get_base_name(get_dirs(dir_fu)))

fu_set2 = set(get_base_name(get_dirs(dir_zi)))

# 下面这是 不纯净的 需要排除的文件夹
fu_set2.remove("女士长袖圆领X04-1")
fu_set2.remove("女士长袖圆领X04-2")
fu_set2.remove("女士长袖圆领X04-3")
fu_set2.remove("女士长袖圆领X04-4")
fu_set2.remove("女士长袖圆领X04-5")

print(len(fu_set1))
print(len(fu_set2))

chayi = list(fu_set1.difference(fu_set2))
print(len(chayi))

for i in chayi:
    rd_dir = os.path.join(dir_fu, i)
    try:
        print(rd_dir)
        shutil.rmtree(rd_dir)
    except:
        print("删除{}文件 有问题!".format(rd_dir))
