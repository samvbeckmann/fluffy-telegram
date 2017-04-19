package com.samvbeckmann.machinelearning.reinforcement.tools;

import com.samvbeckmann.machinelearning.reinforcement.simulation.Board;

import java.io.Serializable;
import java.util.HashMap;

/**
 * Useful for
 */
public class SparseQTable
{
    HashMap<StateAction, Double> table;
    private double def = 0;

    public SparseQTable()
    {
        this(0);
    }

    public SparseQTable(double def)
    {
        this.def = def;
        table = new HashMap<>();
    }

    public double getQValue(Board state, int action)
    {
        return table.getOrDefault(new StateAction(state, action), def);
    }

    public void setQValue(Board state, int action, double val)
    {
        table.put(new StateAction(state, action), val);
    }

    public void setQValue(StateAction stateAction, double val)
    {
        table.put(stateAction, val);
    }

}