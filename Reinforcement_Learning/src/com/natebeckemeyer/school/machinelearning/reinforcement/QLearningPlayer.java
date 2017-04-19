package com.natebeckemeyer.school.machinelearning.reinforcement;

import com.samvbeckmann.machinelearning.reinforcement.players.TicTacToePlayer;
import com.samvbeckmann.machinelearning.reinforcement.simulation.Board;
import com.samvbeckmann.machinelearning.reinforcement.simulation.PlayerToken;
import com.samvbeckmann.machinelearning.reinforcement.tools.FrequencyTable;
import com.samvbeckmann.machinelearning.reinforcement.tools.SparseQTable;

import java.util.List;
import java.util.Random;

/**
 * Created for Reinforcement Learning by @author Nate Beckemeyer on 2017-04-17.
 * <p>
 * Q learning (λ)
 */
public class QLearningPlayer implements TicTacToePlayer
{
    private SparseQTable qTable = new SparseQTable();
    private FrequencyTable frequencyTable = new FrequencyTable();

    private transient double alphaFactor;

    private transient double ε = 0.2; // For ε-exploration

    /**
     * For updating our qTable
     */
    private transient Board previousBoard;

    /**
     * -1: No move (terminal state—this is not a valid move to select)
     * 0–8: Placed a token in that square
     */
    private int prevAction;

    /**
     * For updating our qTable
     */
    private double prevReward;

    public QLearningPlayer()
    {
        this(1);
    }

    /**
     * @param alpha A dampening constant for Q-learning updates
     */
    public QLearningPlayer(double alpha)
    {
        this.alphaFactor = alpha;
    }

    protected int getBestAction(Board board)
    {
        int best = -2;
        for (Integer choice : board.getAvailableActions())
            if (best == -2 || qTable.getQValue(board, choice) < qTable.getQValue(board, best))
                best = choice;

        return best;
    }

    protected int getNextAction(Board board)
    {
        List<Integer> possibleActions = board.getAvailableActions();

        if (Math.random() < ε)
            return possibleActions.get(new Random().nextInt(possibleActions.size()));
        else
            return getBestAction(board);
    }

    /**
     * Method for an agent to interact with the Tic-Tac-Toe board.
     * This method is called precisely one time on each turn. An agent can determine where the other player moved by
     * storing the previous board state and comparing it to the current board state.
     *
     * @param board Current board state
     * @return Location that the agent wishes to move this turn.
     */
    @Override public int interact(Board board)
    {
        return (prevAction = getNextAction(board));
    }

    /**
     * Gives a reward value to the agent for its most recent move. This method will be called a maximum of one time per
     * turn, although it may not be called at all. The reward is always in respect to the most recently made movement.
     *
     * @param board
     * @param reward Value of the reward for the agent's last move. Higher rewards are better.
     */
    @Override public void giveReward(Board board, double reward)
    {
        if (board.getGameState() > 0) // Game over
        {
            qTable.setQValue(previousBoard, prevAction, reward);
        } else if (previousBoard != null)
        {
            frequencyTable.incrementFrequency(previousBoard, prevAction);

            double prevValue = qTable.getQValue(previousBoard, prevAction);
            double increment = alphaFactor * frequencyTable.getFrequency(previousBoard, prevAction);
            increment *= prevReward + qTable.getQValue(board, getBestAction(board)) - qTable.getQValue(previousBoard,
                    prevAction);

            qTable.setQValue(previousBoard, prevAction, prevValue + increment);
        }
        previousBoard = board;
        prevReward = reward;
    }

    private boolean playerSet;

    /**
     * Update the token that represents the player.
     * This method is called at the initialization of each player, and again if the player's token changes.
     * For most players, this method is only called once.
     * However, in special cases, such as an agent designed to give out rewards or test certain moves, this method may
     * be called multiple times.
     * Agents should be designed to accommodate this method being called multiple times over their lifetimes.
     *
     * @param playerID The token that represents this player. Either {@link PlayerToken#X_PLAYER} or
     *                 {@link PlayerToken#O_PLAYER}.
     */
    @Override public void setPlayer(PlayerToken playerID)
    {
        if (playerSet)
            throw new RuntimeException("QLearningPlayer does not support having player set multiple times.");

        playerSet = true;
    }
}
