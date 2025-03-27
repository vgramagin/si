// src/PrepareDataBasedOnURL.js
import React, { useState, useEffect } from 'react';
import callAPI from './callAPI';

const POSSIBLE_STATES = {
    NOT_STARTED: 'NOT_STARTED',
    GAME_CREATED: 'GAME_CREATED',
    GAME_STARTED: 'GAME_STARTED',
}

function ComponentHost() {


    const [gameState, setGameState] = useState(POSSIBLE_STATES.NOT_STARTED);
    const [players, setPlayers] = useState([]);
    const [loading, setLoading] = useState(false);

    const loadData = async () => {
        try {
            setLoading(true);
            const data = await callAPI(`/api/get_data`);
            console.log('response', data);

            if (data && data.gameState) {
                setGameState(data.gameState);
                if (data.players) {
                    setPlayers(data.players);
                }
            } else {
                setGameState(POSSIBLE_STATES.NOT_STARTED);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };



    useEffect(() => {
        const fetchInitialData = async () => loadData();
        fetchInitialData();
    }, []);

    const handleCreateGame = async () => {
        try {
            await callAPI(`/api/set_data`, 'POST', { gameState: POSSIBLE_STATES.GAME_CREATED });
            setGameState(POSSIBLE_STATES.GAME_CREATED);
        } catch (error) {
            console.error('Error setting data:', error);
        }
    }

    const handleStartGame = async () => {
        try {
            console.log('creating...')
            await callAPI(`/api/set_data`, 'POST', { gameState: POSSIBLE_STATES.GAME_STARTED, players });
            setGameState(POSSIBLE_STATES.GAME_STARTED);
        } catch (error) {
            console.error('Error setting data:', error);
        }
    }

    const handleLoadPlayers = async () => {
        await loadData();
    }

    const handleEndGame = async () => {
        try {
            await callAPI(`/api/set_data`, 'POST', { gameState: POSSIBLE_STATES.NOT_STARTED, players: [] });
            setPlayers([]);
            setGameState(POSSIBLE_STATES.NOT_STARTED);
        } catch (error) {
            console.error('Error setting data:', error);
        }
    }

    return (
        <div>
            <h2>Host Interface</h2>

            {gameState === POSSIBLE_STATES.NOT_STARTED && <button onClick={handleCreateGame}>Create Game</button>}
            {gameState === POSSIBLE_STATES.GAME_CREATED && (
                <div>
                    <h3>Game Created</h3>
                    <button onClick={handleLoadPlayers}>Load players (TODO: add socket to do it)</button>
                    <button onClick={handleStartGame}>Start Game</button>
                </div>
            )}
            {gameState === POSSIBLE_STATES.GAME_STARTED && (
                <div>
                    <h3>Game Created</h3>
                    <button onClick={handleLoadPlayers}>Load players (TODO: add socket to do it)</button>
                    <button onClick={handleEndGame}>End Game</button>
                </div>
            )}

            {players.map((player, index) => (
                <div key={index}>
                    <p>{player}</p>
                </div>
            ))}



            {loading && <p>Loading...</p>}


        </div>
    );
}

export default ComponentHost;