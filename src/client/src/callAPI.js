async function callAPI(endpoint, method = 'GET', body = null) {
    const authCookie = document.cookie.split('; ').find(row => row.startsWith('authToken=')).split('=')[1];

    const headers = new Headers({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authCookie}`
    });

    const options = {
        method,
        headers,
        body: body ? JSON.stringify(body) : null
    };

    try {
        const response = await fetch(endpoint, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error calling API:', error);
        throw error;
    }
}

export default callAPI;