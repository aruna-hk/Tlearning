if (document.querySelector(".enrolled > ul").children.length == 0) {
   empty = document.createElement("a")
   empty.textContent = "No record"
   document.querySelector(".enrolled").appendChild(empty)
}
if (document.querySelector(".upnext > ul").children.length == 0) {
   empty = document.createElement("a")
   empty.textContent = "No record"
   document.querySelector(".upnext").appendChild(empty)
}
