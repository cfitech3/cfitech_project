/**
 * CFI-TECH — JavaScript Principal
 * Interactions, animations, utilitaires
 */

'use strict';

/* ─── NAVBAR SCROLL ────────────────────────────────────────── */
(function initNavbar() {
  const nav = document.getElementById('mainNav');
  if (!nav) return;

  function onScroll() {
    if (window.scrollY > 50) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();


/* ─── BACK TO TOP ──────────────────────────────────────────── */
(function initBackToTop() {
  const btn = document.getElementById('backToTop');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();


/* ─── COMPTEUR ANIMÉ ───────────────────────────────────────── */
(function initCounters() {
  const counters = document.querySelectorAll('.counter');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseInt(el.dataset.target || el.textContent, 10);
      const duration = 1800;
      const step = target / (duration / 16);
      let current = 0;

      const update = () => {
        current = Math.min(current + step, target);
        el.textContent = Math.floor(current).toLocaleString('fr-FR');
        if (current < target) requestAnimationFrame(update);
      };
      requestAnimationFrame(update);
      observer.unobserve(el);
    });
  }, { threshold: 0.4 });

  counters.forEach(c => observer.observe(c));
})();


/* ─── COMPTE À REBOURS ─────────────────────────────────────── */
(function initCountdowns() {
  document.querySelectorAll('.countdown').forEach(el => {
    const deadlineStr = el.dataset.deadline;
    if (!deadlineStr) return;
    const deadline = new Date(deadlineStr + 'T23:59:59');

    function update() {
      const now = new Date();
      const diff = deadline - now;
      if (diff <= 0) {
        el.innerHTML = '<span style="color:var(--danger)">Clôturé</span>';
        return;
      }
      const days  = Math.floor(diff / 86400000);
      const hours = Math.floor((diff % 86400000) / 3600000);
      const mins  = Math.floor((diff % 3600000) / 60000);

      const dEl = el.querySelector('.cd-days');
      const hEl = el.querySelector('.cd-hours');
      const mEl = el.querySelector('.cd-mins');
      if (dEl) dEl.textContent = String(days).padStart(2, '0');
      if (hEl) hEl.textContent = String(hours).padStart(2, '0');
      if (mEl) mEl.textContent = String(mins).padStart(2, '0');
    }
    update();
    setInterval(update, 60000);
  });
})();


/* ─── NEWSLETTER AJAX ──────────────────────────────────────── */
(function initNewsletter() {
  const form = document.getElementById('newsletterForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msgEl = document.getElementById('newsletterMsg');
    const btn   = form.querySelector('button[type="submit"]');
    const email = form.querySelector('[name="email"]').value.trim();

    if (!email) return;
    btn.disabled = true;
    btn.textContent = '...';

    try {
      const fd = new FormData(form);
      const resp = await fetch('/newsletter/inscription/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: fd,
      });
      const data = await resp.json();
      if (msgEl) {
        msgEl.textContent = data.message;
        msgEl.style.color = data.status === 'success' ? '#90EE90' : 'rgba(255,255,255,.8)';
      }
      if (data.status === 'success') form.reset();
    } catch {
      if (msgEl) msgEl.textContent = 'Une erreur est survenue. Réessayez.';
    } finally {
      btn.disabled = false;
      btn.textContent = "S'abonner";
    }
  });
})();


/* ─── AUTO-DISMISS MESSAGES ────────────────────────────────── */
(function initMessages() {
  document.querySelectorAll('.custom-alert').forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 6000);
  });
})();


/* ─── FILTRES FORMATIONS (URL params) ──────────────────────── */
(function initFormationFilters() {
  const filterForm = document.getElementById('formationFilterForm');
  if (!filterForm) return;

  filterForm.querySelectorAll('select, input').forEach(input => {
    input.addEventListener('change', () => filterForm.submit());
  });
})();


/* ─── PARTAGE RÉSEAUX SOCIAUX ──────────────────────────────── */
window.shareFormation = function(platform, url, title) {
  const encodedUrl   = encodeURIComponent(url);
  const encodedTitle = encodeURIComponent(title);
  const links = {
    facebook:  `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`,
    twitter:   `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedTitle}`,
    linkedin:  `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`,
    whatsapp:  `https://wa.me/?text=${encodedTitle}%20${encodedUrl}`,
  };
  if (links[platform]) {
    window.open(links[platform], '_blank', 'width=600,height=400');
  }
};


/* ─── COPIER LIEN ───────────────────────────────────────────── */
window.copyLink = function(url) {
  navigator.clipboard.writeText(url).then(() => {
    showToast('Lien copié !', 'success');
  }).catch(() => {
    const input = document.createElement('input');
    input.value = url;
    document.body.appendChild(input);
    input.select();
    document.execCommand('copy');
    document.body.removeChild(input);
    showToast('Lien copié !', 'success');
  });
};


/* ─── TOAST NOTIFICATION ────────────────────────────────────── */
window.showToast = function(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `custom-toast toast-${type}`;
  toast.textContent = message;
  toast.style.cssText = `
    position:fixed; bottom:80px; right:24px; z-index:9999;
    background:${type === 'success' ? 'var(--success)' : 'var(--blue-mid)'};
    color:#fff; padding:12px 20px; border-radius:12px;
    font-family:var(--font-display); font-weight:600; font-size:.9rem;
    box-shadow:0 8px 24px rgba(0,0,0,.2);
    animation: slideInToast .3s ease;
  `;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity .4s';
    setTimeout(() => toast.remove(), 400);
  }, 2500);
};


/* ─── LAZY LOAD IMAGES ──────────────────────────────────────── */
(function initLazyLoad() {
  if ('loading' in HTMLImageElement.prototype) return;
  document.querySelectorAll('img[loading="lazy"]').forEach(img => {
    img.src = img.dataset.src || img.src;
  });
})();


/* ─── CSRF TOKEN HELPER ─────────────────────────────────────── */
function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (const c of cookies) {
    const [k, v] = c.trim().split('=');
    if (k === name) return decodeURIComponent(v);
  }
  return null;
}


/* ─── PROGRESS BAR PAGE ─────────────────────────────────────── */
(function initProgressBar() {
  const bar = document.createElement('div');
  bar.style.cssText = `
    position:fixed;top:0;left:0;z-index:9999;height:3px;width:0%;
    background:linear-gradient(90deg,var(--blue-mid),var(--accent));
    transition:width .2s ease;pointer-events:none;
  `;
  document.body.prepend(bar);

  window.addEventListener('scroll', () => {
    const scrollTop = document.documentElement.scrollTop;
    const scrollMax = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = scrollMax > 0 ? `${(scrollTop / scrollMax) * 100}%` : '0%';
  }, { passive: true });
})();


/* ─── GALERIE LIGHTBOX SIMPLE ───────────────────────────────── */
(function initGallery() {
  const items = document.querySelectorAll('.gallery-item img');
  if (!items.length) return;

  const overlay = document.createElement('div');
  overlay.className = 'gallery-overlay';
  overlay.innerHTML = `
    <div class="gallery-overlay-inner">
      <img src="" alt="" class="gallery-big-img" />
      <button class="gallery-close" aria-label="Fermer">&times;</button>
    </div>
  `;
  overlay.style.cssText = `
    display:none;position:fixed;inset:0;z-index:99999;
    background:rgba(0,0,0,.92);align-items:center;justify-content:center;
  `;
  document.body.appendChild(overlay);

  items.forEach(img => {
    img.style.cursor = 'zoom-in';
    img.addEventListener('click', () => {
      overlay.querySelector('.gallery-big-img').src = img.src;
      overlay.style.display = 'flex';
      document.body.style.overflow = 'hidden';
    });
  });

  function closeOverlay() {
    overlay.style.display = 'none';
    document.body.style.overflow = '';
  }
  overlay.querySelector('.gallery-close').addEventListener('click', closeOverlay);
  overlay.addEventListener('click', e => { if (e.target === overlay) closeOverlay(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeOverlay(); });
})();


/* ─── PHONE FORMAT MALI ─────────────────────────────────────── */
(function initPhoneFormat() {
  const phoneInputs = document.querySelectorAll('input[name="phone"]');
  phoneInputs.forEach(input => {
    input.addEventListener('input', () => {
      let val = input.value.replace(/\D/g, '');
      if (val.startsWith('223')) val = val.slice(3);
      if (val.length > 8) val = val.slice(0, 8);
      input.value = val;
    });
  });
})();


/* ─── Domaines : 4 visible par défaut, toggle pour voir tous ── */
(function initDomains() {
  const MAX_VISIBLE = 4;
  const items = document.querySelectorAll('.domain-item');
  const btn   = document.getElementById('domainsToggleBtn');
  const wrap  = document.getElementById('domainsToggleWrap');

  if (!items.length) return;

  // Cacher les éléments au-delà de MAX_VISIBLE
  function applyVisibility(showAll) {
    items.forEach((el, i) => {
      if (i < MAX_VISIBLE) {
        el.style.display = '';
      } else {
        el.style.display = showAll ? '' : 'none';
      }
    });

    const hiddenCount = items.length - MAX_VISIBLE;
    const textEl = document.getElementById('domainsToggleText');
    if (textEl) {
      textEl.textContent = showAll
        ? 'Réduire'
        : `Voir tous les ${items.length} domaines`;
    }
    // Cacher le bouton si pas assez d'éléments
    if (wrap) {
      wrap.style.display = items.length > MAX_VISIBLE ? '' : 'none';
    }
  }

  let expanded = false;
  applyVisibility(false); // Masquer dès le chargement

  window.toggleDomains = function () {
    expanded = !expanded;
    applyVisibility(expanded);
    lucide.createIcons();
  };
})();