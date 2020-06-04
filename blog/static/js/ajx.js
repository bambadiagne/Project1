
document.addEventListener('DOMContentLoaded', () => {
    let isbn = document.getElementById("isbn").innerHTML;

    document.querySelector('#Form').onsubmit = (e) => {

        const request = new XMLHttpRequest();
        request.open('POST', '/bookpage/' + isbn);
        let comment = document.getElementById("new-review").innerHTML;
        let rating = document.getElementById("ratings-hidden").value;
        request.onload = () => {

            const data = JSON.parse(request.responseText);
            let div = document.createElement("div");
            let p = document.createElement("p");
            p.style.fontWeight = 900;
            p.innerHTML = data.username + '<br><br>' + data.comments;
            div.appendChild(p);
            document.getElementById('result-comment').appendChild(div);
        }

        const data = new FormData();
        data.append('comment', comment);
        data.append('rating', rating);
        data.append('isbn', isbn);
        request.send(data);
        return false;
    };

});
