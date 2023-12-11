from typing import Union
from pyhdl import hdl, Module
from .circuit import Circuit, Wire


def compile_to_circuit(module: Union[hdl.Module, Module]) -> Circuit:
    if isinstance(module, Module):
        module = module.ast
    module: hdl.Module
    circuit = Circuit()
    for param in module.params:
        wire = Wire(param.n_bits, param.signed, param.name)
        circuit.add_wire(wire.name, wire)

    for local in module.wires:
        wire = Wire(local.n_bits, local.signed, local.name)
        circuit.add_wire(wire.name, wire)

    for name, instance in module.instances.items():
        # implement it later
        pass

    for stat in module.combs.statements:
        if isinstance(stat, hdl.Assign):
            expr = stat.expr
            fv = expr.free_variables()
            for var in fv:
                wire = circuit.find_wire(var.name)
                wire.add_change_event(lambda: circuit.execute(stat))
            circuit.execute(stat)
        else:
            raise NotImplementedError(stat)

    for always in module.always:
        edges = always.edges
        body = always.body
        for e in edges:
            wire = circuit.find_wire(e.wire.name)
            if isinstance(e, hdl.PosEdge):
                wire.add_change_event(wire.make_pos_event(lambda: circuit.execute(body)))
            elif isinstance(e, hdl.NegEdge):
                wire.add_change_event(wire.make_neg_event(lambda: circuit.execute(body)))
            else:
                wire.add_change_event(lambda: circuit.execute(body))
    return circuit
