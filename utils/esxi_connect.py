from pyVim.connect import SmartConnect, Disconnect
import ssl

def connect_esxi(host, user, pwd, port=443):
    # 关闭ssl证书校验（内网环境通用）
    ssl_context = ssl._create_unverified_context()
    conn = SmartConnect(
        host=host,
        user=user,
        pwd=pwd,
        port=port,
        sslContext=ssl_context
    )
    if not conn:
        raise Exception(f"{host} 连接失败，请检查账号密码/网络")
    return conn

def close_conn(conn):
    Disconnect(conn)
