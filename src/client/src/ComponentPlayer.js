// src/PrepareDataBasedOnURL.js
import React, { useState, useEffect } from 'react';
import callAPI from './callAPI';

const POSSIBLE_STATES = {
    NOT_STARTED: 'NOT_STARTED',
    GAME_CREATED: 'GAME_CREATED',
    GAME_STARTED: 'GAME_STARTED',
}

function ComponentPlayer() {


    const [gameState, setGameState] = useState(POSSIBLE_STATES.NOT_STARTED);
    const [players, setPlayers] = useState([]);
    const [name, setName] = useState('');
    const [loading, setLoading] = useState(false);

    const loadData = async () => {
        try {
            setLoading(true);
            const data = await callAPI(`/api/get_data`);
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

    const handleJoinGame = async () => {
        try {
            const proposedPlayers = [...players];
            if (!proposedPlayers.includes(name)) {
                proposedPlayers.push(name);
            }
            await callAPI(`/api/set_data`, 'POST', { gameState, players: proposedPlayers });
            await loadData();

        } catch (error) {
            console.error('Error setting data:', error);
        }
    }


    const handleLoadGames = async () => {
        await loadData();
    }



    return (
        <div>
            <h2>Player Interface</h2>

            {gameState === POSSIBLE_STATES.NOT_STARTED && <button onClick={() => handleLoadGames()}>Check For Game Start (TODO: A lot)</button>}
            {gameState === POSSIBLE_STATES.GAME_CREATED && (
                <div>
                    <h3>Game Created</h3>
                    <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
                    <button onClick={() => handleJoinGame()}>Join Game</button>
                    <button onClick={() => handleLoadGames()}>Load Game State (TODO: add socket to do it)</button>
                </div>
            )}
            {gameState === POSSIBLE_STATES.GAME_STARTED && (
                <div>
                    <h3>Game Started</h3>
                    <button onClick={() => handleLoadGames()}>Load Game State (TODO: add socket to do it)</button>
                </div>
            )}

            {players.map((player, index) => (
                <div key={index}>
                    <p>{player === name ? "*" : ""}{player}</p>
                </div>
            ))}



            {loading && <p>Loading...</p>}


        </div>
    );
}

export default ComponentPlayer;