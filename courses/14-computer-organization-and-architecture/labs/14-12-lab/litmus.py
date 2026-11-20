"""Exhaustive litmus-test enumeration for Lab 14-12.

A test is a list of threads; each thread is a list of instructions ("st", var, value), ("ld", var, reg) or
("fence",). `outcomes(test, model)` explores every execution and returns the set of final register states:

- "SC": sequential consistency: some interleaving of the threads' instructions, each acting on memory at once;
- "TSO": every thread has a FIFO store buffer; a store enters the buffer, a load reads its own newest buffered
  store to that variable if any, otherwise memory; the oldest buffered store may drain to memory at any time;
  a fence waits until the buffer is empty (the x86-TSO abstract machine);
- "PSO": as TSO, but the buffer may drain stores to different variables in any order (stores to the same
  variable stay in order), which also lets two stores become visible out of program order.
"""
from __future__ import annotations


def outcomes(test: list[list[tuple]], model: str = "SC") -> set[tuple]:
    regs_order = sorted({ins[2] for th in test for ins in th if ins[0] == "ld"})
    results: set = set()
    seen: set = set()

    def key(pcs, bufs, mem, regs):
        return (pcs, bufs, tuple(sorted(mem.items())), tuple(sorted(regs.items())))

    def dfs(pcs, bufs, mem, regs):
        k = key(pcs, bufs, mem, regs)
        if k in seen:
            return
        seen.add(k)
        done = all(pc == len(th) for pc, th in zip(pcs, test))
        if done and all(not b for b in bufs):
            results.add(tuple(regs[r] for r in regs_order))
            return
        for t, th in enumerate(test):
            buf = bufs[t]
            # drain a buffered store
            if buf:
                drainable = [0] if model == "TSO" else [
                    i for i, (v, _) in enumerate(buf) if all(buf[j][0] != v for j in range(i))]
                for i in drainable:
                    v, val = buf[i]
                    nb = list(bufs)
                    nb[t] = buf[:i] + buf[i + 1:]
                    dfs(pcs, tuple(nb), {**mem, v: val}, regs)
            # execute the next instruction
            if pcs[t] == len(th):
                continue
            ins = th[pcs[t]]
            np_ = list(pcs)
            np_[t] += 1
            np_ = tuple(np_)
            if ins[0] == "st":
                if model == "SC":
                    dfs(np_, bufs, {**mem, ins[1]: ins[2]}, regs)
                else:
                    nb = list(bufs)
                    nb[t] = buf + ((ins[1], ins[2]),)
                    dfs(np_, tuple(nb), mem, regs)
            elif ins[0] == "ld":
                own = [val for v, val in buf if v == ins[1]]
                val = own[-1] if own else mem.get(ins[1], 0)
                dfs(np_, bufs, mem, {**regs, ins[2]: val})
            elif ins[0] == "fence":
                if not buf:
                    dfs(np_, bufs, mem, regs)

    dfs(tuple(0 for _ in test), tuple(() for _ in test), {}, {})
    return results


SB = [[("st", "x", 1), ("ld", "y", "r1")], [("st", "y", 1), ("ld", "x", "r2")]]
SB_FENCED = [[("st", "x", 1), ("fence",), ("ld", "y", "r1")], [("st", "y", 1), ("fence",), ("ld", "x", "r2")]]
MP = [[("st", "data", 42), ("st", "flag", 1)], [("ld", "flag", "r1"), ("ld", "data", "r2")]]
MP_FENCED = [[("st", "data", 42), ("fence",), ("st", "flag", 1)], [("ld", "flag", "r1"), ("ld", "data", "r2")]]
