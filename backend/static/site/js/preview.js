/* Built by tools/build_frontend.py */
const header=document.getElementById('siteHeader'); const menu=document.querySelector('.menu-toggle'); const mobile=document.getElementById('mobileNav');
window.addEventListener('scroll',()=>header?.classList.toggle('scrolled',scrollY>30),{passive:true});
menu?.addEventListener('click',()=>mobile?.classList.toggle('open'));
mobile?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>mobile.classList.remove('open')));
const sections=[...document.querySelectorAll('main section[id]')]; const links=[...document.querySelectorAll('.desktop-nav a')];
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){links.forEach(l=>l.classList.toggle('active',l.getAttribute('href')==='#'+e.target.id));}}),{rootMargin:'-40% 0px -50% 0px'}); sections.forEach(s=>io.observe(s));


const reveal=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-visible');reveal.unobserve(e.target);}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>reveal.observe(el));
document.querySelectorAll('.tilt').forEach(card=>card.addEventListener('pointermove',e=>{if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;const r=card.getBoundingClientRect();const x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;card.style.transform=`perspective(800px) rotateX(${-y*5}deg) rotateY(${x*5}deg) translateY(-6px)`;}));
document.querySelectorAll('.tilt').forEach(card=>card.addEventListener('pointerleave',()=>card.style.transform=''));
const parallax=()=>document.querySelectorAll('.hero-ink').forEach((el,i)=>el.style.transform=`translate3d(0,${scrollY*(i+1)*.045}px,0)`); window.addEventListener('scroll',parallax,{passive:true});


// Manual website image loader: missing files keep the built-in fallback visuals.
function initManagedImages(){
  document.querySelectorAll('.managed-image').forEach(img=>{
    if (img.complete && img.naturalWidth) img.classList.add('image-ready');
    img.addEventListener('load',()=>img.classList.add('image-ready'));
  });
}
document.addEventListener('DOMContentLoaded', initManagedImages);


const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');

function setScene(scene, x, y) {
  scene.style.setProperty('--scene-x', `${x}deg`);
  scene.style.setProperty('--scene-y', `${y}deg`);
}

function initScene(scene) {
  const onMove = (event) => {
    if (reduceMotion.matches) return;
    const r = scene.getBoundingClientRect();
    const px = (event.clientX - r.left) / r.width - 0.5;
    const py = (event.clientY - r.top) / r.height - 0.5;
    setScene(scene, -py * 8, px * 10);
    scene.style.setProperty('--pointer-x', `${px * 100}%`);
    scene.style.setProperty('--pointer-y', `${py * 100}%`);
  };
  const reset = () => setScene(scene, 0, 0);
  scene.addEventListener('pointermove', onMove, { passive: true });
  scene.addEventListener('pointerleave', reset);
}

document.querySelectorAll('[data-3d-scene]').forEach(initScene);

document.querySelectorAll('.three-d-card').forEach((card) => {
  const onMove = (event) => {
    if (reduceMotion.matches) return;
    const r = card.getBoundingClientRect();
    const px = (event.clientX - r.left) / r.width - 0.5;
    const py = (event.clientY - r.top) / r.height - 0.5;
    const depth = Number(card.dataset.tiltDepth || 16);
    card.style.setProperty('--rx', `${-py * 8}deg`);
    card.style.setProperty('--ry', `${px * 10}deg`);
    card.style.setProperty('--tz', `${Math.abs(px) * depth * 0.25 + 6}px`);
    card.style.setProperty('--mx', `${px * 22}px`);
    card.style.setProperty('--my', `${py * 22}px`);
  };
  const reset = () => {
    card.style.setProperty('--rx', '0deg'); card.style.setProperty('--ry', '0deg');
    card.style.setProperty('--tz', '0px'); card.style.setProperty('--mx', '0px'); card.style.setProperty('--my', '0px');
  };
  card.addEventListener('pointermove', onMove, { passive: true });
  card.addEventListener('pointerleave', reset);
});

const tick = () => {
  if (!reduceMotion.matches) {
    document.querySelectorAll('.three-d-stage').forEach((scene) => {
      const t = performance.now() / 1000;
      scene.style.setProperty('--float-a', `${Math.sin(t * 1.2) * 4}px`);
      scene.style.setProperty('--float-b', `${Math.cos(t * 0.9) * 3}px`);
    });
  }
  requestAnimationFrame(tick);
};
requestAnimationFrame(tick);


const counters=[...document.querySelectorAll('[data-counter]')];
const obs=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;const el=e.target,target=+el.dataset.counter;let n=0;const step=Math.max(1,Math.ceil(target/45));const timer=setInterval(()=>{n=Math.min(target,n+step);el.textContent=n+(target===100?'%':'+');if(n>=target)clearInterval(timer);},28);obs.unobserve(el);}),{threshold:.5}); counters.forEach(c=>obs.observe(c));


document.querySelectorAll('.filter').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.filter').forEach(b=>b.classList.remove('active'));btn.classList.add('active');const f=btn.dataset.filter;document.querySelectorAll('.work-card').forEach(card=>{const show=f==='all'||card.dataset.category===f;card.style.display=show?'':'none';});}));


const config = window.RNL_CONFIG || { API_BASE: 'http://127.0.0.1:8000', PREVIEW_FALLBACK: true };
const modal = document.getElementById('quoteModal');
const open = document.getElementById('openQuote');
const form = document.getElementById('quoteForm');
let step = 1;
let products = [];
let selectedProduct = null;
let backendAvailable = false;
const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const MOCK_PRODUCTS = [
  {id:1,name:'Business Cards',slug:'business-cards',category:'print',description:'Premium business cards.',sizes:[{id:1,name:'3.5 × 2 inch'}],papers:[{id:1,name:'300 GSM',gsm:300},{id:2,name:'350 GSM',gsm:350},{id:3,name:'400 GSM',gsm:400}],printing:[{id:1,name:'Single Side'},{id:2,name:'Double Side'}],finishing:[{id:1,name:'Matte Lamination'},{id:2,name:'Gloss Lamination'}]},
  {id:2,name:'Flyers',slug:'flyers',category:'print',description:'Promotional flyers.',sizes:[{id:2,name:'A5'},{id:3,name:'A4'}],papers:[{id:4,name:'130 GSM',gsm:130},{id:5,name:'170 GSM',gsm:170}],printing:[{id:3,name:'Full Color Single Side'},{id:4,name:'Full Color Double Side'}],finishing:[]},
  {id:3,name:'Brochures',slug:'brochures',category:'print',description:'Folded business brochures.',sizes:[{id:4,name:'A4 Tri-fold'},{id:5,name:'A3 Tri-fold'}],papers:[{id:6,name:'170 GSM',gsm:170},{id:7,name:'250 GSM',gsm:250}],printing:[{id:5,name:'Full Color Double Side'}],finishing:[{id:3,name:'Creasing / Folding'}]}
];
function api(path) { return `${String(config.API_BASE || '').replace(/\/$/, '')}${path}`; }
async function apiFetch(path, options = {}) {
  const res = await fetch(api(path), { credentials: 'include', ...options });
  if (!res.ok) { const payload = await res.json().catch(() => ({})); throw new Error(payload.error || `Request failed (${res.status})`); }
  return res.json();
}
function getCookie(name) { return document.cookie.split('; ').find(x => x.startsWith(`${name}=`))?.split('=')[1] || ''; }
function csrfToken() { return decodeURIComponent(getCookie('csrftoken')); }
function renderStep() {
  $$('.quote-panel').forEach(p => p.classList.toggle('active', Number(p.dataset.step) === step));
  $$('.quote-progress i').forEach((p,i) => p.classList.toggle('progress-active', i < step));
}
function closeModal() { modal?.classList.remove('open'); modal?.setAttribute('aria-hidden','true'); }
function openModal() { modal?.classList.add('open'); modal?.setAttribute('aria-hidden','false'); loadProducts(); }
function resetQuote() {
  step = 1; selectedProduct = null; form?.reset(); renderStep();
  if ($('#productError')) $('#productError').textContent = '';
  if ($('#submitError')) $('#submitError').textContent = '';
  $('#quoteSuccess')?.setAttribute('hidden','');
}
open?.addEventListener('click', openModal);
$$('[data-close]').forEach(x => x.addEventListener('click', closeModal));
async function loadProducts() {
  if (products.length) return;
  try { const data = await apiFetch('/api/catalog/products/'); products = data.products || []; backendAvailable = true; }
  catch { products = MOCK_PRODUCTS; backendAvailable = false; }
  const box = $('#productChoices');
  if (!box) return;
  box.innerHTML = products.map(p => `<button type="button" data-product-slug="${p.slug}">${p.name}</button>`).join('');
  box.querySelectorAll('[data-product-slug]').forEach(btn => btn.addEventListener('click', () => chooseProduct(btn.dataset.productSlug)));
  if (!backendAvailable) {
    const note = document.createElement('div'); note.className = 'quote-loading'; note.style.marginTop = '10px';
    note.textContent = 'Preview mode: connect the Django backend to save real quote requests.'; box.after(note);
  }
}
function chooseProduct(slug) {
  selectedProduct = products.find(p => String(p.slug) === String(slug));
  if (!selectedProduct) { const error = $('#productError'); if (error) error.textContent = 'Please select a valid product.'; return; }
  $$('#productChoices button').forEach(x => x.classList.toggle('selected', x.dataset.productSlug === slug));
  fillSelect('#quoteSize', selectedProduct.sizes || [], 'Select size');
  fillSelect('#quotePaper', selectedProduct.papers || [], 'Select paper / GSM');
  fillSelect('#quotePrinting', selectedProduct.printing || [], 'Select printing');
  const finishes = $('#finishingChoices');
  if (finishes) finishes.innerHTML = selectedProduct.finishing?.length ? selectedProduct.finishing.map(f => `<label><input type="checkbox" name="finishing" value="${f.id}"> ${f.name}</label>`).join('') : '<div class="quote-loading">No finishing options for this product.</div>';
  const quantity = $('#quoteQuantity'); if (quantity) quantity.value = 100;
  const error = $('#productError'); if (error) error.textContent = ''; 
}
function fillSelect(selector, options, placeholder) {
  const el = $(selector); if (!el) return;
  el.innerHTML = `<option value="">${placeholder}</option>` + options.map(o => `<option value="${o.id}">${o.name}</option>`).join('');
}
function selectedFinishing() { return $$('input[name="finishing"]:checked').map(x => x.value); }
// Robust step navigation: derive the current step from the visible panel and never call price APIs.
document.addEventListener('click', (event) => {
  const target = event.target instanceof Element ? event.target : event.target?.parentElement;
  const next = target?.closest('.next-step');
  if (!next) return;
  event.preventDefault();
  event.stopPropagation();
  const activePanel = document.querySelector('.quote-panel.active');
  const currentStep = Number(activePanel?.dataset.step || step || 1);
  step = currentStep;
  if (currentStep === 1 && !selectedProduct) {
    const error = $('#productError'); if (error) error.textContent = 'Please select a product first.';
    return;
  }
  if (currentStep === 2 && Number($('#quoteQuantity')?.value || 0) < 1) {
    const error = $('#productError'); if (error) error.textContent = 'Please enter a quantity of at least 1.';
    return;
  }
  if (currentStep < 5) { step = currentStep + 1; renderStep(); }
});
$$('.prev-step').forEach(btn => btn.addEventListener('click', () => { if (step > 1) { step--; renderStep(); } }));
$('#artworkInput')?.addEventListener('change', e => {
  const file=e.target.files?.[0]; if(!file)return;
  if(file.size>20*1024*1024){$('#uploadError').textContent='File is larger than 20 MB.';e.target.value='';return;}
  $('#uploadError').textContent=''; $('#uploadText').textContent=file.name;
});
form?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const button = $('#submitQuote'); $('#submitError').textContent = '';
  if (!selectedProduct) { $('#submitError').textContent = 'Please select a product.'; return; }
  if (Number($('#quoteQuantity').value || 0) < 1) { $('#submitError').textContent = 'Please enter a quantity of at least 1.'; return; }
  button.disabled = true; button.textContent = 'Sending…';
  try {
    if (!backendAvailable) {
      $('#quoteSuccess').hidden = false;
      $('#quoteSuccess').innerHTML = '<strong>Your request is ready.</strong><br><small>This is preview mode, so the request has not been saved. Start the Django backend to submit it to RANL PRINT.</small>';
    } else {
      const fd = new FormData(form); fd.set('product', selectedProduct.slug);
      const data = await apiFetch('/api/quotes/create/', {method:'POST', headers:{'X-CSRFToken':csrfToken()}, body:fd});
      $('#quoteSuccess').hidden = false;
      $('#quoteSuccess').innerHTML = `<strong>Quote request received!</strong><br>Reference: <b>${data.quote_number}</b><br><small>Our team will contact you with a price.</small>`;
    }
    $$('.quote-panel').forEach(p => p.classList.remove('active'));
    $('#quoteSuccess').scrollIntoView({behavior:'smooth',block:'center'});
  } catch(err) { $('#submitError').textContent = err.message || 'Could not send your request. Please try again.'; }
  finally { button.disabled = false; button.textContent = 'Send Quote Request →'; }
});
renderStep();
window.RNLQuote = { reset: resetQuote };



(() => {
  const config = window.RNL_CONFIG || {};
  const $ = (s) => document.querySelector(s);
  const setContact = (selector, value, hrefBuilder) => {
    const el = $(selector);
    if (!el) return;
    const span = el.querySelector('span');
    if (value) {
      if (span) span.textContent = value;
      if (hrefBuilder) el.href = hrefBuilder(value);
      el.hidden = false;
    } else {
      el.hidden = true;
    }
  };
  setContact('[data-contact-phone]', config.PHONE, v => `tel:${v.replace(/[^+\d]/g, '')}`);
  setContact('[data-contact-email]', config.EMAIL, v => `mailto:${v}`);
  setContact('[data-contact-location]', config.LOCATION);
  setContact('[data-contact-hours]', config.HOURS);
  setContact('[data-footer-phone]', config.PHONE, v => `tel:${v.replace(/[^+\d]/g, '')}`);
  setContact('[data-footer-email]', config.EMAIL, v => `mailto:${v}`);
  setContact('[data-footer-location]', config.LOCATION);
  setContact('[data-footer-hours]', config.HOURS);

  const form = document.getElementById('contactForm');
  const status = document.getElementById('contactStatus');
  if (!form || !status) return;

  const apiBase = String(config.API_BASE || '').replace(/\/$/, '');
  const cookie = (name) => document.cookie.split('; ').find(x => x.startsWith(`${name}=`))?.split('=')[1] || '';
  const csrf = () => decodeURIComponent(cookie('csrftoken'));
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('button[type="submit"]');
    status.textContent = '';
    status.className = 'form-status';
    button.disabled = true;
    button.textContent = 'Sending…';
    try {
      await fetch(`${apiBase}/api/csrf/`, { credentials: 'include' });
      const response = await fetch(`${apiBase}/api/contact/`, {
        method: 'POST', credentials: 'include',
        headers: {'X-CSRFToken': csrf()}, body: new FormData(form)
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.error || 'Unable to send your message.');
      status.textContent = 'Thanks — your message has been received.';
      status.classList.add('success');
      form.reset();
    } catch (error) {
      status.textContent = apiBase ? error.message : 'Connect the Django backend to send messages.';
      status.classList.add('error');
    } finally {
      button.disabled = false;
      button.textContent = 'Send Message →';
    }
  });
})();


(() => {
  const config = window.RNL_CONFIG || {};
  const form = document.getElementById('trackOrderForm');
  const status = document.getElementById('trackOrderStatus');
  const result = document.getElementById('trackOrderResult');
  if (!form || !status || !result) return;
  const apiBase = String(config.API_BASE || '').replace(/\/$/, '');
  const cookie = (name) => document.cookie.split('; ').find(x => x.startsWith(`${name}=`))?.split('=')[1] || '';
  const csrf = () => decodeURIComponent(cookie('csrftoken'));
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const money = value => `৳ ${Number(value || 0).toLocaleString('en-BD',{minimumFractionDigits:2,maximumFractionDigits:2})}`;
  fetch(`${apiBase}/api/csrf/`, {credentials:'include'}).catch(() => {});
  form.addEventListener('submit', async e => {
    e.preventDefault(); status.textContent=''; status.className='form-status'; result.hidden=true;
    const button=form.querySelector('button'); button.disabled=true; button.textContent='Checking…';
    try {
      const response=await fetch(`${apiBase}/api/orders/track/`,{method:'POST',credentials:'include',headers:{'X-CSRFToken':csrf()},body:new FormData(form)});
      const data=await response.json().catch(()=>({}));
      if(!response.ok) throw new Error(data.error || 'Unable to find this order.');
      const o=data.order;
      result.innerHTML=`<div class="track-result-head"><strong>${esc(o.order_number)}</strong><span>${esc(o.status)}</span></div><div class="track-result-grid"><div><small>Payment</small><b>${esc(o.payment_status)}</b></div><div><small>Delivery</small><b>${esc(o.delivery_status)}</b></div><div><small>Total</small><b>${money(o.total)}</b></div><div><small>Due</small><b>${money(o.due)}</b></div></div>${o.tracking_number?`<p><small>Tracking number</small><br><b>${esc(o.tracking_number)}</b></p>`:''}`;
      result.hidden=false;
    } catch(error) { status.textContent=error.message; status.classList.add('error'); }
    finally { button.disabled=false; button.textContent='Track Order →'; }
  });
})();


document.addEventListener('DOMContentLoaded', () => {
  const loader = document.getElementById('pageLoader');
  setTimeout(() => loader?.classList.add('loaded'), 650);
  document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const el = document.querySelector(a.getAttribute('href'));
    if (el) { e.preventDefault(); el.scrollIntoView({behavior:'smooth', block:'start'}); }
  }));
  document.querySelectorAll('.magnetic').forEach(btn => {
    btn.addEventListener('pointermove', e => { const r=btn.getBoundingClientRect(); btn.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.12}px, ${(e.clientY-r.top-r.height/2)*.12}px)`; });
    btn.addEventListener('pointerleave', () => btn.style.transform='');
  });
  const track=document.getElementById('testimonialTrack');
  document.querySelector('[data-test-next]')?.addEventListener('click',()=>track?.scrollBy({left:360,behavior:'smooth'}));
  document.querySelector('[data-test-prev]')?.addEventListener('click',()=>track?.scrollBy({left:-360,behavior:'smooth'}));
});
