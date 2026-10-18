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

  // share tabs
  var tabs=document.querySelectorAll('.tabs [data-kind]');
  function setKind(k){
    tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.kind===k)});
    var f=document.querySelector('form[data-upload]'); if(!f)return;
    f.querySelector('[name=kind]').value=k;
    f.querySelectorAll('[data-show]').forEach(function(el){el.style.display=el.dataset.show.split(' ').indexOf(k)>-1?'':'none'});
    var l=f.querySelector('label[for=ss]'); if(l)l.textContent=l.dataset['label'+k[0].toUpperCase()+k.slice(1)]||l.textContent;
  }
  tabs.forEach(function(t){t.addEventListener('click',function(){setKind(t.dataset.kind)})});
  if(tabs.length)setKind('item');

  // generic forms -> Supabase
  document.querySelectorAll('form[data-table]').forEach(function(f){
    f.addEventListener('submit',function(ev){
      ev.preventDefault();
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
          .then(function(r){ if(r&&r.error)throw r.error; f.reset(); if(tabs.length)setKind('item');
            msg(f,'ok','Thank you! Jim has received it and will review it soon.'); })
          .catch(function(e){ console.error(e); msg(f,'err','Sorry — something went wrong. Please try again in a moment.'); });
      });
    });
  });

  // album + comments
  var album=document.getElementById('album'), com=document.getElementById('comments');
  if((album||com)&&ready){ window.HKclient(function(c){
    if(album) c.from('public_album').select('*').order('created_at',{ascending:false}).limit(200).then(function(r){
      if(!r.data||!r.data.length)return; album.innerHTML='';
      r.data.forEach(function(it){
        var url=it.file_path?c.storage.from('album').getPublicUrl(it.file_path).data.publicUrl:null;
        var media=!url?'':(/^video/.test(it.file_type||'')?'<video controls preload="metadata" src="'+url+'"></video>':(/pdf/.test(it.file_type||'')?'<div class="bd"><a href="'+url+'">Open document (PDF)</a></div>':'<img loading="lazy" src="'+url+'" alt="">'));
        var d=document.createElement('div'); d.className='item';
        d.innerHTML=media+'<div class="bd"><h4></h4><p></p><div class="by"></div></div>';
        d.querySelector('h4').textContent=it.title||(it.kind==='hello'?'Hi everyone!':'');
        d.querySelector('p').textContent=it.story||'';
        d.querySelector('.by').textContent=[it.credit_name||it.name,it.year,it.people].filter(Boolean).join(' · ');
        album.appendChild(d);
      });
    });
    if(com) c.from('public_comments').select('*').eq('page','album').order('created_at',{ascending:true}).then(function(r){
      (r.data||[]).forEach(function(x){var d=document.createElement('div');d.className='note';d.innerHTML='<b></b><span></span>';d.querySelector('b').textContent=x.name;d.querySelector('span').textContent=x.body;com.appendChild(d)});
    });
  });}
})();
