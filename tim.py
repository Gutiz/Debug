from datetime import datetime, timedelta
import calendar
import re
from datetime import timezone

# ===== 配置区（关键修复）=====
CURRENT_UTC = datetime.now(timezone.utc)  # 保留原始UTC时间（用于兜底）
TIMEZONE_OFFSET = timedelta(hours=8)  # 中国标准时间偏移（UTC+8）
CURRENT_BEIJING = CURRENT_UTC + TIMEZONE_OFFSET  # ✅ 核心：使用北京时间作为解析基准

UNIT_MAP = {'y': 'year', 'm': 'month', 'd': 'day', 'h': 'hour', 'f': 'minute', 's': 'second'}

# ===== 核心解析函数（保持不变）=====
def parse_time_expression(expr: str, base_time: datetime) -> datetime:
    """解析逻辑不变，但base_time现为北京时间"""
    parts = re.findall(r'(-?\d+)([ymdhfs])', expr)
    offsets = {}
    settings = {}
    
    for num_str, unit in parts:
        num = int(num_str)
        if num_str.startswith('-'):
            offsets[unit] = num
        else:
            settings[unit] = num
    
    current = base_time
    
    # === 第一阶段：处理偏移 ===
    if 'y' in offsets:
        try:
            current = current.replace(year=current.year + offsets['y'])
        except ValueError:
            current = current.replace(year=current.year + offsets['y'], day=28)
    
    if 'm' in offsets:
        total_months = current.year * 12 + (current.month - 1) + offsets['m']
        target_year = total_months // 12
        target_month = total_months % 12 + 1
        max_day = calendar.monthrange(target_year, target_month)[1]
        target_day = min(current.day, max_day)
        try:
            current = current.replace(year=target_year, month=target_month, day=target_day)
        except ValueError:
            current = current.replace(year=target_year, month=target_month, day=1)
    
    delta = timedelta(
        days=offsets.get('d', 0),
        hours=offsets.get('h', 0),
        minutes=offsets.get('f', 0),
        seconds=offsets.get('s', 0)
    )
    current += delta
    
    # === 第二阶段：处理设置 ===
    if 'y' in settings:
        try:
            current = current.replace(year=settings['y'])
        except ValueError:
            current = current.replace(year=settings['y'], day=28)
    
    if 'm' in settings:
        target_month = settings['m']
        max_day = calendar.monthrange(current.year, target_month)[1]
        target_day = min(current.day, max_day)
        try:
            current = current.replace(month=target_month, day=target_day)
        except ValueError:
            current = current.replace(month=target_month, day=1)
    
    for unit, val in settings.items():
        if unit == 'd':
            try:
                current = current.replace(day=val)
            except ValueError:
                max_day = calendar.monthrange(current.year, current.month)[1]
                current = current.replace(day=max_day)
        elif unit == 'h':
            current = current.replace(hour=val)
        elif unit == 'f':
            current = current.replace(minute=val)
        elif unit == 's':
            current = current.replace(second=val)
    
    # === 🔑 第三阶段：设置单位右侧归零（保持不变）===
    if settings:
        units_order = ['y', 'm', 'd', 'h', 'f', 's']
        set_indices = [units_order.index(u) for u in settings.keys() if u in units_order]
        if set_indices:
            min_unit_idx = max(set_indices)
            for idx in range(min_unit_idx + 1, len(units_order)):
                unit = units_order[idx]
                if unit not in settings:
                    try:
                        if unit == 'm':
                            current = current.replace(month=1)
                        elif unit == 'd':
                            current = current.replace(day=1)
                        elif unit == 'h':
                            current = current.replace(hour=0)
                        elif unit == 'f':
                            current = current.replace(minute=0)
                        elif unit == 's':
                            current = current.replace(second=0)
                    except ValueError:
                        if unit == 'd':
                            max_day = calendar.monthrange(current.year, current.month)[1]
                            current = current.replace(day=max_day)
    return current

# ===== 主逻辑（关键修复：时区转换）=====
def main(time_type: str, time_expr: str, start_expr: str, end_expr: str) -> dict:
    # 每次执行时重新获取当前时间
    current_utc = datetime.now(timezone.utc)
    current_beijing = current_utc + TIMEZONE_OFFSET

    time_sec = 0
    start_sec = 0
    end_sec = 0
    error_msg = ""

    try:
        # 安全处理输入（防None，转小写）
        time_type = (time_type or "").strip().lower()
        time_expr = (time_expr or "").strip()
        start_expr = (start_expr or "").strip()
        end_expr = (end_expr or "").strip()

        if time_type == "point" and time_expr:
            # ✅ 核心修复1：用北京时间解析
            target_beijing = parse_time_expression(time_expr, current_beijing)
            # ✅ 核心修复2：转换为UTC时间（Loki要求）
            target_utc = target_beijing - TIMEZONE_OFFSET
            time_sec = int(target_utc.timestamp())
        
        elif time_type == "range":
            # 默认空字符串为当前时间
            start_beijing = parse_time_expression(start_expr, current_beijing)
            end_beijing = parse_time_expression(end_expr, current_beijing)
            start_utc = start_beijing - TIMEZONE_OFFSET
            end_utc = end_beijing - TIMEZONE_OFFSET
            
            if end_utc < start_utc:
                end_utc = start_utc + timedelta(seconds=1)
            start_sec = int(start_utc.timestamp())
            end_sec = int(end_utc.timestamp())
        
        else:  # 安全兜底（使用UTC时间）
            now_sec = int(current_utc.timestamp())
            time_sec = now_sec
            start_sec = now_sec - 3600
            end_sec = now_sec
            error_msg = f"Unknown or invalid time_type: '{time_type}'"
            print(f"[TIME_LOGIC_WARNING] {error_msg}")
    
    except Exception as e:
        # 全局异常兜底
        now_sec = int(current_utc.timestamp())
        time_sec = now_sec
        start_sec = now_sec - 3600
        end_sec = now_sec
        error_msg = str(e)
        print(f"[TIME_PARSE_ERROR] {error_msg} | time_type={time_type}")
    
    return {
        "time_sec": time_sec,
        "start_sec": start_sec,
        "end_sec": end_sec,
        "error": error_msg
    }


# ===== 测试运行代码 =====
if __name__ == "__main__":
    time_type = "range"
    time_expr = ""
    start_expr = ""
    end_expr = ""
    
    result = main(time_type, time_expr, start_expr, end_expr)
    print(f"time_type: {time_type}", f"start_sec: {result['start_sec']}", f"end_sec: {result['end_sec']}")
