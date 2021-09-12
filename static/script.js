const wrapper = document.querySelector(".wrapper");
const fileName = document.querySelector(".file-name");
const defaultBtn = document.querySelector("#default-btn");
const cancelBtn = document.querySelector("#cancel-btn i");
const img = document.querySelector("img");

const detectBtn = document.querySelector("#detect-btn");

const skillBars = document.getElementById('skill-bars')

let regExp = /[0-9a-zA-Z\^\&\'\@\{\}\[\]\,\$\=\!\-\#\(\)\.\%\+\~\_ ]+$/;

function defaultBtnActive(){
    defaultBtn.click();
}

defaultBtn.addEventListener("change", function(){
    let file = defaultBtn.files[0];

    if(file){

        const reader = new FileReader();
        reader.onload = function(){
            const result = reader.result;
            img.src = result;
            wrapper.classList.add("active");
        }

        cancelBtn.addEventListener("click", function(){
            img.src = "";
            wrapper.classList.remove("active");
            file = null
        })
        reader.readAsDataURL(file);


    }

    if(defaultBtn.value){
        let valueStore = defaultBtn.value.match(regExp);
        fileName.textContent = valueStore;
    }
    detectBtn.addEventListener('click',function(){
        
        let html = ''

        if(file){
            const formData = new FormData()
            formData.append('file', file)
            fetch('http://127.0.0.1:8000/detect',{
                method: 'post',
                body: formData
            })
            .then(res => res.json())
            .then(data=>{
                let i = 1;
                let html = ''
                for (const [object, score] of data) {
                    html += 
                    `
                    <style>
                    .progress-line.line${i}  span{
                        width: ${Math.round(score*100)}%;
                    } 
                    .progress-line.line${i}  span::after{
                        content: "${Math.round(score*100)}%";
                    }
                    </style>
                    <div class="bar">
                    <div class="info">
                       <span>${object}</span>
                    </div>
                    <div class="progress-line line${i}">
                       <span></span>
                    </div>
                    </div>`
                    i += 1
                };
                skillBars.innerHTML = html;
            })
        }    
    })

});

