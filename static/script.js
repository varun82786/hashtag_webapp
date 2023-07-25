document.addEventListener('DOMContentLoaded', function () {
    const copyBtn = document.querySelector('.copy-btn');
    copyBtn.addEventListener('click', function () {
        const selectedHashtags = document.querySelectorAll('.hashtag.selected');
        if (selectedHashtags.length === 0) {
            alert('Please select hashtags to copy.');
            return;
        }

        let hashtagsText = '';
        selectedHashtags.forEach(function (hashtag) {
            hashtagsText += hashtag.textContent + ' ';
        });

        if (selectedHashtags.length >= 30) {
            alert('Instagram allows only 30 hashtags. Please select 30 or fewer hashtags.');
            return;
        }

        copyToClipboard(hashtagsText).then(function () {
            alert('Selected hashtags copied to clipboard!');
            // Remove the selected class after copying
            selectedHashtags.forEach(function (hashtag) {
                hashtag.classList.remove('selected');
            });
        }).catch(function (error) {
            console.error('Failed to copy hashtags: ', error);
        });
    });
});

function toggleSelection(hashtag) {
    hashtag.classList.toggle('selected');
    updateCounter();
}

function updateCounter() {
    const selectedHashtags = document.querySelectorAll('.hashtag.selected');
    const counter = document.querySelector('.counter');
    counter.textContent = 'Selected hashtags: ' + selectedHashtags.length;
}

function copyToClipboard(text) {
    if (!navigator.clipboard) {
        // Fallback: create a temporary text area element and copy the text to it
        const tempTextArea = document.createElement('textarea');
        tempTextArea.value = text;
        document.body.appendChild(tempTextArea);
        tempTextArea.select();
        document.execCommand('copy');
        document.body.removeChild(tempTextArea);
        return Promise.resolve();
    }

    // Use the clipboard API if available
    return navigator.clipboard.writeText(text);
}

function copySelectedHashtags() {
    const selectedHashtags = document.querySelectorAll('.hashtag.selected');
    if (selectedHashtags.length === 0) {
        alert('Please select hashtags to copy.');
        return;
    }

    let hashtagsText = '';
    selectedHashtags.forEach(function (hashtag) {
        hashtagsText += "#"+hashtag.textContent + ' ';
    });

    copyToClipboard(hashtagsText).then(function () {
        alert('Selected hashtags copied to clipboard!');
        // Remove the selected class after copying
        selectedHashtags.forEach(function (hashtag) {
            hashtag.classList.remove('selected');
        });
    }).catch(function (error) {
        console.error('Failed to copy hashtags: ', error);
    });
}
