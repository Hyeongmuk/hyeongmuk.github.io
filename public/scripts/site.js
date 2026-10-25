(() => {
 const toggle=document.querySelector('.menu-toggle'), menu=document.getElementById('mobile-menu');
 if(!toggle||!menu) return;
 const close=()=>{menu.hidden=true;toggle.setAttribute('aria-expanded','false')};
 toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')==='true';menu.hidden=open;toggle.setAttribute('aria-expanded',String(!open));});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!menu.hidden){close();toggle.focus();}});
 document.addEventListener('click',e=>{if(!menu.contains(e.target)&&!toggle.contains(e.target))close();});
 window.matchMedia('(min-width:761px)').addEventListener('change',e=>{if(e.matches)close();});
})();
