from datetime import datetime

def format_datetime(dt_str):
    # Здесь мы предположим, что dt_str - это строка с форматом даты
    dt = datetime.fromisoformat(dt_str)  # Преобразуем строку в datetime
    return dt.strftime("%d.%m.%Y %H:%M:%S")