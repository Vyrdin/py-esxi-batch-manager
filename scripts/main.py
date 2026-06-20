# scripts/main.py
import sys
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import pyVim.task
import ssl


def connect_to_vcenter(vcenter_ip, vcenter_user, vcenter_password, port=443):
    
    try:        
        ssl_context = ssl._create_unverified_context()
        si = SmartConnect(
            host=vcenter_ip,
            user=vcenter_user,
            pwd=vcenter_password,
            port=port,
            sslContext=ssl_context
        )
        if not si:
            raise Exception("连接返回空实例，请检查地址账号密码")
        print(f"✅ 成功连接 vCenter: {vcenter_ip}")
        return si
    except Exception as e:
        print(f"❌ vCenter 连接失败: {str(e)}")
        sys.exit(-1)


def close_vcenter_conn(si):
    
    if si:
        Disconnect(si)
        print("🔌 已断开vCenter连接")


def get_all_esxi_hosts(si):
  
    content = si.RetrieveContent()
    host_folder = content.hostFolder
    all_hosts = host_folder.childEntity
    host_list = []
    for obj in all_hosts:
        if isinstance(obj, vim.HostSystem):
            host_list.append(obj)
    return host_list


def wait_for_tasks(si, task_list):
    
    content = si.RetrieveContent()
    for task in task_list:
        pyVim.task.WaitForTask(task, content)


def vm_power_on(si, vm_obj):
  
    try:
        print(f"▶️ 正在开机: {vm_obj.name}")
        task = vm_obj.PowerOn()
        wait_for_tasks(si, [task])
        print(f"✅ {vm_obj.name} 开机完成")
    except Exception as e:
        print(f"❌ {vm_obj.name} 开机失败: {str(e)}")


def vm_power_off(si, vm_obj):
    
    try:
        print(f"⏹️ 正在关机: {vm_obj.name}")
        task = vm_obj.PowerOff()
        wait_for_tasks(si, [task])
        print(f"✅ {vm_obj.name} 关机完成")
    except Exception as e:
        print(f"❌ {vm_obj.name} 关机失败: {str(e)}")


def main():
    # =================================================================================
    VC_IP = "vcenter_ip_address"
    VC_USER = "vcenter_username"
    VC_PWD = "vcenter_password"
    RUN_POWER_ON = False   
    RUN_POWER_OFF = False
    # ==================================================================================

    
    si_instance = connect_to_vcenter(VC_IP, VC_USER, VC_PWD)

    
    esxi_hosts = get_all_esxi_hosts(si_instance)
    if not esxi_hosts:
        print("未检测到任何ESXi主机")
        close_vcenter_conn(si_instance)
        return

    
    for host in esxi_hosts:
        print("\n=====================================")
        print(f"ESXi 主机名称: {host.name}")
        
        ip_info = host.network.ipConfig.ipAddress
        host_ip = ip_info[0].ipAddress if ip_info else "无管理IP"
        print(f"管理IP: {host_ip}")
        print(f"ESXi版本: {host.summary.config.product.version}")
        print(f"连接状态: {host.summary.runtime.connectionState}")
        print("=====================================\n")

        
        vm_all = host.vm or []
        power_off_vms = [vm for vm in vm_all if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOff]
        power_on_vms = [vm for vm in vm_all if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn]

        print(f"当前关机虚拟机数量: {len(power_off_vms)}")
        print(f"当前运行虚拟机数量: {len(power_on_vms)}")

       
        if RUN_POWER_ON and power_off_vms:
            print("\n------ 批量开机任务开始 ------")
            for vm in power_off_vms:
                vm_power_on(si_instance, vm)

        
        if RUN_POWER_OFF and power_on_vms:
            print("\n------ 批量关机任务开始 ------")
            for vm in power_on_vms:
                vm_power_off(si_instance, vm)

   
    close_vcenter_conn(si_instance)


if __name__ == "__main__":
    main()
