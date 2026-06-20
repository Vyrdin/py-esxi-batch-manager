import os
from openpyxl import Workbook

def save_vm_report(data, save_path):
    if not os.path.exists("./output"):
        os.makedirs("./output")
    wb = Workbook()
    ws = wb.active
    ws.title = "虚拟机资产清单"
    # 写入表头
    ws.append(["主机地址", "虚拟机名", "CPU核数", "内存GB", "运行状态", "存储占用GB"])
    for row in data:
        ws.append(row)
    wb.save(save_path)
    print(f"资产报表已导出：{save_path}")
