(function(){
  // mobile menu
  var b=document.querySelector('.menu-btn'),m=document.getElementById('menu');
  if(b)b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o)});

  var cfg=window.HK||{}, ready=!!(cfg.url&&cfg.key), sb=null;
  function client(){ if(sb||!ready||!window.supabase)return sb; sb=window.supabase.createClient(cfg.url,cfg.key); return sb; }
  function loadLib(cb){ if(!ready)return cb(); if(window.supabase)return cb();
    var s=document.createElement('script'); s.src='https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.min.js'; s.onload=cb; document.head.appendChild(s); }
  window.HKclient=function(cb){loadLib(function(){cb(client())})};
  function msg(f,cls,t){var e=f.querySelector('.msg'); if(!e)return; e.className='msg '+cls; e.textContent=t;}
  function uuid(){return (crypto.randomUUID?crypto.randomUUID():Date.now()+'-'+Math.random().toString(16).slice(2))}

  // contribution tabs (item / story / hello / note)
  var panel=document.querySelector('.contrib'), tabs=panel?panel.querySelectorAll('.tabs [data-kind]'):[];
  function setKind(k){
    if(!panel)return; panel.classList.remove('collapsed');
    tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.kind===k)});
    panel.querySelectorAll('form[data-kinds]').forEach(function(f){f.style.display=f.dataset.kinds.split(' ').indexOf(k)>-1?'':'none'});
    var f=panel.querySelector('form[data-upload]'); if(k==='note'||!f)return;
    f.querySelector('[name=kind]').value=k;
    f.querySelectorAll('[data-show]').forEach(function(el){el.style.display=el.dataset.show.split(' ').indexOf(k)>-1?'':'none'});
    var l=f.querySelector('label[for=ss]'); if(l)l.textContent=l.dataset['label'+k[0].toUpperCase()+k.slice(1)]||l.textContent;
  }
  tabs.forEach(function(t){t.addEventListener('click',function(){setKind(t.dataset.kind)})});
  if(panel&&!panel.classList.contains('collapsed'))setKind('item');

  // Also send sign-ups to Jim's CRM (OneFocus), so every relative who joins,
  // registers for the reunion or shares something lands in his contacts.
  // A copy only: the site's own database below is still the record, and a
  // CRM hiccup never blocks or slows the form.
  var CRM_FORMS={members:'join',reunion:'reunion',contributions:'share'};
  function toCRM(f){
    var form=CRM_FORMS[f.dataset.table]; if(!cfg.crm||!form)return;
    try{
      var out={form:form};
      new FormData(f).forEach(function(v,k){ if(k==='file'||typeof v!=='string'||v==='')return; out[k]=v; });
      if(!out.email)return;
      if(!out.name&&out.credit_name)out.name=out.credit_name;
      fetch(cfg.crm,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(out),keepalive:true}).catch(function(){});
    }catch(e){}
  }

  // generic forms -> Supabase
  document.querySelectorAll('form[data-table]').forEach(function(f){
    f.addEventListener('submit',function(ev){
      ev.preventDefault();
      toCRM(f);
      if(!ready){msg(f,'wait','Thank you! This form opens in a few days — please check back soon, or write to Jim through the About page.');return;}
      msg(f,'wait','Sending…');
      var fd=new FormData(f), row={};
      fd.forEach(function(v,k){ if(k==='file')return; if(f.querySelector('[name="'+k+'"][type=checkbox]'))row[k]=true; else row[k]=v; });
      f.querySelectorAll('input[type=checkbox]').forEach(function(c){ if(!(c.name in row))row[c.name]=false; });
      delete row.rights_ok;
      window.HKclient(function(c){
        var file=fd.get('file'), up=Promise.resolve(null);
        if(file&&file.size){
          if(file.size>52428800){msg(f,'err','That file is over 50 MB. Please send a smaller version.');return;}
          var path=uuid()+'-'+file.name.replace(/[^\w.\-]+/g,'_');
          up=c.storage.from('uploads').upload(path,file,{contentType:file.type}).then(function(r){if(r.error)throw r.error;return path;});
        }
        up.then(function(path){ if(path){row.file_path=path;row.file_type=file.type;} return c.from(f.dataset.table).insert(row); })
          .then(function(r){ if(r&&r.error)throw r.error; f.reset(); var cur=panel&&panel.querySelector('.tabs [aria-selected=true]'); if(cur)setKind(cur.dataset.kind);
            msg(f,'ok','Thank you! Jim has received it and will review it soon.'); })
          .catch(function(e){ console.error(e); msg(f,'err','Sorry — something went wrong. Please try again in a moment.'); });
      });
    });
  });

  // album + comments
  var album=document.getElementById('album'), com=document.getElementById('comments');
  function esc(x){var d=document.createElement('div');d.textContent=x==null?'':x;return d.innerHTML}
  if((album||com)&&ready){ window.HKclient(function(c){
    if(album) c.from('public_album').select('*').order('created_at',{ascending:false}).limit(1000).then(function(r){
      var items=(r.data||[]).map(function(it){ it.url=it.file_path?c.storage.from('album').getPublicUrl(it.file_path).data.publicUrl:null;
        it.kindOf=!it.url?'text':(/^video/.test(it.file_type||'')?'video':(/pdf/.test(it.file_type||'')?'pdf':'image')); it.label=it.title||(it.kind==='hello'?'Hi everyone!':'A memory'); return it; });
      if(!items.length)return;
      album.innerHTML=''; var shown=0, PAGE=12, more=document.getElementById('amore');
      document.getElementById('acount').textContent=items.length+(items.length===1?' item':' items');
      var ss=document.getElementById('slideshow'); if(items.some(function(i){return i.kindOf==='image'})) ss.hidden=false;
      function tile(it,i){var b=document.createElement('button');b.type='button';b.className='tile';
        var th=it.kindOf==='image'?'<img loading="lazy" src="'+it.url+'" alt="'+esc(it.label)+'">':it.kindOf==='video'?'<video muted preload="metadata" src="'+it.url+'#t=0.5"></video><span class="play">▶ Video</span>':it.kindOf==='pdf'?'<div class="txt">📄 '+esc(it.label)+'</div>':'<div class="txt">“'+esc((it.story||'').slice(0,140))+((it.story||'').length>140?'…':'')+'”</div>';
        b.innerHTML='<div class="th">'+th+'</div><div class="tc"><div class="tt">'+esc(it.label)+'</div><div class="tb">'+esc([it.year,it.credit_name||it.name].filter(Boolean).join(' · '))+'</div></div>';
        b.onclick=function(){open(i,false)}; return b;}
      function page(){items.slice(shown,shown+PAGE).forEach(function(it,j){album.appendChild(tile(it,shown+j))}); shown=Math.min(items.length,shown+PAGE); more.hidden=shown>=items.length;}
      more.onclick=page; page();
      // lightbox
      var lb=document.getElementById('lb'),stage=document.getElementById('lbstage'),cap=document.getElementById('lbcap'),pos=document.getElementById('lbpos'),play=document.getElementById('lbplay'),speed=document.getElementById('lbspeed'),idx=0,timer=null,list=items;
      function show(){var it=list[idx]; stage.innerHTML=it.kindOf==='image'?'<img src="'+it.url+'" alt="'+esc(it.label)+'">':it.kindOf==='video'?'<video controls autoplay src="'+it.url+'"></video>':it.kindOf==='pdf'?'<a class="btn solid" href="'+it.url+'" target="_blank" rel="noopener">Open the document (PDF)</a>':'<div class="txt">'+esc(it.story)+'</div>';
        cap.innerHTML='<h4>'+esc(it.label)+'</h4>'+(it.story&&it.kindOf!=='text'?'<p>'+esc(it.story)+'</p>':'')+'<small>'+esc([it.people,it.year,it.credit_name||it.name].filter(Boolean).join(' · '))+'</small>';
        pos.textContent=(idx+1)+' of '+list.length;}
      function go(d){idx=(idx+d+list.length)%list.length;show();}
      function stop(){clearInterval(timer);timer=null;play.textContent='▶ Play';}
      function start(){stop();timer=setInterval(function(){go(1)},+speed.value);play.textContent='❚❚ Pause';}
      function open(i,slides){list=slides?items.filter(function(x){return x.kindOf==='image'}):items; idx=slides?0:list.indexOf(items[i]); if(idx<0)idx=0; lb.hidden=false; document.body.style.overflow='hidden'; show(); if(slides)start(); else stop();}
      function close(){stop();lb.hidden=true;stage.innerHTML='';document.body.style.overflow='';}
      document.getElementById('lbprev').onclick=function(){go(-1);if(timer)start()}; document.getElementById('lbnext').onclick=function(){go(1);if(timer)start()};
      document.getElementById('lbclose').onclick=close; play.onclick=function(){timer?stop():start()}; speed.onchange=function(){if(timer)start()};
      ss.onclick=function(){open(0,true)};
      document.addEventListener('keydown',function(e){if(lb.hidden)return; if(e.key==='Escape')close(); if(e.key==='ArrowRight')go(1); if(e.key==='ArrowLeft')go(-1); if(e.key===' '){e.preventDefault();timer?stop():start();}});
      var tx=null; stage.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true}); stage.addEventListener('touchend',function(e){if(tx===null)return;var dx=e.changedTouches[0].clientX-tx; if(Math.abs(dx)>40)go(dx<0?1:-1); tx=null;});
    });
    if(com) c.from('public_comments').select('*').eq('page','album').order('created_at',{ascending:false}).then(function(r){
      var d=r.data||[]; if(!d.length)return; com.innerHTML=''; var n=0,cm=document.getElementById('cmore');
      function more(){d.slice(n,n+8).forEach(function(x){var e=document.createElement('div');e.className='note';e.innerHTML='<b></b><span></span>';e.querySelector('b').textContent=x.name+' · '+new Date(x.created_at).toLocaleDateString();e.querySelector('span').textContent=x.body;com.appendChild(e)}); n+=8; cm.hidden=n>=d.length;}
      cm.onclick=more; more();
    });
  });}
})();
