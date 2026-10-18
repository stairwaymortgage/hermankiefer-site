(function(){
  var root=document.getElementById('admin'); if(!root)return;
  if(!(window.HK&&window.HK.url)){root.innerHTML='<p>The database is not connected yet.</p>';return;}
  function esc(s){var d=document.createElement('div');d.textContent=s==null?'':s;return d.innerHTML}
  window.HKclient(function(c){
    var lf=document.getElementById('login');
    lf.addEventListener('submit',function(e){e.preventDefault(); c.auth.signInWithOtp({email:lf.querySelector('input').value,options:{emailRedirectTo:location.origin+'/admin'}}).then(function(r){var m=lf.querySelector('.msg');m.className='msg '+(r.error?'err':'ok');m.textContent=r.error?r.error.message:'Check your email for the sign-in link.'})});
    c.auth.getSession().then(function(s){ if(s.data.session) load(); });
    c.auth.onAuthStateChange(function(ev,s){ if(s&&ev==='SIGNED_IN')load(); });
    function section(t){var h=document.createElement('h2');h.textContent=t;h.style.marginTop='40px';root.appendChild(h);var d=document.createElement('div');root.appendChild(d);return d;}
    function load(){
      root.innerHTML='<p><button class="btn ghost on-paper" id="so">Sign out</button></p>';
      document.getElementById('so').onclick=function(){c.auth.signOut().then(function(){location.reload()})};
      var q=section('Shared items waiting for review');
      c.from('contributions').select('*').eq('status','pending').order('created_at').then(function(r){
        if(!r.data||!r.data.length){q.innerHTML='<p class="muted">Nothing waiting.</p>';return;}
        r.data.forEach(function(it){
          var d=document.createElement('div');d.className='admin-row';
          d.innerHTML='<b>'+esc(it.title||it.kind)+'</b> — '+esc(it.name)+' &lt;'+esc(it.email)+'&gt; · visibility: <b>'+esc(it.visibility)+'</b><br>'+esc(it.story)+'<br><span class="muted">'+esc([it.people,it.year,it.credit_name].filter(Boolean).join(' · '))+'</span><div class="media"></div><div class="acts"><button class="ok">Approve</button><button class="no">Keep private (archive)</button><button class="del">Reject</button></div>';
          if(it.file_path) c.storage.from('uploads').createSignedUrl(it.file_path,3600).then(function(s){ if(!s.data)return; var u=s.data.signedUrl; d.querySelector('.media').innerHTML=/^video/.test(it.file_type)?'<video controls src="'+u+'"></video>':(/^image/.test(it.file_type)?'<img src="'+u+'">':'<a href="'+u+'" target="_blank">Open file</a>'); });
          d.querySelector('.ok').onclick=function(){
            var p=Promise.resolve();
            if(it.file_path&&it.visibility==='public') p=c.storage.from('uploads').copy(it.file_path,it.file_path,{destinationBucket:'album'});
            p.then(function(){return c.from('contributions').update({status:'approved'}).eq('id',it.id)}).then(function(){d.remove()});
          };
          d.querySelector('.no').onclick=function(){c.from('contributions').update({status:'archived'}).eq('id',it.id).then(function(){d.remove()})};
          d.querySelector('.del').onclick=function(){c.from('contributions').update({status:'rejected'}).eq('id',it.id).then(function(){d.remove()})};
          q.appendChild(d);
        });
      });
      var cm=section('Messages & comments');
      c.from('comments').select('*').eq('status','pending').order('created_at').then(function(r){
        if(!r.data||!r.data.length){cm.innerHTML='<p class="muted">Nothing waiting.</p>';return;}
        r.data.forEach(function(x){var d=document.createElement('div');d.className='admin-row';
          d.innerHTML='<b>'+esc(x.name)+'</b> &lt;'+esc(x.email)+'&gt; on <i>'+esc(x.page)+'</i><br>'+esc(x.body)+'<div class="acts">'+(x.page.indexOf('private')<0?'<button class="ok">Publish</button>':'')+'<button class="no">Mark read</button></div>';
          var ok=d.querySelector('.ok'); if(ok)ok.onclick=function(){c.from('comments').update({status:'approved'}).eq('id',x.id).then(function(){d.remove()})};
          d.querySelector('.no').onclick=function(){c.from('comments').update({status:'read'}).eq('id',x.id).then(function(){d.remove()})};
          cm.appendChild(d);});
      });
      var ts=section('Family tree suggestions');
      c.from('tree_suggestions').select('*').eq('status','pending').order('created_at').then(function(r){
        if(!r.data||!r.data.length){ts.innerHTML='<p class="muted">Nothing waiting.</p>';return;}
        r.data.forEach(function(x){var d=document.createElement('div');d.className='admin-row';
          d.innerHTML='<b>'+esc(x.kind)+'</b> on <b>'+esc(x.person_name)+'</b> (#'+esc(x.person_id)+') — '+esc(x.name)+' &lt;'+esc(x.email)+'&gt;<br>'+esc(x.details)+'<div class="acts"><button class="ok">Done</button></div>';
          d.querySelector('.ok').onclick=function(){c.from('tree_suggestions').update({status:'done'}).eq('id',x.id).then(function(){d.remove()})};
          ts.appendChild(d);});
      });
      var mb=section('Family members who joined');
      c.from('members').select('*').order('created_at',{ascending:false}).limit(500).then(function(r){
        if(!r.data||!r.data.length){mb.innerHTML='<p class="muted">No one yet.</p>';return;}
        var t='<table style="width:100%;font-family:var(--sans);font-size:14px;border-collapse:collapse"><tr><th align=left>Name</th><th align=left>Branch / relation</th><th align=left>Contact</th><th align=left>Opt-ins</th></tr>';
        r.data.forEach(function(m){t+='<tr style="border-top:1px solid #ddd"><td>'+esc(m.name)+'</td><td>'+esc(m.branch)+'<br>'+esc(m.relation)+'</td><td>'+esc(m.email)+'<br>'+esc(m.phone)+'</td><td>'+(m.dir_ok?'directory ':'')+(m.digest_ok?'newsletter ':'')+(m.business_ok?'<b>business</b>':'')+'</td></tr>'});
        mb.innerHTML=t+'</table>';
      });
    }
  });
})();
