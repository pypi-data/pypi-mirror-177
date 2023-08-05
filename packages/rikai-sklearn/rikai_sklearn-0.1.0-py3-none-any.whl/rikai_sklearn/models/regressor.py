from typing import List
from rikai_sklearn.models import SklearnModelType


class Regressor(SklearnModelType):
    def schema(self) -> str:
        return "float"

    def predict(self, x, *args, **kwargs) -> List[float]:
        assert self.model is not None
        return self.model.predict(x).tolist()

MODEL_TYPE = Regressor()
