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

document.getElementById('generateWordCloudButton').addEventListener('click', function() {
    const cryptoInput = document.getElementById('cryptoInput').value.toLowerCase();
    generateWordCloud(cryptoInput);
});

function generateWordCloud(subreddit) {
    // Make an AJAX request to the Flask server to generate the word cloud image
    var wordCloudXhr = new XMLHttpRequest();
    wordCloudXhr.onreadystatechange = function() {
        if (wordCloudXhr.readyState === XMLHttpRequest.DONE) {
            if (wordCloudXhr.status === 200) {
                // Create a Blob from the response and create a URL for the Blob
                var blob = new Blob([wordCloudXhr.response], { type: 'image/png' });
                var blobUrl = URL.createObjectURL(blob);

                // Display the generated word cloud image
                var wordCloudContainer = document.getElementById('wordCloudContainer');
                wordCloudContainer.innerHTML = '<img src="' + blobUrl + '" alt="Word Cloud">';
            } else {
                console.error('Error generating word cloud:', wordCloudXhr.status);
            }
        }
    };
    wordCloudXhr.open('GET', '/generate_word_cloud?input=' + encodeURIComponent(subreddit));
    wordCloudXhr.responseType = 'arraybuffer'; // Treat the response as an array buffer (binary data)
    wordCloudXhr.send();
}


document.getElementById('analyzeSentimentButton').addEventListener('click', function() {
    const cryptoInput = document.getElementById('cryptoInput').value.toLowerCase();
    performSentimentAnalysis(cryptoInput);
});

function performSentimentAnalysis(subreddit) {
    // Make an AJAX request to the Flask server to perform sentiment analysis
    var sentimentXhr = new XMLHttpRequest();
    sentimentXhr.onreadystatechange = function() {
        if (sentimentXhr.readyState === XMLHttpRequest.DONE) {
            if (sentimentXhr.status === 200) {
                // Parse the JSON response
                var sentimentData = JSON.parse(sentimentXhr.responseText);

                // Display the sentiment chart
                displaySentimentChart(sentimentData);
            } else {
                console.error('Error getting sentiment analysis:', sentimentXhr.status);
            }
        }
    };
    sentimentXhr.open('GET', '/get_sentiment?input=' + encodeURIComponent(subreddit));
    sentimentXhr.send();
}

// Function to display the sentiment chart using ApexCharts
function displaySentimentChart(sentimentData) {
    // Adapt series and labels based on your sentiment data
    var series = Object.values(sentimentData).map(value => value || 0);
    var labels = Object.keys(sentimentData);

    // Chart options
    var options = {
        series: series,
        labels: labels,
        chart: {
            type: 'donut',
            height: 150,  // Adjust the height as needed
            sparkline: {
                enabled: true,
            }
        },
        plotOptions: {
            pie: {
                donut: {
                    labels: {
                        show: true,
                        total: {
                            showAlways: false,
                            show: true,
                            label: 'Total'
                        }
                    }
                }
            }
        },
        colors: ['#808080', '#008000', '#FF0000'],  // Neutral grey, positive green, negative red
    };

    // Create a new ApexCharts instance and render the chart
    var chart = new ApexCharts(document.querySelector("#sentimentChart"), options);
    chart.render();
}