const bot_icon = document.querySelector(".bot_icon")
const msg_box = document.querySelector(".msg_box")
const suggestionlist = document.querySelector(".suggestionlist");
const inputstr = document.querySelector(".inputstr");
const msg = document.querySelector(".msg");
const cover = document.querySelector(".cover");



let suggestion_list = []
suggestion_list.sort();

let msg_history = []

let question_obj 


function getQuestion(obj){
    setTimeout(async()=>{
        question_obj = await sendResponce('data',obj)
        console.log(question_obj)
        if(question_obj?.end_of_conversation){
            msg.innerHTML += `<div class="botmsg">Thank You...</div>`
            setTimeout(()=>{
                bot_icon.click();
            },2000)
        }else{
            extract_question()
        }
    }
    ,2000)
}

getQuestion({});


bot_icon.addEventListener("click",()=>{
    if(msg_box.classList.contains("on")){
        msg_box.classList.add("off")
        msg_box.classList.remove("on")
        cover.classList.add("coveroff")
        cover.classList.remove("coveron")
    }else{
        msg_box.classList.add("on")
        msg_box.classList.remove("off")
        cover.classList.add("coveron")
        cover.classList.remove("coveroff")
    }
});

inputstr.addEventListener("input",(eve)=>{
    var val = (eve.target.value);
    list = suggestion_list.filter((ele)=>{
        return ((ele.toLowerCase()).includes(String(val).toLowerCase()))
    }
    )
    display_suggestion(list);
    if(val == ""){
        suggestionlist.innerHTML = ""
        suggestion_list.forEach((ele)=>{
            suggestionlist.innerHTML+=`<div class="sug">${ele}</div>`
        })
    }
    selector()
})


function display_suggestion(suggestion_list){
    suggestionlist.innerHTML = ""
    if(suggestion_list?.length != 0){
        suggestionlist.style.visibility =  "visible";
    }else{
        suggestionlist.style.visibility =  "hidden";
    }
    suggestion_list?.forEach((ele)=>{
        suggestionlist.innerHTML+=`<div class="sug">${ele}</div>`
    })
    selector();
}

display_suggestion(suggestion_list)

function selector(){
    const select_sug = document.querySelectorAll(".sug");

    select_sug.forEach(ele=>{
        ele.addEventListener("click",(eve)=>{
            inputstr.value = (ele.innerText);
        })
    })
}
function display_msg(){
    msg.innerHTML = "";
    msg_history.forEach((ele)=>{
        if(ele.type == "bot"){
            msg.innerHTML += `<div class="botmsg">${ele.msg}</div>`
        }else{
            msg.innerHTML += `<div class="usermsg">${ele.msg}</div>`    
        }
    })
}
display_msg();

function savemsg(eve){
    if(inputstr.value == ""){
        return;
    }
    var obj = {
        type : "user",
        msg : `${inputstr.value}`
    }
    msg_history.push(obj);
    question_obj.value = inputstr.value;
    inputstr.placeholder = "Text to be send..."
    display_suggestion([])
    getQuestion(question_obj);
    display_msg();
    inputstr.value = "";
}

function extract_question(){
    msg_history.push({
        type : "bot",
        msg : question_obj?.question
    })
    display_msg();
    suggestion_list = question_obj?.suggestion
    display_suggestion(suggestion_list) 
    inputstr.placeholder = question_obj?.placeholder  
}


async function sendResponce(url,obj){
    try{
        const res = await fetch(`http://localhost:5000/${url}`,{
            method : "POST",
            headers : {'Content-Type': 'application/json'},
            body : JSON.stringify(obj)
        })
        const ans = res.json()
        return ans;
    }
    catch(err){
        console.log(err)
    }
}