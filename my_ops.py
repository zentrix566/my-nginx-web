# /root/my_ops.py
from fastmcp import FastMCP
import psutil
import platform

# 创建 MCP 服务，命名为 aliyun-sentry
mcp = FastMCP("aliyun_sentry")

@mcp.tool()
def get_system_status():
    """获取服务器 CPU、内存和磁盘信息"""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return {
        "cpu_usage": f"{cpu}%",
        "memory_usage": f"{mem}%",
        "disk_usage": f"{disk}%",
        "platform": platform.system()
    }

if __name__ == "__main__":
    # 关键点：使用 sse 传输，监听 0.0.0.0 让外部可以访问
    mcp.run(transport="sse", host="0.0.0.0", port=8000)