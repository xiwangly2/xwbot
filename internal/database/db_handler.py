from sqlalchemy.orm import sessionmaker
from internal.database.init import engine
from internal.database.models.logs import Logs
from internal.database.models.switch import Switch

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_bot_switch(group_id: str):
    session = SessionLocal()
    try:
        return session.query(Switch).filter(Switch.group_id == group_id).first()
    finally:
        session.close()


def set_bot_switch(group_id: str, switch_value: str):
    session = SessionLocal()
    try:
        switch = session.query(Switch).filter(Switch.group_id == group_id).first()
        if switch:
            switch.switch = switch_value
        else:
            switch = Switch(group_id=group_id, switch=switch_value,
                            time="current_time")  # Replace "current_time" with actual time
            session.add(switch)
        session.commit()
    finally:
        session.close()


def set_chat_logs(json: str):
    session = SessionLocal()
    try:
        log = Logs(json=json, time="current_time")  # Replace "current_time" with actual time
        session.add(log)
        session.commit()
    finally:
        session.close()
