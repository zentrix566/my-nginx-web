import psutil
import subprocess
import json
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware

# 1. 初始化 FastMCP
mcp = FastMCP("aliyun_sentry")

# 2. 注入 CORS 中间件（修复 Web 页面连接报错的关键）
mcp._app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许任何来源访问
    allow_credentials=True,
    allow_methods=["*"],  # 允许 GET, POST, OPTIONS 等
    allow_headers=["*"],
)

# --- 工具定义区 ---

@mcp.tool()
def get_system_status():
    """获取服务器实时的 CPU、内存、磁盘使用率"""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # 返回 JSON 字符串，方便 Web 页面解析
    stats = {
        "cpu_usage": f"{cpu_usage}%",
        "memory_usage": f"{memory.percent}%",
        "memory_free": f"{round(memory.available / (1024**3), 2)} GB",
        "disk_usage": f"{disk.percent}%"
    }
    return json.dumps(stats)

@mcp.tool()
def analyze_and_fix_oom():
    """检查 OOM 隐患并提供清理建议"""
    try:
        # 检查最近 10 条内存相关报错
        oom_check = subprocess.getoutput('dmesg | grep -i "out of memory" | tail -n 5')
        if not oom_check:
            oom_check = "未发现 OOM 错误记录。"
            
        # 获取占用内存前三的进程
        top_proc = subprocess.getoutput('ps -eo pid,comm,%mem --sort=-%mem | head -n 4')
        
        return {
            "analysis": f"OOM 扫描结果: {oom_check}",
            "top_processes": top_proc,
            "fix_action": "sudo journalctl --vacuum-time=1s"
        }
    except Exception as e:
        return f"分析失败: {str(e)}"

@mcp.tool()
def execute_shell(command: str):
    """在服务器上执行指定的 Shell 指令"""
    # 限制只允许执行特定的安全命令（示例，生产环境建议加白名单）
    forbidden = ["rm -rf /", "mkfs", "shutdown"]
    if any(f in command for f in forbidden):
        return "错误：检测到高危指令，拒绝执行。"

    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return {"status": "success", "output": output.decode('utf-8')}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "output": e.output.decode('utf-8')}

# --- 启动服务 ---

if __name__ == "__main__":
    # 使用 SSE 传输协议，监听 8000 端口
    # host="0.0.0.0" 确保外网可以访问
    mcp.run(transport="sse", host="0.0.0.0", port=8000)