'use strict';

/* ═══════════════════════════════════════════════════════════════
   MINADXPLORER — main.js
   All interactive behaviour in one file, organized by feature.
   ═══════════════════════════════════════════════════════════════ */


/* ── 1. PAGE FADE-IN ─────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', function () {
  document.body.classList.add('page-ready');
});


/* ── 2. HERO STAGGER ─────────────────────────────────────────── */
(function () {
  var els = document.querySelectorAll('[data-hero]');
  if (!els.length) return;
  els.forEach(function (el, i) {
    el.style.transitionDelay = (i * 90) + 'ms';
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { el.classList.add('hero-in'); });
    });
  });
})();


/* ── 3. SCROLL REVEAL WITH SIBLING STAGGER ───────────────────── */
(function () {
  if (!window.IntersectionObserver) return;
  var SELECTORS = [
    '.project-row', '.service-cell', '.cert-card', '.experience-card',
    '.research-card', '.blog-row', '.blog-card-new', '.ext-link',
    '.project-card', '.about-detail-row', '.stack-layout > div',
    '.writing-feature', '.writing-item', '.link-index-item', '.writing-side-intro',
  ].join(', ');
  var els = document.querySelectorAll(SELECTORS);
  var siblingCounters = new Map();
  els.forEach(function (el) {
    el.classList.add('reveal');
    var parent = el.parentElement;
    var idx = siblingCounters.get(parent) || 0;
    el.style.setProperty('--reveal-delay', Math.min(idx * 55, 280) + 'ms');
    siblingCounters.set(parent, idx + 1);
  });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
    });
  }, { threshold: 0.05, rootMargin: '0px 0px -24px 0px' });
  els.forEach(function (el) { io.observe(el); });
})();


/* ── 4. STAT COUNTER ─────────────────────────────────────────── */
(function () {
  var stats = document.querySelectorAll('.hero-stat-val');
  if (!stats.length || !window.IntersectionObserver) return;
  function easeOut(t) { return 1 - Math.pow(1 - t, 4); }
  function count(el, target, suffix, dur) {
    var start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = Math.round(easeOut(p) * target) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var raw    = e.target.textContent.trim();
      var suffix = raw.replace(/[0-9]/g, '');
      var num    = parseInt(raw, 10);
      if (!isNaN(num)) count(e.target, num, suffix, 900);
      io.unobserve(e.target);
    });
  }, { threshold: 0.8 });
  stats.forEach(function (el) { io.observe(el); });
})();


/* ── 5. MOBILE NAV (with overlay + outside-click close) ─────── */
(function () {
  var btn     = document.getElementById('nav-hamburger');
  var menu    = document.getElementById('mobile-nav');
  var overlay = document.getElementById('nav-overlay');
  var lastFocused = null;
  if (!btn || !menu) return;

  function getFocusableInMenu() {
    return menu.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])');
  }

  function trapTabInMenu(e) {
    if (!menu.classList.contains('open') || e.key !== 'Tab') return;
    var focusables = getFocusableInMenu();
    if (!focusables.length) return;
    var first = focusables[0];
    var last = focusables[focusables.length - 1];
    var active = document.activeElement;

    if (e.shiftKey && active === first) {
      e.preventDefault();
      last.focus();
      return;
    }
    if (!e.shiftKey && active === last) {
      e.preventDefault();
      first.focus();
    }
  }

  function open() {
    lastFocused = document.activeElement;
    menu.classList.add('open');
    overlay && overlay.classList.add('visible');
    btn.setAttribute('aria-expanded', 'true');
    menu.setAttribute('aria-hidden', 'false');
    menu.setAttribute('aria-modal', 'true');
    document.body.style.overflow = 'hidden'; // prevent scroll-through

    var focusables = getFocusableInMenu();
    if (focusables.length) focusables[0].focus();
  }
  function close() {
    menu.classList.remove('open');
    overlay && overlay.classList.remove('visible');
    btn.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-hidden', 'true');
    menu.removeAttribute('aria-modal');
    document.body.style.overflow = '';
    if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();
  }

  btn.addEventListener('click', function () {
    menu.classList.contains('open') ? close() : open();
  });

  // Close on overlay tap
  overlay && overlay.addEventListener('click', close);

  // Close when any menu link is tapped
  menu.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', close);
  });

  // Close on Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menu.classList.contains('open')) close();
    trapTabInMenu(e);
  });
})();


/* ── 6. ACTIVE NAV LINK (current page or scrolled section) ──── */
(function () {
  var nav = document.getElementById('site-nav');
  var links = document.querySelectorAll('.nav-link');
  var path  = window.location.pathname;

  if (nav) {
    var syncNavState = function () {
      nav.classList.toggle('scrolled', window.scrollY > 10);
    };
    syncNavState();
    window.addEventListener('scroll', syncNavState, { passive: true });
  }

  // Mark links for non-home pages (e.g. /blog/, /projects/)
  links.forEach(function (link) {
    var href = (link.getAttribute('href') || '').split('#')[0];
    if (href && href !== '/' && path.startsWith(href)) {
      link.classList.add('nav-link--active');
    }
  });

  // On the homepage, highlight the section in view as user scrolls
  if (path === '/') {
    links.forEach(function (l) {
      var href = l.getAttribute('href') || '';
      l.classList.toggle('nav-link--active', href === '/');
    });

    var sections = document.querySelectorAll('section[id]');
    if (!sections.length || !window.IntersectionObserver) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var id = e.target.id;
        links.forEach(function (l) {
          var href = l.getAttribute('href') || '';
          l.classList.toggle('nav-link--active', href === '/#' + id);
        });
      });
    }, { rootMargin: '-40% 0px -40% 0px' });
    sections.forEach(function (s) { io.observe(s); });
  }
})();


/* ── 7. BACK TO TOP ─────────────────────────────────────────── */
(function () {
  var btn = document.getElementById('back-to-top');
  if (!btn) return;
  window.addEventListener('scroll', function () {
    btn.classList.toggle('visible', window.scrollY > 500);
  }, { passive: true });
  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();


/* ── 8. NAV LINK UNDERLINE (CSS-only, JS marks active only) ─── */
/*  → See .nav-link::after in main.css                          */


/* ── 9. BUTTON PRESS FEEDBACK (CSS-only) ────────────────────── */
/*  → See .btn:active in main.css                               */


/* ── 10. CONTACT FORM AJAX ──────────────────────────────────── */
(function () {
  var form      = document.getElementById('contact-form');
  var feedback  = document.getElementById('form-feedback');
  var submitBtn = document.getElementById('contact-submit');
  if (!form || !feedback || !submitBtn) return;

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    var label = submitBtn.querySelector('.btn-label');
    if (label) label.textContent = 'Sending…';
    submitBtn.disabled = true;
    feedback.className = 'form-feedback';
    feedback.textContent = '';

    try {
      var res  = await fetch(form.action || '/contact/', {
        method: 'POST',
        body: new FormData(form),
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      });
      var data = await res.json();
      if (data.success) {
        feedback.className   = 'form-feedback form-feedback--ok';
        feedback.textContent = data.message || "Message sent — I'll be in touch.";
        form.reset();
      } else {
        feedback.className   = 'form-feedback form-feedback--err';
        feedback.textContent = 'Please check all fields and try again.';
      }
    } catch (_) {
      feedback.className   = 'form-feedback form-feedback--err';
      feedback.textContent = 'Something went wrong. Please email directly.';
    } finally {
      if (label) label.textContent = 'Send message';
      submitBtn.disabled = false;
    }
  });
})();


/* ── 11. LIKE BUTTON ─────────────────────────────────────────── */
(function () {
  var btn = document.getElementById('like-btn');
  if (!btn) return;

  function getCookie(name) {
    var re    = new RegExp('(^|;\\s*)' + name + '\\s*=\\s*([^;]+)');
    var match = document.cookie.match(re);
    return match ? decodeURIComponent(match[2]) : '';
  }

  btn.addEventListener('click', async function () {
    var slug      = btn.dataset.slug;
    var countEl   = document.getElementById('like-count');
    var sidebarEl = document.getElementById('sidebar-like-count');
    var icon      = btn.querySelector('.like-icon');
    btn.disabled  = true;

    try {
      var res  = await fetch('/blog/' + slug + '/like/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        },
      });
      var data = await res.json();
      btn.classList.toggle('liked', data.liked);
      btn.title = data.liked ? 'Remove like' : 'Like this post';
      if (icon) icon.setAttribute('fill', data.liked ? 'currentColor' : 'none');
      if (countEl)   countEl.textContent   = data.count;
      if (sidebarEl) sidebarEl.textContent = data.count;
      btn.classList.remove('pop');
      requestAnimationFrame(function () { btn.classList.add('pop'); });
    } catch (_) {
      // Silent — like state unchanged on network error
    } finally {
      btn.disabled = false;
    }
  });
})();


/* ── 12. VIEW-ALL TOGGLE ─────────────────────────────────────── */
(function () {
  document.querySelectorAll('[data-toggle-list]').forEach(function (list) {
    var items     = list.querySelectorAll('[data-toggle-item]');
    var showCount = parseInt(list.dataset.showCount, 10) || items.length;
    // The button lives as a sibling of the list's parent wrapper
    var btn       = list.parentElement.querySelector('[data-toggle-btn]');

    if (items.length <= showCount) {
      if (btn) btn.style.display = 'none';
      return;
    }

    items.forEach(function (item, i) {
      if (i >= showCount) item.classList.add('is-hidden');
    });

    if (!btn) return;

    var labelEl   = btn.querySelector('.view-all-label');
    var moreText  = btn.dataset.labelMore || 'View all';
    var lessText  = btn.dataset.labelLess || 'Show less';
    if (labelEl) labelEl.textContent = moreText;

    btn.addEventListener('click', function () {
      var expanded = btn.classList.toggle('is-expanded');
      items.forEach(function (item, i) {
        if (i >= showCount) item.classList.toggle('is-hidden', !expanded);
      });
      if (labelEl) labelEl.textContent = expanded ? lessText : moreText;
      if (!expanded) {
        list.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  });
})();


/* ── 13. READING PROGRESS BAR ────────────────────────────────── */
(function () {
  var fill    = document.querySelector('.reading-progress-fill');
  var article = document.querySelector('.blog-detail-body');
  if (!fill || !article) return;
  function update() {
    var top    = article.getBoundingClientRect().top + window.scrollY;
    var h      = article.offsetHeight;
    var pct    = Math.min(Math.max(((window.scrollY - top + window.innerHeight * 0.3) / h) * 100, 0), 100);
    fill.style.width = pct + '%';
  }
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
})();


/* ── 14. SHARE BUTTONS ───────────────────────────────────────── */
(function () {
  document.querySelectorAll('.share-btn[data-share]').forEach(function (btn) {
    btn.addEventListener('click', async function () {
      var type  = btn.dataset.share;
      var url   = window.location.href;
      var title = document.title;

      if (type === 'copy') {
        try {
          await navigator.clipboard.writeText(url);
          btn.classList.add('copied');
          setTimeout(function () { btn.classList.remove('copied'); }, 1800);
        } catch (_) {}
        return;
      }

      var shareUrl = type === 'twitter'
        ? 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(title) + '&url=' + encodeURIComponent(url)
        : type === 'linkedin'
        ? 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url)
        : '';

      if (shareUrl) window.open(shareUrl, '_blank', 'noopener,width=600,height=500');
    });
  });
})();
