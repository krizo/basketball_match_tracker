from fastapi import HTTPException
from sqlmodel import Session, select, SQLModel
from sqlmodel.main import SQLModelMetaclass

from db.database import engine, DbConnection


def read_records(model_class: SQLModelMetaclass, offset: int = 0, limit: int = 100):
    with Session(engine) as session:
        return session.exec(select(model_class).offset(offset).limit(limit)).all()


def create_record(model_class: SQLModelMetaclass, data: SQLModel):
    with Session(engine) as session:
        record = model_class.from_orm(data)
        session.add(record)
        session.commit()
        session.refresh(record)
        return record


def read_record(model_class: SQLModelMetaclass, record_id: int):
    session = DbConnection().get_db()
    match = session.get(model_class, record_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


def update_record(model_class: SQLModelMetaclass, update_data: SQLModel, record_id: int):
    session = DbConnection().get_db()
    record = session.get(model_class, record_id)
    record_data = update_data.dict(exclude_unset=True)
    for key, value in record_data.items():
        setattr(record, key, value)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


def delete_record(model_class: SQLModelMetaclass, record_id: int):
    session = DbConnection().get_db()
    record = session.get(model_class, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Match not found")
    session.delete(record)
    session.commit()
    return {"ok": True}
