package com.samvbeckmann.machinelearning.reinforcement.tools;

import com.samvbeckmann.machinelearning.reinforcement.simulation.Board;

import java.io.Serializable;
import java.util.HashMap;

/**
 * Created by Nate on 4/17/17.
 */
public class FrequencyTable
{
    HashMap<StateAction, Integer> freqMap = new HashMap<>();

    public FrequencyTable()
    {
    }

    public void incrementFrequency(Board state, int action)
    {
        freqMap.merge(new StateAction(state, action), 1, (k, x) -> x + 1);
    }

    public int getFrequency(Board state, int action)
    {
        return freqMap.getOrDefault(state, 0);
    }

}
