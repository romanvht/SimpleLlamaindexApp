function sendQuestion() {
    const question = document.getElementById('question-input');
    const responseContainer = document.getElementById('response-container');

    if (question.value.trim() === '') {
        responseContainer.innerHTML = '<div class="centered">Введите вопрос!</div>';
        return;
    }

    responseContainer.innerHTML = '<div class="centered"><img src="assets/img/load.svg" alt="loading"></div>';

    const apiUrl = 'https://hatiko.romanvht.ru:5000/api';

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: question.value }),
    })
        .then(response => response.json())
        .then(data => {
            responseContainer.innerHTML = responseToHTML(data.response);
            question.value = '';
        })
        .catch(error => {
            responseContainer.innerHTML = '<div class="centered">Error: ' + error.message + '</div>';
        });
}

function responseToHTML(markdown) {
    markdown = markdown.replace(/^# (.*$)/gm, '<h1>$1</h1>');
    markdown = markdown.replace(/^## (.*$)/gm, '<h2>$1</h2>');
    markdown = markdown.replace(/^### (.*$)/gm, '<h3>$1</h3>');
    markdown = markdown.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    markdown = markdown.replace(/\*(.*?)\*/g, '<em>$1</em>');
    markdown = markdown.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');
    markdown = markdown.replace(/^\s*\*\s(.*)/gm, '<li>$1</li>');
    markdown = markdown.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    markdown = markdown.replace(/\n/g, '<br>');
    
    return markdown.trim();
}

document.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendQuestion();
    }
});

const block = document.getElementById('response-container');
let previousHeight = block.scrollHeight;

const observer = new MutationObserver(function () {
    const newHeight = block.scrollHeight + 'px'; 
    block.style.height = previousHeight + 'px'; 
    previousHeight = block.scrollHeight;
    block.style.height = newHeight;

    setTimeout(() => {
        previousHeight = block.scrollHeight;
        block.style.height = "auto";
    }, 200);
});

observer.observe(block, {
    childList: true, 
    subtree: true
});
