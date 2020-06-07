
document.addEventListener('DOMContentLoaded', () => {
    let isbn = document.getElementById("isbn").innerHTML;

    document.querySelector('#Form').onsubmit = (e) => {

        const request = new XMLHttpRequest();
        request.open('POST', '/bookpage/' + isbn);
        let comment = document.getElementById("new-review").value;
        let rating = document.getElementById("ratings-hidden").value;
        request.onload = () => {

            const data = JSON.parse(request.responseText);
            let div = document.createElement("div");
            let username=data.username;
            let comments= data.comments;
            
            div.innerHTML="<strong>"+username+"</strong><br><p>"+comments+"</p>";
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
