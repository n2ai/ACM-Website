$(document).ready(() => {

    const form = document.getElementById('load-form');
    const editTable = document.querySelector('.edit-table');

    form.addEventListener('submit', (event) => {
        // prevent the form from submitting normally
        event.preventDefault();

        // get the selected category
        const category = document.getElementById('category').value;

        // make an AJAX request to the server
        const xhr = new XMLHttpRequest();
        xhr.open('GET', `/load?category=${category}`);
        xhr.onreadystatechange = function () {
            if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                // update the content of the edit-table div
                editTable.innerHTML = xhr.responseText;
            }
        };
        xhr.send();
    });

})


