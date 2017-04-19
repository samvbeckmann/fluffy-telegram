package com.samvbeckmann.machinelearning.reinforcement.tools;

import com.samvbeckmann.machinelearning.reinforcement.simulation.Board;

import java.io.Serializable;

/**
 * Created for Reinforcement Learning by @author Nate Beckemeyer on 2017-04-17.
 */
class StateAction
{
    private Board state;
    private int action;

    StateAction(Board s, int a)
    {
        state = s;
        action = a;
    }

    @Override
    public boolean equals(Object o)
    {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        StateAction that = (StateAction) o;

        return action == that.action && state.equals(that.state);
    }

    @Override
    public int hashCode()
    {
        int result = state.hashCode();
        result = 31 * result + action;
        return result;
    }
}