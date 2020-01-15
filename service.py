"""
Author: Hugo
Date: 2020-01-07 22:31
Desc: 
"""

from model import AuditModel


async def audit_record(event: str, event_type: str, level: int, timestamp: str) -> dict:
    audit_instance = AuditModel(
        event=event,
        event_type=event_type,
        level=level,
        timestamp=timestamp
    )
    try:
        result = audit_instance.save()
        return {"retcode": 0, "stdout": result}
    except Exception as e:
        return {"retcode": 1, "stderr": str(e)}
