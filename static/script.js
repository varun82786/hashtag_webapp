document.addEventListener('DOMContentLoaded', function () {
    const copyBtn = document.querySelector('.copy-btn');
    copyBtn.addEventListener('click', function () {
        const selectedHashtags = document.querySelectorAll('.hashtag.selected');
        if (selectedHashtags.length === 0) {
            alert('Please select hashtags to copy.');
            return;
        }

        let hashtagsArray = Array.from(selectedHashtags).map(function (hashtag) {
            return extractFirstPart(hashtag.textContent);
        });

        if (selectedHashtags.length > 30) {
            alert('Instagram allows only 30 hashtags. Please select 30 or fewer hashtags.');
            return;
        }

        // Your new string to insert
        const newString = "#cruisingbug";

        // Generate a random index
        const randomIndex = Math.floor(Math.random() * (hashtagsArray.length + 1));

        // Insert the new string at the random index
        hashtagsArray.splice(randomIndex, 0, newString);

        // Join the array back into a string
        const hashtagsText = hashtagsArray.join(' ');

        copyToClipboard(hashtagsText).then(function () {
            alert('Selected hashtags copied to clipboard!');
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
        hashtagsText += hashtag.textContent + ' ';
    });

    /*copyToClipboard(hashtagsText).then(function () {
        alert('Selected hashtags copied to clipboard!');
        // Remove the selected class after copying
        selectedHashtags.forEach(function (hashtag) {
            hashtag.classList.remove('selected');
        });
    }).catch(function (error) {
        console.error('Failed to copy hashtags: ', error);
    });*/
}

function extractFirstPart(inputString) {
    // Use the split method to split the inputString by space
    const parts = inputString.split(' ');
    
    // Check if there are parts, and return the first part (index 0)
    if (parts.length > 0) {
        return parts[0];
    } else {
        // Return an empty string if there are no parts
        return '';
    }
}
