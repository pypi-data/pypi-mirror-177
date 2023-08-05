from typing import List
from rikai_sklearn.models import SklearnModelType


class Classifier(SklearnModelType):
    """Classification model type"""

    def schema(self) -> str:
        return "int"

    def predict(self, x, *args, **kwargs) -> List[int]:
        assert self.model is not None
        return self.model.predict(x).tolist()

MODEL_TYPE=Classifier()
