/* One reusable search/filter behavior for Publications and Study Notes; no frameworks or network calls. */
(() => {
 const normalize=(s)=>String(s||'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase().replace(/[–—-]/g,' ').replace(/\s+/g,' ').trim();
 document.querySelectorAll('[data-search-controls]').forEach(controls=>{
   const id=controls.dataset.searchControls;
   const root=document.querySelector(`[data-search-root="${id}"]`);
   if(!root)return;
   const search=controls.querySelector('[data-text-filter]');
   const areas=[...controls.querySelectorAll('[data-area-filter]')];
   const keywords=[...controls.querySelectorAll('[data-keyword-filter]')];
   const items=[...root.querySelectorAll('[data-filter-item]')];
   const itemData=items.map(item=>({item,hay:normalize(item.dataset.search),tags:(item.dataset.keywords||'').split('|')}));
   const groups=[...root.querySelectorAll('[data-filter-group]')];
   const counter=root.querySelector('[data-result-count]');
   const empty=root.querySelector('[data-empty-state]');
   const reset=root.querySelector('[data-filter-reset]');
   let area='all', keyword='all';
   function update(){
     const terms=normalize(search.value).split(' ').filter(Boolean);
     let visible=0;
     for(const {item,hay,tags} of itemData){
       const ok=(area==='all'||(item.dataset.area||'').split('|').includes(area))&&(keyword==='all'||tags.includes(keyword))&&terms.every(t=>hay.includes(t));
       item.hidden=!ok;if(ok)visible++;
     }
     for(const group of groups)group.hidden=![...group.querySelectorAll('[data-filter-item]')].some(i=>!i.hidden);
     for(const b of areas)b.setAttribute('aria-pressed',String(b.dataset.areaFilter===area));
     for(const b of keywords)b.setAttribute('aria-pressed',String(b.dataset.keywordFilter===keyword));
     if(counter)counter.textContent=`${visible} ${id==='notes'?(visible===1?'note':'notes'):(visible===1?'publication':'publications')}`;
     if(empty)empty.hidden=visible!==0;
   }
   areas.forEach(b=>b.addEventListener('click',()=>{area=b.dataset.areaFilter;update();}));
   keywords.forEach(b=>b.addEventListener('click',()=>{keyword=b.dataset.keywordFilter;update();}));
   search.addEventListener('input',update);
   if(reset)reset.addEventListener('click',()=>{area='all';keyword='all';search.value='';update();search.focus();});
   update();
 });
})();
