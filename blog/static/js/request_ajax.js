const templateComment=`<div class="card-body">
<div class="row">
  <div class="col-md-2">
 <!--   <img *ngIf='userPhoto' [src]="userPhoto" class="img img-rounded img-fluid" />-->

    <img  src="https://image.ibb.co/jw55Ex/def_face.jpg" class="img img-rounded img-fluid" />
    <p class="text-secondary text-center"></p>
  </div>
  <div class="col-md-10">
    <p>
      <strong>{{all_comments[0][0]}}</strong>
      <span class="float-right"><i class="text-warning fa fa-star"></i></span>
      <span class="float-right"><i class="text-warning fa fa-star"></i></span>
      <span class="float-right"><i class="text-warning fa fa-star"></i></span>
      <span class="float-right"><i class="text-warning fa fa-star"></i></span>

    </p>
    <div class="clearfix"></div>
    <p>{{all_comments[i][1]}}</p>
  </div>
</div>
 <br>
</div>`
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
            
            div.innerHTML=`<div class="card-body">
            <div class="row">
              <div class="col-md-2">
             <!--   <img *ngIf='userPhoto' [src]="userPhoto" class="img img-rounded img-fluid" />-->
            
                <img  src="https://image.ibb.co/jw55Ex/def_face.jpg" class="img img-rounded img-fluid" />
                <p class="text-secondary text-center"></p>
              </div>
              <div class="col-md-10">
                <p>
                  <strong>${username}</strong>
                  <span class="float-right"><i class="text-warning fa fa-star"></i></span>
                  <span class="float-right"><i class="text-warning fa fa-star"></i></span>
                  <span class="float-right"><i class="text-warning fa fa-star"></i></span>
                  <span class="float-right"><i class="text-warning fa fa-star"></i></span>
            
                </p>
                <div class="clearfix"></div>
                <p>${comments}</p>
              </div>
            </div>
             <br>
            </div>`                         
            
            
            //"<strong>"+username+"</strong><br><p>"+comments+"</p>";
            document.getElementById('no-comment').hidden=true;
            document.getElementById('comment-section').appendChild(div);
        }

        const data = new FormData();
        data.append('comment', comment);
        data.append('rating', rating);
        data.append('isbn', isbn);
        request.send(data);
        return false;
    };

});
