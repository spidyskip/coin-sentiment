function getCryptoPrice() {
    const cryptoInput = document.getElementById('cryptoInput').value.toLowerCase();
    const apiUrl = `https://api.coingecko.com/api/v3/simple/price?ids=${cryptoInput}&vs_currencies=usd`;

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const price = data[cryptoInput]?.usd;
            if (price !== undefined) {
                document.getElementById('cryptoPrice').innerHTML = `<strong>Current Price:</strong> $${price}`;
            } else {
                document.getElementById('cryptoPrice').innerHTML = `<em>Symbol not found or data not available</em>`;
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('cryptoPrice').innerHTML = `<em>Error fetching data: ${error.message}</em>`;
        });
}
