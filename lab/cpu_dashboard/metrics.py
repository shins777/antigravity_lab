"""System and CPU metrics extraction service using psutil."""
import os
import time
import platform
import datetime
from typing import Dict, Any, List, Optional
import psutil


class SystemMetricsService:
    """Service for extracting real-time CPU, Memory, and Process metrics."""

    @staticmethod
    def get_cpu_summary() -> Dict[str, Any]:
        """Returns overall CPU usage, core counts, frequency, and load averages."""
        overall_percent = psutil.cpu_percent(interval=None)
        per_core = psutil.cpu_percent(interval=None, percpu=True)
        logical_cores = psutil.cpu_count(logical=True) or 1
        physical_cores = psutil.cpu_count(logical=False) or logical_cores

        # CPU Frequencies
        freq_info = {}
        try:
            freq = psutil.cpu_freq()
            if freq:
                freq_info = {
                    "current": round(freq.current, 1),
                    "min": round(freq.min, 1) if freq.min else None,
                    "max": round(freq.max, 1) if freq.max else None,
                }
        except Exception:
            freq_info = {"current": "N/A", "min": None, "max": None}

        # Load Averages (macOS / Linux)
        load_avg = {}
        try:
            if hasattr(os, "getloadavg"):
                l1, l5, l15 = os.getloadavg()
                load_avg = {
                    "1min": round(l1, 2),
                    "5min": round(l5, 2),
                    "15min": round(l15, 2),
                }
        except Exception:
            load_avg = {"1min": "N/A", "5min": "N/A", "15min": "N/A"}

        return {
            "overall_percent": overall_percent,
            "per_core": per_core,
            "logical_cores": logical_cores,
            "physical_cores": physical_cores,
            "frequency": freq_info,
            "load_avg": load_avg,
        }

    @staticmethod
    def get_memory_summary() -> Dict[str, Any]:
        """Returns RAM and Swap memory utilization."""
        vmem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        def bytes_to_gb(b: int) -> float:
            return round(b / (1024 ** 3), 2)

        return {
            "ram": {
                "total_gb": bytes_to_gb(vmem.total),
                "used_gb": bytes_to_gb(vmem.used),
                "available_gb": bytes_to_gb(vmem.available),
                "percent": vmem.percent,
            },
            "swap": {
                "total_gb": bytes_to_gb(swap.total),
                "used_gb": bytes_to_gb(swap.used),
                "free_gb": bytes_to_gb(swap.free),
                "percent": swap.percent,
            },
        }

    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Returns system platform, boot time, and uptime."""
        boot_time_ts = psutil.boot_time()
        boot_datetime = datetime.datetime.fromtimestamp(boot_time_ts)
        uptime_seconds = int(time.time() - boot_time_ts)

        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s" if days > 0 else f"{hours}h {minutes}m {seconds}s"

        return {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor() or platform.machine(),
            "boot_time": boot_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "uptime": uptime_str,
        }

    @staticmethod
    def get_top_processes(
        limit: int = 10,
        search: Optional[str] = None,
        sort_by: str = "cpu_percent",
    ) -> List[Dict[str, Any]]:
        """Returns top resource consuming processes."""
        processes = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "num_threads", "status", "username"]):
            try:
                info = proc.info
                if search and search.lower() not in (info.get("name") or "").lower():
                    continue
                processes.append({
                    "PID": info.get("pid"),
                    "Name": info.get("name") or "Unknown",
                    "CPU (%)": round(info.get("cpu_percent") or 0.0, 1),
                    "RAM (%)": round(info.get("memory_percent") or 0.0, 1),
                    "Threads": info.get("num_threads") or 1,
                    "Status": info.get("status") or "running",
                    "User": info.get("username") or "-",
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Sort descending
        key_map = {"cpu_percent": "CPU (%)", "memory_percent": "RAM (%)"}
        sort_key = key_map.get(sort_by, "CPU (%)")
        processes.sort(key=lambda p: p.get(sort_key, 0.0), reverse=True)

        return processes[:limit]
