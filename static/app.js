 const textarea = document.querySelector("#mytextarea");
textarea.addEventListener("keyup", e =>{
  textarea.style.height = "40%";
  let scHeight = e.target.scrollHeight;
  textarea.style.height = `${scHeight}px`;
});
