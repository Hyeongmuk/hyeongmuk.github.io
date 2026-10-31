/* One reusable search/filter behavior for Publications and Study Notes; no frameworks or network calls. */
(() => {
 const normalize=(s)=>String(s||'').normalize('NFKD').replace(/[̀-ͯ]/g,'').toLocaleLowerCase().replace(/[–—-]/g,' ').replace(/\s+/g,' ').trim();
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
   const resetAll=controls.querySelector('[data-filter-reset-all]');
   const keywordSummary=controls.querySelector('[data-keyword-summary]');
   const keywordToggle=controls.querySelector('[data-keyword-toggle]');
   const keywordPanel=controls.querySelector('[data-keyword-panel]');
   // Area headings inside the list repeat the selected tab, so they show only under All.
   const areaHeadings=[...root.querySelectorAll('[data-area-heading]')];
   const areaIds=new Set(areas.map(b=>b.dataset.areaFilter));
   // The selected area lives in the URL (?area=<id>) so a filtered list can be linked and survives Back.
   const fromUrl=new URLSearchParams(location.search).get('area');
   let area=areaIds.has(fromUrl)?fromUrl:'all', keyword='all';
   function syncUrl(){
     const url=new URL(location.href);
     if(area==='all')url.searchParams.delete('area');else url.searchParams.set('area',area);
     history.replaceState(history.state,'',url);
   }
   function update(){
     const terms=normalize(search.value).split(' ').filter(Boolean);
     let visible=0;
     for(const {item,hay,tags} of itemData){
       const ok=(area==='all'||(item.dataset.area||'').split('|').includes(area))&&(keyword==='all'||tags.includes(keyword))&&terms.every(t=>hay.includes(t));
       item.hidden=!ok;if(ok)visible++;
     }
     for(const group of groups)group.hidden=![...group.querySelectorAll('[data-filter-item]')].some(i=>!i.hidden);
     for(const h of areaHeadings)h.hidden=area!=='all';
     for(const b of areas)b.setAttribute('aria-pressed',String(b.dataset.areaFilter===area));
     for(const b of keywords)b.setAttribute('aria-pressed',String(b.dataset.keywordFilter===keyword));
     if(counter)counter.textContent=`${visible} ${id==='notes'?(visible===1?'note':'notes'):(visible===1?'publication':'publications')}`;
     if(empty)empty.hidden=visible!==0;
     if(resetAll)resetAll.hidden=area==='all' && keyword==='all' && !terms.length;
     if(keywordSummary){
       keywordSummary.textContent=keyword==='all'?'Keywords':`Keyword: ${keyword}`;
       keywordToggle.dataset.hasSelection=String(keyword!=='all');
     }
   }
   areas.forEach(b=>b.addEventListener('click',()=>{area=b.dataset.areaFilter;syncUrl();update();}));
   keywords.forEach(b=>b.addEventListener('click',()=>{keyword=b.dataset.keywordFilter;update();}));
   search.addEventListener('input',update);
   if(keywordToggle)keywordToggle.addEventListener('click',()=>{
     const open=keywordToggle.getAttribute('aria-expanded')!=='true';
     keywordToggle.setAttribute('aria-expanded',String(open));keywordPanel.hidden=!open;
   });
   const clear=()=>{area='all';keyword='all';search.value='';syncUrl();update();search.focus();};
   if(reset)reset.addEventListener('click',clear);
   if(resetAll)resetAll.addEventListener('click',clear);
   update();
 });
})();
