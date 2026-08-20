"""Type aliases used across the gate library."""

from typing import Callable, Dict

Size = int
Name = str

QRegsSpec = Dict[Name, Size]

Value = int
Computation = Callable[[Value], Value]
ComputationsMap = Dict[Name, Computation]
ValuesMap = Dict[Name, Value]
