document.addEventListener('DOMContentLoaded', function () {
    const copyBtn = document.querySelector('.copy-btn');
    copyBtn.addEventListener('click', function () {
        const selectedHashtags = document.querySelectorAll('.hashtag');
        let hashtagsText = '';
        selectedHashtags.forEach(function (hashtag) {
            hashtagsText += hashtag.textContent + ' ';
        });
        navigator.clipboard.writeText(hashtagsText);
    });
});
