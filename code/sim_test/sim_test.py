#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# sim_test.py
#
# Testing out the simulator in Cirq.
#
# written by Ryan LaRose <laroser1@msu.edu>
# at Michigan State University August 2018.
# =============================================================================

# =============================================================================
# imports
# =============================================================================

import cirq

import numpy as np
import sys
import time

# =============================================================================
# constants
# =============================================================================

# one qubit operations dictionary
oneq_ops = {1 : cirq.X,
            2 : cirq.Y,
            3 : cirq.Z,
            4 : cirq.H,
            5 : cirq.X ** 0.5,
            6 : cirq.T}

# =============================================================================
# functions
# =============================================================================

def sim_test(nqubits, depth, nreps, 
             insert_strategy=cirq.InsertStrategy.EARLIEST, 
             verbose=False, sim_type=0):
    """
    Cirq Simulator test for a circuit structure of layers consisting of
    random one qubit rotations and CNOTs between all qubits.
    
    input:
        nqubits [type: int]
            number of qubits in the circuit
            
        depth [type: int]
            number of layers (described above) in the circuit
            
        nreps [type: int]
            number of times to run the circuit as per the keyword argument
            'repetitions' in the method cirq.google.XmonSimulator.run.
            
        insert_strategy [type: cirq.InsertStrategy,
                         default = cirq.InsertStrategy.EARLIEST]
            insert strategy for new gates in the circuit
        
        verbose [type: bool,
                 default = False]
            flag for verbose output to console (prints out circuit)

        sim_type [type: bool]
            what simulator to use in the timing analysis
            0 = cirq.google.XmonSimulator
            1 = cirq.Simulator

    returns:
        (runtime of simulating the circuit) / nreps
    """
    # get a simulator
    simulator = cirq.google.XmonSimulator()
    if sim_type == 1:
        simulator = cirq.Simulator()
    
    # get some qubits and a circuit
    qbits = [cirq.LineQubit(x) for x in range(nqubits)]
    circ = cirq.Circuit()
    
    # =========================================================================
    # random circuit
    # =========================================================================
    
    def rot(qubit, params):
        """
        Helper function to return an arbitrary rotation of the form
        R = Rz(params[2]) * Ry(params[1]) * Rx(params[0])
        on the qubit.
        """
        rx = cirq.Rx(rads=params[0])
        ry = cirq.Ry(rads=params[1])
        rz = cirq.Rz(rads=params[2])
        
        yield (rx(qubit), ry(qubit), rz(qubit))

    for _ in range(depth):
        # append random single qubit rotations
        for q in qbits:
            circ.append(rot(q, 2 * np.pi * np.random.rand(3)),
                        strategy=insert_strategy)

        # get a random control qubit for cnots
        ctrl = qbits[np.random.randint(len(qbits))]

        # append layer of CNOTS
        circ.append([cirq.CNOT(ctrl, targ) for targ in qbits if targ != ctrl],
                     strategy=insert_strategy)
    # measurements     
    for q in qbits:
        circ.append(cirq.measure(q),
                    strategy=cirq.InsertStrategy.INLINE)
    
    # verbose options
    if verbose:
        print('Circuit structure shown below:', circ, sep='\n')
        
    # =========================================================================
    # do the circuit execution and time it
    # =========================================================================
    
    start = time.time()
    simulator.run(circ, repetitions=nreps)
    return (time.time() - start) / nreps

def random_circuit(num_qubits, depth, 
                   oneq_ops_dict=oneq_ops):
    """Returns a circuit with one qubit gates selected at random from
    'oneq_ops_dict' for a specified number of qubits 'num_qubits'
    and depth 'depth'.
    
    Args:
        num_qubits [type: int]
            number of qubits in the circuit

        depth [type: int]
            number of single qubit gates to append to the circuit

        oneq_ops_dict [type: dict]
            dictionary of one qubit operations with (key, value) pairs that
            consist of (integer key, gate)

    Returns:
        A cirq.Circuit with 'num_qubits' qubits and 'depth' total single
        qubit gates selected at random from 'oneq_ops_dict'.
    """
    # create a circuit
    circ = cirq.Circuit()

    # loop over the depth
    for _ in range(depth):
        # select random integers corresponding to gates to append to circuit
        op_keys = np.random.randint(1, len(oneq_ops) + 1, num_qubits)

        # append the gates to the circuit
        circ.append(
            [oneq_ops[key](q) for (q, key) in enumerate(op_keys)],
            strategy=cirq.InsertStrategy.EARLIEST
            )

    return circ

# =============================================================================
# main 
# =============================================================================

def main():
    """
    Main function for the script.
    """
    # grab user input    
    if len(sys.argv) >= 2:
        nqubits = int(sys.argv[1])
    else:
        nqubits = 2
    if len(sys.argv) >= 3:
        depth = int(sys.argv[2])
    else:
        depth = 3
    if len(sys.argv) >= 4:
        shots = int(sys.argv[3])
    else:
        shots = 1
    if len(sys.argv) >= 5:
        if sys.argv[4] == 0:
            verbose = False
        else:
            verbose = True
    else:
        verbose = False
    if len(sys.argv) >= 6:
        sim = int(sys.argv[5])
    else:
        sim = 0

    # run the simulator test and print the results
    print(nqubits, depth, 
          shots, sim_test(nqubits, depth, shots, verbose=False, sim_type=sim))
    
# =============================================================================
# script
# =============================================================================
    
if __name__ == "__main__":
    main()