const chatForm=document.getElementById("chatForm");
const messageInput=document.getElementById("messageInput");
const sendButton=document.getElementById("sendButton");
const clearButton=document.getElementById("clearButton");
const chatMessages=document.getElementById("chatMessages");
const typingIndicator=document.getElementById("typingIndicator");
const activityList=document.getElementById("activityList");
let conversationHistory=[];

function addMessage(role,text){
  const article=document.createElement("article");
  article.className=`message ${role}-message`;
  const avatar=document.createElement("div");
  avatar.className="message-avatar";
  avatar.textContent=role==="user"?"YOU":"AI";
  const content=document.createElement("div");
  content.className="message-content";
  const label=document.createElement("span");
  label.className="message-role";
  label.textContent=role==="user"?"You":"Assistant";
  const paragraph=document.createElement("p");
  paragraph.textContent=text;
  content.appendChild(label);
  content.appendChild(paragraph);
  article.appendChild(avatar);
  article.appendChild(content);
  chatMessages.appendChild(article);
  chatMessages.scrollTop=chatMessages.scrollHeight;
}

function showActivity(trace){
  activityList.replaceChildren();
  if(!Array.isArray(trace)||trace.length===0){
    const item=document.createElement("li");
    item.textContent="No tools were used for this response.";
    activityList.appendChild(item);
    return;
  }
  trace.forEach(entry=>{
    const item=document.createElement("li");
    const name=entry.tool||entry.name||"Activity";
    const result=entry.result||entry.status||"";
    item.textContent=`${name}: ${typeof result==="string"?result:JSON.stringify(result)}`;
    activityList.appendChild(item);
  });
}

async function sendMessage(rawText){
  const message=rawText.trim();
  if(!message)return;
  addMessage("user",message);
  conversationHistory.push({role:"user",content:message});
  messageInput.value="";
  sendButton.disabled=true;
  typingIndicator.hidden=false;
  try{
    const response=await fetch("/api/chat",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({message:message,history:conversationHistory.slice(-8)})
    });
    const data=await response.json();
    if(!response.ok)throw new Error(data.detail||data.error||"The server could not process the request.");
    const answer=data.answer||"The assistant returned an empty response.";
    addMessage("assistant",answer);
    conversationHistory.push({role:"assistant",content:answer});
    conversationHistory=conversationHistory.slice(-8);
    showActivity(data.trace||data.activity||[]);
  }catch(error){
    addMessage("assistant",`Sorry, something went wrong: ${error.message}`);
    showActivity([]);
  }finally{
    typingIndicator.hidden=true;
    sendButton.disabled=false;
    messageInput.focus();
  }
}

chatForm.addEventListener("submit",event=>{
  event.preventDefault();
  sendMessage(messageInput.value);
});
document.querySelectorAll(".chip").forEach(chip=>{
  chip.addEventListener("click",()=>sendMessage(chip.dataset.prompt||""));
});
clearButton.addEventListener("click",()=>{
  conversationHistory=[];
  chatMessages.replaceChildren();
  activityList.replaceChildren();
  const item=document.createElement("li");
  item.textContent="No activity yet.";
  activityList.appendChild(item);
  addMessage("assistant","Conversation cleared. I can help with IT policies, assets, tickets, support teams and incident drafts.");
  messageInput.focus();
});
