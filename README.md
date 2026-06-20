# py-esxi-batch-manager
## 基于pyVmomi的ESXi/vSphere Python批量自动化运维工具箱
轻量化工程化工具，统一批量管理多台独立ESXi主机与vCenter集群，替代VMware网页端重复人工操作，适用于机房虚拟化批量交付、资产巡检、虚拟机生命周期自动化。

## 🛡️ 核心批量能力
- 多台ESXi主机yaml清单统一管理，一键批量连接
- 虚拟机批量操作：开机/关机/重启/挂起/销毁
- 模板机批量克隆，自定义CPU、内存、磁盘、网卡配置
- 批量快照创建、定时清理过期快照、快照回滚恢复
- 批量采集硬件性能指标：CPU/内存/磁盘/存储池使用率
- 批量调整虚拟机硬件规格，在线扩容内存与CPU
- 自动采集全机房资产信息，导出标准化Excel台账报表
- 兼容独立单机ESXi、vCenter Server集群双场景

## 📦 环境依赖
Python 3.8 ~ 3.12
底层依赖VMware官方SDK pyVmomi
一键安装全部依赖：

pip install -r requirements.txt  

📂 仓库工程目录说明
```
py-esxi-batch-manager/
├── config/
│   └── host_list.yaml       # ESXi主机配置清单，批量填写多台机房设备
├── scripts/
│   └── main.py              # 程序主入口，所有批量任务执行起点
├── utils/
│   ├── esxi_connect.py      # ESXi连接封装工具，统一处理ssl与连接释放
│   └── export_excel.py      # 资产报表导出模块，自动生成Excel
├── output/                  # 运行脚本自动创建，存放巡检资产报表
├── requirements.txt         # 项目依赖清单
└── README.md
```
⚡ 快速部署 & 使用教程  
1.Clone 整个仓库到本地  

git clone https://github.com/你的用户名/py-esxi-batch-manager.git  
cd py-esxi-batch-manager  
2.安装依赖环境  
pip install -r requirements.txt  
3.修改配置文件 config/host_list.yaml  
填入你的机房 ESXi 主机 IP、登录账号与密码，支持多台设备批量录入
4.执行批量运维任务

# 批量采集所有虚拟机资产并导出Excel报表  
python scripts/main.py  
5.执行完成后，资产 Excel 报表自动输出至 output/ 文件夹
<h2 style="font-size:24px;">⚠️ 生产运维安全规范</h2>
<p style="font-size:18px;">
1. 仅在内网隔离环境使用，禁止公网直接开放ESXi 443端口<br>
2. 日常资产巡检建议配置只读账号；克隆、销毁等高风险操作分配独立管理员账号<br>
3. 正式环境禁止YAML明文存储密码，可改造为环境变量传入账号凭证<br>
4. 批量销毁、批量关机脚本
</p>

<h2 style="font-size:24px;">适用人群</h2>
<p style="font-size:18px;">虚拟化运维工程师、IDC机房管理员、自动化运维开发、私有云平台维护人员</p>
