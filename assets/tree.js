(function(){
  var el=document.getElementById('tree'); if(!el)return;
  var drawer=document.getElementById('drawer'), dbody=document.getElementById('dbody'), form=document.getElementById('treeform');
  function esc(s){var d=document.createElement('div');d.textContent=s==null?'':s;return d.innerHTML}
  function li(n,depth){
    var has=n.children&&n.children.length, open=depth<1||n.mine;
    var l=document.createElement('li'); if(has&&!open)l.dataset.closed='1';
    var b=document.createElement('button'); b.type='button';
    b.className='node'+(n.private?' priv':'')+(n.mine?' mine':'');
    b.innerHTML='<span class="tg'+(has?'':' none')+'">'+(has?(open?'−':'+'):'')+'</span><span><span class="nm">'+esc(n.name)+'</span> '+(n.years?'<span class="yr">'+esc(n.years)+'</span>':'')+
      (n.spouse&&n.spouse.length?'<br><span class="sp">m. '+esc(n.spouse.join('; '))+'</span>':'')+'</span>'+(n.id===84?' <span class="badge">Site founder</span>':'');
    b.dataset.name=(n.name||'').toLowerCase();
    b.addEventListener('click',function(e){
      if(has&&e.target.closest('.tg')){toggle(l);return;}
      if(has&&!e.target.closest('.tg')&&l.dataset.closed){toggle(l);}
      show(n);
    });
    l.appendChild(b);
    if(has){var u=document.createElement('ul'); if(!open)u.hidden=true; n.children.forEach(function(c){u.appendChild(li(c,depth+1))}); l.appendChild(u);}
    return l;
  }
  function toggle(l,force){var u=l.querySelector(':scope>ul'); if(!u)return; var o=force!==undefined?force:u.hidden; u.hidden=!o; l.dataset.closed=o?'':'1'; var t=l.querySelector(':scope>.node .tg'); if(t)t.textContent=o?'−':'+';}
  function show(n){
    var h='<span class="eyebrow">'+(n.branch?esc(n.branch)+' branch':'Family tree')+'</span><h3>'+esc(n.name)+'</h3>';
    if(n.private) h+='<p class="muted">This relative is living, so their details are private. If this is you, you can choose to be listed.</p>';
    else { if(n.years)h+='<p>'+esc(n.years)+'</p>'; if(n.spouse&&n.spouse.length)h+='<p>Married: '+esc(n.spouse.join('; '))+'</p>'; if(n.place)h+='<p class="muted">Born: '+esc(n.place)+'</p>';
      if(n.children&&n.children.length)h+='<p class="muted">'+n.children.length+' child'+(n.children.length>1?'ren':'')+' in the tree</p>'; }
    dbody.innerHTML=h; form.person_id.value=n.id; form.person_name.value=n.name;
    var m=form.querySelector('.msg'); if(m){m.className='msg';m.textContent='';}
    drawer.classList.add('open'); drawer.setAttribute('aria-hidden','false');
  }
  drawer.querySelector('.x').addEventListener('click',function(){drawer.classList.remove('open');drawer.setAttribute('aria-hidden','true')});
  fetch('/assets/tree.json').then(function(r){return r.json()}).then(function(d){
    el.innerHTML=''; var u=document.createElement('ul'); u.appendChild(li(d.root,0)); el.appendChild(u);
    document.getElementById('anc').innerHTML='<b>Before Detroit (family tradition, from the Saga):</b> '+d.ancestors.slice().reverse().map(esc).join(' → ')+' → <b>Dr. Herman Kiefer</b>. <a href="/story/the-legend">Read the legend →</a><br><span>'+d.count+' descendants and family shown.</span>';
  });
  document.getElementById('texpand').onclick=function(){el.querySelectorAll('li').forEach(function(l){toggle(l,true)})};
  document.getElementById('tcollapse').onclick=function(){el.querySelectorAll('li li').forEach(function(l){toggle(l,false)})};
  document.getElementById('tmine').onclick=function(){el.querySelectorAll('li li').forEach(function(l){toggle(l,false)}); el.querySelectorAll('.node.mine').forEach(function(b){var l=b.parentNode;while(l&&l!==el){if(l.tagName==='LI')toggle(l,true);l=l.parentNode}}); var me=el.querySelector('.badge'); if(me)me.scrollIntoView({behavior:'smooth',block:'center'})};
  var s=document.getElementById('tsearch');
  s.addEventListener('input',function(){var q=s.value.trim().toLowerCase(); el.querySelectorAll('.node').forEach(function(b){b.classList.remove('hit')}); if(q.length<2)return;
    var first=null; el.querySelectorAll('.node').forEach(function(b){ if(b.dataset.name.indexOf(q)>-1){b.classList.add('hit'); var l=b.parentNode.parentNode; while(l&&l!==el){if(l.tagName==='LI')toggle(l,true); l=l.parentNode} first=first||b;}}); if(first)first.scrollIntoView({behavior:'smooth',block:'center'});});
})();
