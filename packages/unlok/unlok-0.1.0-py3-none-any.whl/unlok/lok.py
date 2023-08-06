from pydantic import Field
from koil import koilable
from koil.composition import Composition
from unlok.rath import LokRath


@koilable(add_connectors=True)
class Lok(Composition):
    rath: LokRath = Field(default_factory=LokRath)
