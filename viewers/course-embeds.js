/* course-embeds.js — shared expander for [data-embed] placeholders in a course page.
   MIRRORS the inline block in pages/course-viewer.html (copied verbatim so a grammar
   rendered as a course matches the MDX course exactly). Fills lineage/timeline/people/
   decks/suits/numbers/card/trumps-synthesis/trumps-detail/suits-detail/essay/plates/
   apparatus from the deck grammars + research/synthesis. Relative paths (../tarot,
   ../research, ../viewers/...) resolve identically from pages/ and viewers/, so this
   works in BOTH course-viewer and grammar-course. Pass the rendered course root in. */
window.expandCourseEmbeds = async function(root){
  if(!root) return;
                  const T='../tarot', RES='../research';
                  const esc=s=>String(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
                  const mdl=s=>esc(String(s||'').replace(/\s*\[@[^\]]+\]/g,''))  // drop [@citation] keys
                    .replace(/`([^`]+)`/g,'<code>$1</code>')                       // inline code
                    .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/\*(.+?)\*/g,'<em>$1</em>').replace(/\*+/g,'')
                    .replace(/\[([^\]]+)\]\(([^)]+)\)/g,(m,t,h)=>`<a href="${h}"${h.startsWith('#')?'':' target="_blank" rel="noopener noreferrer"'}>${t}</a>`)
                    .replace(/\n{2,}/g,'</p><p>').replace(/\n/g,'<br>');
                  const get=async u=>{ try{ return await (await fetch(u)).json(); }catch(e){ return null; } };
                  // live viewers
                  root.querySelectorAll('[data-embed="lineage"],[data-embed="timeline"]').forEach(el=>{
                    const w=el.dataset.embed;
                    const src=(w==='lineage'?'../viewers/genealogy-tree.html':'../viewers/timeline.html')+'?embed=1';
                    const label=w==='lineage'?'The Lineage of Tarot':'Timeline · 1440s–1900s';
                    const fig=w==='lineage'?'../print/book/figures/lineage.png':'../print/book/figures/timeline.png';
                    el.innerHTML=`<figure class="tarot-embed"><div class="viewer-frame screen-only"><iframe loading="lazy" title="${label}" src="${src}"></iframe></div><div class="print-figure"><img src="${fig}" alt="${label}"></div><figcaption>${label}. Interactive on screen; a static plate in print.</figcaption></figure>`;
                  });
                  // embeds report their full content height (?embed=1) so they render whole, no inner scroll
                  if(!window.__tarotEmbedHeightHooked){ window.__tarotEmbedHeightHooked=true;
                    window.addEventListener('message',e=>{ if(!e.data||e.data.type!=='tarotEmbedHeight')return;
                      document.querySelectorAll('.viewer-frame iframe').forEach(f=>{ if(f.contentWindow===e.source) f.style.height=Math.max(320,e.data.h)+'px'; }); }); }
                  // people — the weave + a who's-who organised BY ROLE (deck-specific makers
                  // are woven into the deck chapters instead).
                  const peopleEls=[...root.querySelectorAll('[data-embed="people"]')];
                  let PG=null, makersByDeck={}, scholarsByDeck={};
                  if(peopleEls.length || root.querySelector('[data-embed="decks"]')){
                    PG=await get(T+'/people-of-tarot/grammar.json');
                    if(PG) for(const p of PG.items){ if((p.metadata||{}).kind==='person'||p.category==='person'){
                      for(const s of ((p.metadata||{}).made||[])) (makersByDeck[s]=makersByDeck[s]||[]).push(p);
                      for(const s of ((p.metadata||{}).studied||[])) (scholarsByDeck[s]=scholarsByDeck[s]||[]).push(p); } }
                  }
                  if(peopleEls.length && PG){
                    const items=Object.fromEntries(PG.items.map(i=>[i.id,i]));
                    const r3=items['root-people-of-tarot'];
                    let html=''; if(r3)html+='<div class="people-weave"><p>'+mdl((r3.sections||{})['What it is'])+'</p></div>';
                    for(const gid of ['grp-makers','grp-patrons','grp-occultists','grp-scholars','grp-institutions']){ const grp=items[gid]; if(!grp)continue;
                      html+='<h3>'+esc(grp.name)+'</h3>'; const wt=(grp.sections||{})['What this groups']; if(wt)html+='<p>'+mdl(wt)+'</p>';
                      for(const cid of grp.composite_of||[]){ const p=items[cid]; if(!p)continue;
                        const who=((p.sections||{}).Who||'').replace(/\s*\[@[^\]]+\]/g,''); const life=(p.metadata||{}).lifespan||'';
                        html+=`<div class="bio"><div class="bio-name">${esc(p.name)}${life?` <span class="bio-life">${esc(life)}</span>`:''}</div><div class="bio-text"><p>${mdl(who)}</p></div></div>`;
                      }
                    }
                    peopleEls.forEach(el=>el.innerHTML=html);
                  }
                  // per-deck chapters (Part II) — overview + the hands behind each deck
                  const deckEls=[...root.querySelectorAll('[data-embed="decks"]')];
                  if(deckEls.length){
                    const col=await get(T+'/_collection.json');
                    const mdBlock=t=>String(t||'').split(/\n{2,}/).map(b=>{ b=b.trim();
                      return /^#{1,3}\s/.test(b)?'<h4>'+esc(b.replace(/^#+\s*/,''))+'</h4>':(b?'<p>'+mdl(b)+'</p>':''); }).join('');
                    let html='';
                    if(col){ for(const g of col.grammars.filter(x=>!x.is_meta).sort((a,b)=>(a.year||9999)-(b.year||9999))){
                      const dg=await get(T+'/'+g.slug+'/grammar.json'); if(!dg)continue;
                      const sigs=dg.items.filter(i=>(i.level||1)===1 && (i.image_url||(i.metadata||{}).image_url)).map(i=>i.image_url||(i.metadata||{}).image_url);
                      const cover=g.cover_image_url||sigs[0];
                      const cells=sigs.slice(1,9).map(im=>`<figure class="c"><img loading="lazy" src="${esc(im)}"></figure>`).join('');
                      let makers='';
                      for(const p of (makersByDeck[g.slug]||[])){ const who=((p.sections||{}).Who||'').replace(/\s*\[@[^\]]+\]/g,'').split('. ')[0]; const life=(p.metadata||{}).lifespan||'';
                        makers+=`<p class="maker"><strong>${esc(p.name)}${life?' ('+esc(life)+')':''}</strong> — ${mdl(who.slice(0,240))}.</p>`; }
                      if(makers)makers='<div class="made-by"><h4>The hands behind it</h4>'+makers+'</div>';
                      const sch=(scholarsByDeck[g.slug]||[]).map(p=>esc(p.name)).join(' · ');
                      if(sch)makers+='<div class="made-by"><h4>Studied by</h4><p class="maker">'+sch+'</p></div>';
                      html+=`<section class="deck-chapter" id="deck-${g.slug}"><h3>${esc((g.name||g.slug).split(' — ')[0])}${g.year_label?' · '+esc(g.year_label):''}</h3>${cover?`<img class="deck-cover" src="${esc(cover)}">`:''}${mdBlock(dg.description)}${makers}${cells?`<div class="strip">${cells}</div>`:''}</section>`;
                    } }
                    deckEls.forEach(el=>el.innerHTML=html);
                  }
                  // the four suits (Minor Arcana) — intro + per-suit synthesis + pip→scenic strip
                  const suitEls=[...root.querySelectorAll('[data-embed="suits"]')];
                  if(suitEls.length){
                    const suits=await get(RES+'/synthesis/suits.json');
                    const CANON={cups:'cups',coins:'coins',swords:'swords',batons:'batons',wands:'batons',pentacles:'coins',disks:'coins',staves:'batons',clubs:'batons'};
                    const SORDER=['batons','coins','swords','cups'], STITLE={batons:'Batons (Wands)',coins:'Coins (Pentacles)',swords:'Swords',cups:'Cups'};
                    const ANCH=['tarot-de-marseille-conver','sola-busca-tarot','golden-dawn-book-t-tarot','visconti-sforza-tarot'];
                    const sidx={};
                    for(const slug of ANCH){ const dg=await get(T+'/'+slug+'/grammar.json'); if(!dg)continue;
                      for(const it of dg.items){ const s=(it.metadata||{}).suit, img=it.image_url||(it.metadata||{}).image_url;
                        if(s&&img){ const cs=CANON[String(s).toLowerCase()]; if(cs){ (sidx[cs]=sidx[cs]||{}); (sidx[cs][slug]=sidx[cs][slug]||[]).push(img); } } } }
                    let html=suits?`<p>${mdl(suits._intro)}</p>`:'';
                    for(const cs of SORDER){ if(!suits||!suits[cs])continue;
                      const cells=ANCH.flatMap(slug=>((sidx[cs]||{})[slug]||[]).slice(0,5)).map(im=>`<figure class="c"><img loading="lazy" src="${esc(im)}"></figure>`).join('');
                      html+=`<section class="card-chapter"><h3>The Suit of ${esc(STITLE[cs])}</h3><div class="synthbox"><p>${mdl(suits[cs])}</p></div><div class="strip">${cells}</div></section>`;
                    }
                    suitEls.forEach(el=>el.innerHTML=html);
                  }
                  // the numbers (pips Ace–Ten) — one shared meaning per number across the suits
                  // (the Golden Dawn laid the ten pips over the ten Sephiroth). synthesis + cross-suit strip.
                  const numEls=[...root.querySelectorAll('[data-embed="numbers"]')];
                  if(numEls.length){
                    const nums=await get(RES+'/synthesis/numbers.json');
                    const RANKW={ace:1,one:1,two:2,three:3,four:4,five:5,six:6,seven:7,eight:8,nine:9,ten:10};
                    const CANON2={cups:'Cups',coins:'Coins',pentacles:'Coins',disks:'Coins',swords:'Swords',batons:'Batons',wands:'Batons',staves:'Batons',clubs:'Batons'};
                    const SUITORDER=['Batons','Coins','Swords','Cups'];
                    const nidx={};
                    for(const slug of ['golden-dawn-book-t-tarot']){ const dg=await get(T+'/'+slug+'/grammar.json'); if(!dg)continue;
                      for(const it of dg.items){ const md=it.metadata||{}; let n=md.number; const arch=String(md.archetype||'');
                        const m=arch.match(/card:(.+?)-of-(.+)/); if(n==null&&m)n=RANKW[m[1].toLowerCase()];
                        const suit=md.suit||(m&&m[2]); const cs=suit&&CANON2[String(suit).toLowerCase()];
                        if(!n||n>10||!cs)continue; const img=it.image_url||md.image_url;
                        (nidx[n]=nidx[n]||{})[cs]={img,title:md.golden_dawn_title||'',item:it.id,slug}; } }
                    let html=nums&&nums._intro?`<p>${mdl(nums._intro)}</p>`:'';
                    for(let n=1;n<=10;n++){ if(!nums||!nums[n])continue;
                      const cells=SUITORDER.map(cs=>{const c=(nidx[n]||{})[cs];if(!c||!c.img)return '';
                        return `<a class="c" href="../viewers/cards.html?src=../tarot/${c.slug}/grammar.json&item=${encodeURIComponent(c.item)}" title="${esc(c.title)}"><img loading="lazy" src="${esc(c.img)}"><div>${esc(cs)}</div></a>`;}).join('');
                      const tm=String(nums[n]).match(/^\*\*(.+?)\*\*\s*/); const head=tm?tm[1]:('Number '+n); const body=tm?String(nums[n]).slice(tm[0].length):String(nums[n]);
                      html+=`<section class="card-chapter"><h3>${esc(head)}</h3><div class="synthbox"><p>${mdl(body)}</p></div><div class="strip">${cells}</div></section>`;
                    }
                    numEls.forEach(el=>el.innerHTML=html);
                  }
                  // card chapter: synthesis + cross-deck image strip
                  const cardEls=[...root.querySelectorAll('[data-embed="card"]')];
                  if(cardEls.length){
                    const syn=await get(RES+'/synthesis/trumps.json'); const col=await get(T+'/_collection.json');
                    for(const el of cardEls){
                      const tk=el.dataset.trump; if(!tk) continue;
                      let html='<div class="synthbox"><p>'+mdl((syn&&syn[tk])||'')+'</p></div><div class="strip">';
                      if(col){ const cells=[];
                        for(const g of col.grammars.filter(x=>!x.is_meta)){ const dg=await get(T+'/'+g.slug+'/grammar.json'); if(!dg)continue;
                          const it=dg.items.find(i=>(i.metadata||{}).trump_key===tk); const img=it&&(it.image_url||(it.metadata||{}).image_url);
                          const dname=(g.name||g.slug).split(' — ')[0];
                          // each card links to its detail view in that deck (history-only static viewer)
                          const url=`../viewers/cards.html?src=../tarot/${g.slug}/grammar.json&item=${encodeURIComponent(it?it.id:'')}`;
                          if(img) cells.push({y:g.year||9999,h:`<a class="c" href="${url}" title="Open the ${esc(dname)} card"><img loading="lazy" src="${esc(img)}"><div>${esc(dname.slice(0,14))}</div></a>`});
                        }
                        cells.sort((a,b)=>a.y-b.y); html+=cells.map(c=>c.h).join('');
                      }
                      html+='</div>';
                      const lbl=tk.replace(/-/g,' ').replace(/\b\w/g,c=>c.toUpperCase());
                      html+=`<p class="card-links screen-only"><a href="../viewers/prototypes/lenses.html?card=${encodeURIComponent(tk)}">See ${esc(lbl)} across every deck in Lenses →</a> · <a href="https://flow.recursive.eco" target="_blank" rel="noopener">Get a reading at recursive.eco →</a></p>`;
                      el.innerHTML=html;
                    }
                  }
                  // trump chapters — fetch each deck ONCE, build a trump→entries index (with sections).
                  // FRONT: trumps-synthesis (synthesis + strip). CATALOGUE: trumps-detail (per-deck Scenes + later readings).
                  const synEls=[...root.querySelectorAll('[data-embed="trumps-synthesis"]')];
                  const detEls=[...root.querySelectorAll('[data-embed="trumps-detail"]')];
                  const sdetEls=[...root.querySelectorAll('[data-embed="suits-detail"]')];
                  if(synEls.length||detEls.length||sdetEls.length){
                    const syn=await get(RES+'/synthesis/trumps.json'); const col=await get(T+'/_collection.json');
                    const ORDER=['fool','magician','high-priestess','empress','emperor','hierophant','lovers','chariot','strength','hermit','wheel-of-fortune','justice','hanged-man','death','temperance','devil','tower','star','moon','sun','judgement','world'];
                    const NUM={}; ORDER.forEach((k,i)=>NUM[k]=i);
                    const CANON={cups:'cups',coins:'coins',swords:'swords',batons:'batons',wands:'batons',pentacles:'coins',disks:'coins',staves:'batons',clubs:'batons'};
                    const idx={}, midx={};
                    if(col){ for(const g of col.grammars.filter(x=>!x.is_meta)){ const dg=await get(T+'/'+g.slug+'/grammar.json'); if(!dg)continue;
                      for(const it of dg.items){ const md=it.metadata||{}; const img=it.image_url||md.image_url;
                        // group minors by the canonical minor_key (e.g. four-of-coins) so the same card
                        // lines up across decks regardless of suit/court naming; archetype is a fallback.
                        const mk=md.minor_key||(String(md.archetype||'').match(/^card:(.+)/)||[])[1];
                        if(mk&&(md.arcana==='minor'||md.suit||md.minor_key)){
                          (midx[mk]=midx[mk]||[]).push({slug:g.slug,name:(g.name||g.slug).split(' — ')[0],year:g.year||9999,img,sections:it.sections||{}}); }
                        const tk=md.trump_key; if(!tk)continue;
                        (idx[tk]=idx[tk]||[]).push({slug:g.slug,name:(g.name||g.slug).split(' — ')[0],year:g.year||9999,id:it.id,img,sections:it.sections||{}}); } } }
                    const attr=v=>{const m=String(v||'').match(/^\s*\[([^\]]{3,200})\]/);return m?m[1].trim():null;};
                    const ayear=a=>{const m=(a||'').match(/\b(1[0-9]{3}|20[0-9]{2})\b/);return m?+m[1]:9999;};
                    const lbl=tk=>tk.replace(/-/g,' ').replace(/\b\w/g,c=>c.toUpperCase());
                    if(synEls.length){ let html='';
                      for(const tk of ORDER){ if(!syn||!syn[tk])continue;
                        const cells=(idx[tk]||[]).filter(c=>c.img).sort((a,b)=>a.year-b.year).map(c=>`<a class="c" href="../viewers/cards.html?src=../tarot/${c.slug}/grammar.json&item=${encodeURIComponent(c.id)}"><img loading="lazy" src="${esc(c.img)}"><div>${esc(c.name.slice(0,14))}</div></a>`).join('');
                        html+=`<div class="card-chapter"><h3>${NUM[tk]} — ${esc(lbl(tk))}</h3><div class="synthbox"><p>${mdl(syn[tk])}</p></div><div class="strip">${cells}</div><p class="card-links screen-only"><a href="../viewers/prototypes/lenses.html?card=${tk}">See ${esc(lbl(tk))} across every deck in Lenses →</a> · <a href="https://flow.recursive.eco" target="_blank" rel="noopener">Get a reading at recursive.eco →</a></p></div>`;
                      }
                      synEls.forEach(el=>el.innerHTML=html);
                    }
                    if(detEls.length){ const ANCH=['cary-yale-visconti-tarot','visconti-sforza-tarot','charles-vi-tarot','este-tarot']; let html='';
                      for(const tk of ORDER){ if(!syn||!syn[tk])continue;
                        const ents=(idx[tk]||[]).sort((a,b)=>a.year-b.year);
                        const entryOf=slug=>ents.find(x=>x.slug===slug);
                        const sceneOf=c=>{if(!c)return null;const s=c.sections;return s.Scene||s.About||s.Iconography;};
                        const early=ANCH.find(s=>sceneOf(entryOf(s))); let ind='', drow=0;
                        for(const slug of [early,'tarot-de-marseille-conver','golden-dawn-book-t-tarot']){ if(!slug)continue; const c=entryOf(slug); const sc=sceneOf(c); if(!sc)continue;
                          const g=col.grammars.find(x=>x.slug===slug);
                          const thumb=c.img?`<a class="cardthumb" href="../viewers/cards.html?src=../tarot/${slug}/grammar.json&item=${encodeURIComponent(c.id)}"><img loading="lazy" src="${esc(c.img)}"></a>`:'';
                          ind+=`<div class="indeck-row${drow++%2?' flip':''}">${thumb}<div class="indeck-text"><strong>${esc((g.name||slug).split(' — ')[0])} · ${g.year||''}.</strong> ${mdl(sc.slice(0,520))}${sc.length>520?'…':''}</div></div>`; }
                        if(ind)ind='<h4>In the decks</h4>'+ind;
                        const later=[],seen=new Set();
                        for(const c of ents)for(const v of Object.values(c.sections)){const a=attr(v);if(!a)continue;const voice=a.split(',')[0].trim();if(seen.has(voice))continue;seen.add(voice);later.push([ayear(a),a,String(v).replace(/^\s*\[[^\]]*\]\s*/,'')]);}
                        later.sort((a,b)=>a[0]-b[0]); let lat='';
                        for(const [,a,body] of later)lat+=`<div class="later"><div class="later-src">${esc(a)}</div><p>${mdl(body.slice(0,760))}${body.length>760?'…':''}</p></div>`;
                        if(lat)lat='<h4>Later readings</h4>'+lat;
                        const ov=syn[tk]?`<div class="synthbox"><p>${mdl(syn[tk])}</p></div>`:'';
                        if(ind||lat)html+=`<div class="card-chapter"><h3>${NUM[tk]} — ${esc(lbl(tk))}</h3>${ov}${ind}${lat}</div>`;
                      }
                      detEls.forEach(el=>el.innerHTML=html);
                    }
                    if(sdetEls.length){
                      const RANK={ace:1,one:1,two:2,three:3,four:4,five:5,six:6,seven:7,eight:8,nine:9,ten:10,page:11,knave:11,valet:11,jack:11,princess:11,knight:12,cavalier:12,prince:12,queen:13,king:14};
                      const SORDER=['batons','coins','swords','cups'], STITLE={batons:'Batons (Wands)',coins:'Coins (Pentacles)',swords:'Swords',cups:'Cups'};
                      const SANCH=['sola-busca-tarot','tarot-de-marseille-conver','golden-dawn-book-t-tarot'];
                      const parts=a=>{const m=String(a||'').match(/^(?:card:)?(.+?)-of-(.+)/);if(!m)return null;const cs=CANON[m[2]]||m[2];return{rank:m[1],cs,ro:RANK[m[1]]||50};};
                      const bySuit={};
                      for(const arch of Object.keys(midx)){const p=parts(arch);if(!p)continue;(bySuit[p.cs]=bySuit[p.cs]||[]).push([p.ro,p.rank,arch]);}
                      let html='';
                      for(const cs of SORDER){ const cards=(bySuit[cs]||[]).sort((a,b)=>a[0]-b[0]); if(!cards.length)continue;
                        html+=`<div class="card-chapter" id="suitdetail-${cs}"><h3>The Suit of ${esc(STITLE[cs])}</h3>`;
                        for(const [ro,rank,arch] of cards){ const ents=(midx[arch]||[]).sort((a,b)=>a.year-b.year);
                          const sceneOf=slug=>{const c=ents.find(x=>x.slug===slug);if(!c)return null;const s=c.sections;return s.Scene||s.Description||s.About||s.Iconography;};
                          let ind='',repimg='';for(const slug of SANCH){const sc=sceneOf(slug);if(sc){const g=col.grammars.find(x=>x.slug===slug);const c=ents.find(x=>x.slug===slug);if(c&&c.img)repimg=c.img;ind=`<span class="mscene"><strong>${esc((g.name||slug).split(' — ')[0])}:</strong> ${mdl(sc.slice(0,300))}${sc.length>300?'…':''}</span>`;break;}}
                          if(!repimg){const wi=ents.find(x=>x.img);if(wi)repimg=wi.img;}
                          const later=[],seen=new Set();
                          for(const c of ents)for(const v of Object.values(c.sections)){const a=attr(v);if(!a)continue;const voice=a.split(',')[0].trim();if(seen.has(voice))continue;seen.add(voice);later.push([ayear(a),a,String(v).replace(/^\s*\[[^\]]*\]\s*/,'')]);}
                          later.sort((a,b)=>a[0]-b[0]); let rd='';
                          if(later.length){const [,a,body]=later[0];rd=`<span class="mread"><em>${esc(a.split(',')[0])}</em> — ${mdl(body.slice(0,240))}${body.length>240?'…':''}</span>`;}
                          const rl=(rank||'').replace(/-/g,' ').replace(/\b\w/g,c=>c.toUpperCase());
                          const badge=(ro>=1&&ro<=10)?String(ro):esc(rl.charAt(0));
                          const imgh=repimg?`<div class="minor-img"><img loading="lazy" src="${esc(repimg)}"></div>`:'';
                          html+=`<div class="minor-card"><div class="minor-head"><span class="rank-num">${badge}</span><strong>${esc(rl)} of ${esc(STITLE[cs].split(' ')[0])}</strong></div><div class="minor-body">${ind} ${rd}</div>${imgh}</div>`;
                        }
                        html+='</div>';
                      }
                      sdetEls.forEach(el=>el.innerHTML=html);
                    }
                  }
                  // the Divination Question essay — from the meta grammar (single source)
                  const essayEls=[...root.querySelectorAll('[data-embed="essay"]')];
                  if(essayEls.length){
                    const mg=await get(T+'/all-decks-many-lenses/grammar.json');
                    const e=mg&&mg.items.find(i=>i.id==='essay-divination-question');
                    let html=''; if(e)for(const [k,v] of Object.entries(e.sections||{}))html+=`<h3>${esc(k)}</h3><p>${mdl(v)}</p>`;
                    essayEls.forEach(el=>el.innerHTML=html);
                  }
                  // full-page plates (front gallery)
                  const plateEls=[...root.querySelectorAll('[data-embed="plates"]')];
                  if(plateEls.length){
                    // Part 1 — one card across the centuries: Death. The skeleton persists ~460 years
                    // while the scene around it is rebuilt each time (the 'painted fossil').
                    const DEATH=[
                      ['visconti-sforza-tarot','tk:death','Death — Visconti-Sforza, Milan, c. 1451. The earliest clear tarot Death: a white skeleton standing frontally on a gold ground, holding a bow and arrow.'],
                      ['tarot-de-marseille-conver','tk:death','Death — Tarot de Marseille (Conver), 1760. Three centuries on, the same skeleton now mows a field of severed body parts with a scythe — and the card is left pointedly untitled.'],
                      ['golden-dawn-book-t-tarot','tk:death','Death — Rider-Waite-Smith line, 1909. The skeleton survives the whole journey but is restaged once more: an armoured rider on a pale horse beneath a rising sun.']];
                    // Part 2 — continuity (the Fool, recognisable for 460 years) + diversity (how far the family spreads).
                    const ICONS=[
                      ['visconti-sforza-tarot','tk:fool','The Fool — Visconti-Sforza, c. 1451. A ragged wanderer; the figure scarcely changes for five centuries.'],
                      ['tarot-de-marseille-conver','tk:fool','Le Mat — Marseille (Conver), 1760. The same vagabond and his nipping dog, now in woodcut.'],
                      ['golden-dawn-book-t-tarot','tk:fool','The Fool — Rider-Waite-Smith line, 1909. Still the wanderer, stepping off a cliff into the modern deck.'],
                      ['mamluk-deck','item:cups-king','Mamluk card, 14th–15th c. Egypt/Syria — the four-suit ancestor that reached Europe in the 1370s.'],
                      ['sola-busca-tarot','item:cups-05','Sola Busca, 1491 — the first deck to give every numbered pip a figured scene, four centuries before the RWS.'],
                      ['mantegna-tarocchi','item:plate-01','The "Mantegna Tarocchi", c. 1465 — a humanist set of ranks and virtues, not a tarot at all: a cousin, not a parent.'],
                      ['visconti-sforza-tarot','tk:world','The World — Visconti-Sforza, c. 1451. Tooled gold leaf for a ducal court: tarot began as luxury, not occultism.'],
                      ['tarot-de-marseille-conver','tk:moon','The Moon — Marseille, 1760. The uncanny scene of towers, dogs, and crayfish the occultists inherited whole.']];
                    const resolve=(dg,spec)=> spec.startsWith('tk:') ? dg.items.find(i=>(i.metadata||{}).trump_key===spec.slice(3))
                      : spec.startsWith('item:') ? dg.items.find(i=>i.id===spec.slice(5))
                      : dg.items.find(i=>i.image_url||(i.metadata||{}).image_url);
                    async function gallery(list){ let h='';
                      for(const [slug,spec,cap] of list){ const dg=await get(T+'/'+slug+'/grammar.json'); if(!dg)continue;
                        const it=resolve(dg,spec); const img=it&&(it.image_url||(it.metadata||{}).image_url); if(!img)continue;
                        const href=`../viewers/cards.html?src=${encodeURIComponent('../tarot/'+slug+'/grammar.json')}&item=${encodeURIComponent(it.id)}`;
                        h+=`<figure class="plate"><a href="${href}"><img loading="lazy" src="${esc(img)}"></a><figcaption>${esc(cap)}</figcaption></figure>`; }
                      return h; }
                    const html=`<div class="plates-h">One card across the centuries — Death</div><div class="plate-row">${await gallery(DEATH)}</div>`
                      +`<div class="plates-h">Continuity &amp; diversity — a few iconic cards</div><div class="plate-grid">${await gallery(ICONS)}</div>`;
                    plateEls.forEach(el=>el.innerHTML=html);
                  }
                  // apparatus: image credits + bibliography + colophon
                  const appEls=[...root.querySelectorAll('[data-embed="apparatus"]')];
                  if(appEls.length){
                    const col=await get(T+'/_collection.json');
                    let cred='<h3>Image credits</h3><p>Every card image here is in the <strong>public domain</strong> — the originals all predate the twentieth century. Reproductions are drawn from the institutions and archives below; full per-card provenance is in the research dossiers on GitHub.</p><ul class="credits">';
                    if(col){ for(const g of col.grammars.filter(x=>!x.is_meta).sort((a,b)=>(a.year||9999)-(b.year||9999))){
                      const dg=await get(T+'/'+g.slug+'/grammar.json');
                      const credit=(dg&&dg.image_credit)||[...new Set((dg?dg.items:[]).map(i=>(i.metadata||{}).collection).filter(Boolean))].join('; ')||'public domain — see the deck dossier';
                      cred+=`<li><strong>${esc((g.name||g.slug).split(' — ')[0])}.</strong> ${esc(credit)}.</li>`;
                    } }
                    cred+='</ul>';
                    let bib='';
                    try{ const txt=await (await fetch('../research/bibliography.bib')).text();
                      const rows=[]; const re2=/@\w+\s*\{[^,]+,([\s\S]*?)\n\}/g; let m;
                      while((m=re2.exec(txt))){ const b=m[1]; const f=n=>{const mm=new RegExp(n+'\\s*=\\s*[{"]([^}"]*)[}"]','i').exec(b);return mm?mm[1].trim():'';};
                        const au=f('author')||f('editor'),ti=f('title'),yr=f('year'); if(ti)rows.push([au,ti,yr]); }
                      rows.sort((a,b)=>(a[0].toLowerCase()+a[2]).localeCompare(b[0].toLowerCase()+b[2]));
                      bib=rows.map(([au,ti,yr])=>`<p class="bibentry">${au?esc(au)+'. ':''}<em>${esc(ti)}</em>${yr?' ('+esc(yr)+')':''}.</p>`).join('');
                    }catch(e){}
                    appEls.forEach(el=>el.innerHTML=cred+'<h3>Sources &amp; further reading</h3><div class="bib">'+bib+'</div><h3>About this book</h3><p>Generated from the open data of <strong>The Recursive Tarot</strong> — a public-domain collection of historical tarot grammars. Text CC-BY-SA-4.0; card images public domain. Source: github.com/PlayfulProcess/recursive-tarot.</p>');
                  }
};
