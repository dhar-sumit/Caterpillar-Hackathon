document.addEventListener('DOMContentLoaded', () => {
    const textArea = document.getElementById('textArea');
    const startInspectionButton = document.getElementById('startInspection');
    const restartAppButton = document.getElementById('restartApp');
    const exitAppButton = document.getElementById('exitApp');

    function updateText(message) {
        textArea.innerHTML += `<div>${message}</div>`;
        textArea.scrollTop = textArea.scrollHeight;
    }

    function fetchData(url, method = 'GET', body = null) {
        return fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: body
        }).then(response => response.json());
    }

    function playAudio(audioUrl) {
        const audio = new Audio(audioUrl);
        audio.play();
    }

    startInspectionButton.addEventListener('click', () => {
        updateText('Starting inspection...');
        fetchData('/start-inspection').then(data => {
            if (data.results) {
                updateText(data.results.join('<br/>'));
            } else if (data.error) {
                updateText('Error: ' + data.error);
            }
        });
    });

    restartAppButton.addEventListener('click', () => {
        updateText('Restarting application...');
        fetchData('/restart-app');
    });

    exitAppButton.addEventListener('click', () => {
        updateText('Exiting application...');
        fetchData('/exit-app');
    });

    function speak(text) {
        fetchData('/speak', 'POST', JSON.stringify({ text: text })).then(data => {
            if (data.audio_url) {
                playAudio(data.audio_url);
            } else if (data.error) {
                updateText('Error generating speech.');
            }
        });
    }

    // Test speaking functionality
    // speak('Hello, this is a test.');
});
