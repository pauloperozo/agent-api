from datetime import datetime, timezone
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlmodel import SQLModel, Session, select
from .database import engine

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):

    def __init__(self, model_class: Type[ModelType]) -> None:
        self._model_class = model_class

    def get_all(self) -> List[ModelType]:

        with Session(engine) as session:
            statement = select(self._model_class)
            if hasattr(self._model_class, "deleted_at"):
                statement = statement.where(self._model_class.deleted_at == None)
            
            models = session.exec(statement).all()
            return list(models)

    def get_by_id(self, model_id: Any) -> Optional[ModelType]:

        with Session(engine) as session:
            model = session.get(self._model_class, model_id)

            if model and getattr(model, "deleted_at", None) is not None:
                return None
            return model

    def create(self, model: ModelType) -> ModelType:

        with Session(engine) as session:
            session.add(model)
            session.commit()
            session.refresh(model)
            return model

    def update(self, model_id: Any, update_data: Dict[str, Any]) -> Optional[ModelType]:

        with Session(engine) as session:
        
            model = self.get_by_id(model_id)
            if model is None:
                return None

            for key, value in update_data.items():
                if value is not None and hasattr(model, key):
                    setattr(model, key, value)

            if hasattr(model, "updated_at"):
                setattr(model, "updated_at", datetime.now(timezone.utc))

            session.add(model)
            session.commit()
            session.refresh(model)
            return model

    def delete(self, model_id: Any) -> None:

        with Session(engine) as session:
            model = session.get(self._model_class, model_id)
            if model:
                if hasattr(model, "deleted_at"):
                    setattr(model, "deleted_at", datetime.now(timezone.utc))
                    session.add(model)
                else:
                    session.delete(model)
                session.commit()

    def get_by_field(self, field_name: str, value: Any) -> Optional[ModelType]:

        if not hasattr(self._model_class, field_name):
            raise AttributeError(
                f"El modelo {self._model_class.__name__} no tiene el campo '{field_name}'"
            )

        with Session(engine) as session:
            model_field = getattr(self._model_class, field_name)
            statement = select(self._model_class).where(model_field == value)

            if hasattr(self._model_class, "deleted_at"):
                statement = statement.where(self._model_class.deleted_at == None)
                
            return session.exec(statement).first()