#!/usr/bin/env python3
"""
graph.py — Node/edge engine for the skill orchestration layer.

Skills surface issues independently. None of them knows the others exist.
This engine is where those independent opinions get combined into one
coherent review agenda, under rules that are enforced rather than trusted.

Two guarantees, both checked at runtime rather than assumed:

1. Declared access. A node names the keys it reads and the keys it writes.
   Reading anything else raises AccessViolation. A node that never declared
   `rfi_log` cannot reach into the RFI log, because it was never given a way to.

2. Cycle consistency. External state (the issue registry, prior findings,
   the RFI log) is frozen once at the start of a cycle. Every node in that
   cycle reads the same frozen version. Derived values written by nodes are
   write-once, so two nodes can never disagree about what a key holds.

Together these bound the blast radius of a bad node: it can only affect the
nodes downstream of it, and Graph.downstream() names that set exactly.
"""

from collections import deque
from copy import deepcopy


class AccessViolation(Exception):
    """A node read or wrote a key it did not declare."""


class GraphError(Exception):
    """The graph itself is malformed — a cycle, a missing producer, two writers."""


class SharedState:
    """The live store. Mutates freely between cycles; frozen during one."""

    def __init__(self, initial=None):
        self._store = dict(initial or {})
        self._version = 0

    def write(self, key, value):
        self._store[key] = value
        self._version += 1
        return self._version

    def read(self, key, default=None):
        return self._store.get(key, default)

    @property
    def version(self):
        return self._version

    def snapshot(self):
        """Freeze the current store. The copy is deep, so later writes to the
        live store cannot reach into a cycle already in flight."""
        return Snapshot(deepcopy(self._store), self._version)


class Snapshot:
    """An immutable, versioned view of external state for exactly one cycle."""

    __slots__ = ("_store", "version")

    def __init__(self, store, version):
        self._store = store
        self.version = version

    def __contains__(self, key):
        return key in self._store

    def keys(self):
        return set(self._store)

    def get(self, key, default=None):
        return deepcopy(self._store.get(key, default))


class CycleContext:
    """One decision cycle: a frozen input snapshot plus write-once derived values."""

    def __init__(self, snapshot):
        self.snapshot = snapshot
        self.derived = {}
        self._writers = {}

    def resolve(self, key, default=None):
        if key in self.derived:
            return deepcopy(self.derived[key])
        return self.snapshot.get(key, default)

    def has(self, key):
        return key in self.derived or key in self.snapshot

    def commit(self, node_name, key, value):
        if key in self.derived:
            raise GraphError(
                f"{node_name} wrote '{key}', already written by "
                f"{self._writers[key]} in this cycle; derived keys are write-once"
            )
        self.derived[key] = value
        self._writers[key] = node_name


class NodeView:
    """What a node is handed. Enforces the node's own declaration."""

    __slots__ = ("_ctx", "_node")

    def __init__(self, ctx, node):
        self._ctx = ctx
        self._node = node

    @property
    def cycle_version(self):
        return self._ctx.snapshot.version

    def read(self, key, default=None):
        if key not in self._node.reads:
            raise AccessViolation(
                f"{self._node.name} read '{key}' but declares reads={sorted(self._node.reads)}"
            )
        return self._ctx.resolve(key, default)

    def write(self, key, value):
        if key not in self._node.writes:
            raise AccessViolation(
                f"{self._node.name} wrote '{key}' but declares writes={sorted(self._node.writes)}"
            )
        self._ctx.commit(self._node.name, key, value)


class Node:
    """One job, declared inputs, declared outputs."""

    def __init__(self, name, reads, writes):
        self.name = name
        self.reads = set(reads)
        self.writes = set(writes)
        if self.reads & self.writes:
            raise GraphError(
                f"{name} both reads and writes {sorted(self.reads & self.writes)}; "
                "a node may not overwrite its own input"
            )

    def run(self, view):
        raise NotImplementedError

    def __repr__(self):
        return f"<Node {self.name} reads={sorted(self.reads)} writes={sorted(self.writes)}>"


class Graph:
    """Nodes wired by what they read and write, run in dependency order."""

    def __init__(self, nodes, inputs=()):
        self.nodes = list(nodes)
        self.inputs = set(inputs)
        self._by_name = {}
        for node in self.nodes:
            if node.name in self._by_name:
                raise GraphError(f"duplicate node name: {node.name}")
            self._by_name[node.name] = node
        self._producers = self._build_producers()
        self.order = self._toposort()

    def _build_producers(self):
        producers = {}
        for node in self.nodes:
            for key in node.writes:
                if key in producers:
                    raise GraphError(
                        f"'{key}' is written by both {producers[key]} and {node.name}; "
                        "each derived key needs exactly one writer"
                    )
                if key in self.inputs:
                    raise GraphError(f"{node.name} writes '{key}', which is external input")
                producers[key] = node.name
        for node in self.nodes:
            for key in node.reads:
                if key not in producers and key not in self.inputs:
                    raise GraphError(
                        f"{node.name} reads '{key}', which no node writes and "
                        "which is not declared as external input"
                    )
        return producers

    def edges(self):
        """(upstream, downstream) pairs, derived from the declarations alone."""
        out = set()
        for node in self.nodes:
            for key in node.reads:
                producer = self._producers.get(key)
                if producer:
                    out.add((producer, node.name))
        return sorted(out)

    def _toposort(self):
        incoming = {n.name: 0 for n in self.nodes}
        adjacency = {n.name: [] for n in self.nodes}
        for upstream, downstream in self.edges():
            adjacency[upstream].append(downstream)
            incoming[downstream] += 1

        ready = deque(sorted(n for n, c in incoming.items() if c == 0))
        order = []
        while ready:
            name = ready.popleft()
            order.append(name)
            for nxt in sorted(adjacency[name]):
                incoming[nxt] -= 1
                if incoming[nxt] == 0:
                    ready.append(nxt)
        if len(order) != len(self.nodes):
            stuck = sorted(set(incoming) - set(order))
            raise GraphError(f"graph has a cycle among: {stuck}")
        return order

    def downstream(self, node_name):
        """The blast radius of a node: every node its output can reach."""
        if node_name not in self._by_name:
            raise GraphError(f"unknown node: {node_name}")
        adjacency = {n.name: [] for n in self.nodes}
        for upstream, dnstream in self.edges():
            adjacency[upstream].append(dnstream)
        seen = set()
        queue = deque(adjacency[node_name])
        while queue:
            name = queue.popleft()
            if name in seen:
                continue
            seen.add(name)
            queue.extend(adjacency[name])
        return sorted(seen)

    def run(self, state):
        """Run one cycle against a single frozen snapshot of external state."""
        missing = self.inputs - state.snapshot().keys()
        if missing:
            raise GraphError(f"state is missing declared inputs: {sorted(missing)}")
        ctx = CycleContext(state.snapshot())
        for name in self.order:
            node = self._by_name[name]
            node.run(NodeView(ctx, node))
        return ctx

    def describe(self):
        lines = [f"inputs: {sorted(self.inputs)}", "", "nodes (in run order):"]
        for name in self.order:
            node = self._by_name[name]
            lines.append(
                f"  {name}\n"
                f"      reads  {sorted(node.reads)}\n"
                f"      writes {sorted(node.writes)}\n"
                f"      blast  {self.downstream(name) or '(terminal)'}"
            )
        lines.append("")
        lines.append("edges:")
        for upstream, downstream in self.edges():
            lines.append(f"  {upstream} -> {downstream}")
        return "\n".join(lines)


if __name__ == "__main__":
    from nodes import build_graph

    print(build_graph().describe())
