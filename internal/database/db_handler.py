import json
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from internal.database.init import engine
from internal.database.models.logs import Logs
from internal.database.models.switch import Switch

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_bot_switch(group_id: str):
    session = SessionLocal()
    try:
        return session.query(Switch).filter(Switch.group_id == str(group_id)).first()
    finally:
        session.close()


def set_bot_switch(group_id: str, switch_value: str):
    session = SessionLocal()
    try:
        switch = session.query(Switch).filter(Switch.group_id == str(group_id)).first()
        if switch:
            switch.switch = switch_value
        else:
            date = datetime.now()
            switch = Switch(group_id=group_id, switch=switch_value, time=date)
            session.add(switch)
        session.commit()
    finally:
        session.close()


def set_chat_logs(messages: str):
    session = SessionLocal()
    try:
        messages = json.dumps(messages, ensure_ascii=False)
        date = datetime.now()
        log = Logs(json=messages, time=date)
        session.add(log)
        session.commit()
    finally:
        session.close()
