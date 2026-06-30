'use strict';

/* ═══════════════════════════════════════════════════════════════
   MINADXPLORER — main.js
   Six animations. Each section is labelled with:
     WHERE  — which template / element it targets
     WHAT   — what it does
     HOW    — technique used
   ═══════════════════════════════════════════════════════════════ */


/* ───────────────────────────────────────────────────────────────
   ANIMATION 1 — PAGE FADE-IN
   WHERE: <body> — every page
   WHAT:  Page starts invisible (opacity:0 set in CSS).
          On DOMContentLoaded we add .page-ready → opacity:1.
          Prevents a hard paint-pop on load.
   HOW:   Single CSS transition on body triggered by class toggle.
   ─────────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', function () {
  document.body.classList.add('page-ready');
});


/* ───────────────────────────────────────────────────────────────
   ANIMATION 2 — HERO STAGGER
   WHERE: home.html → section.hero — elements with [data-hero]
          (the tag line, h1, sub paragraph, actions, stats)
   WHAT:  Each hero element fades up with a staggered delay,
          creating a cascade: tag → headline → sub → buttons → stats.
   HOW:   JS sets a transition-delay in sequence, then adds
          .hero-in to trigger the CSS transform.
   ─────────────────────────────────────────────────────────────── */
(function initHeroStagger() {
  var els = document.querySelectorAll('[data-hero]');
  if (!els.length) return;

  els.forEach(function (el, i) {
    el.style.transitionDelay = (i * 90) + 'ms';
    // Small rAF so browser has painted before we trigger
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        el.classList.add('hero-in');
      });
    });
  });
})();


/* ───────────────────────────────────────────────────────────────
   ANIMATION 3 — SCROLL REVEAL WITH STAGGER
   WHERE: Applies automatically to:
          .project-row, .service-cell, .cert-card, .timeline-item,
          .research-card, .blog-row, .ext-link, .project-card,
          .about-detail-card, .about-detail-row, .stack-layout > div
   WHAT:  Elements fade up as they enter the viewport.
          Siblings in the same parent stagger their delays so
          they cascade rather than all appearing at once.
   HOW:   IntersectionObserver + CSS --reveal-delay custom property.
   ─────────────────────────────────────────────────────────────── */
(function initScrollReveal() {
  if (!window.IntersectionObserver) return;

  var SELECTORS = [
    '.project-row',
    '.service-cell',
    '.cert-card',
    '.timeline-item',
    '.research-card',
    '.blog-row',
    '.ext-link',
    '.project-card',
    '.about-detail-row',
    '.stack-layout > div',
  ].join(', ');

  var els = document.querySelectorAll(SELECTORS);

  // Calculate stagger delay per element based on its position
  // among siblings with the same class in the same parent.
  var siblingCounters = new Map();

  els.forEach(function (el) {
    el.classList.add('reveal');

    var parent = el.parentElement;
    var key = parent;
    var idx = siblingCounters.get(key) || 0;
    // Max stagger capped at 300ms so long lists don't feel slow
    var delay = Math.min(idx * 60, 300);
    el.style.setProperty('--reveal-delay', delay + 'ms');
    siblingCounters.set(key, idx + 1);
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05, rootMargin: '0px 0px -28px 0px' });

  els.forEach(function (el) { io.observe(el); });
})();


/* ───────────────────────────────────────────────────────────────
   ANIMATION 4 — NAV LINK UNDERLINE
   WHERE: partials/nav.html → <a class="nav-link">
   WHAT:  A 1px line slides from left to right on hover.
          The CSS ::after pseudo-element handles the actual
          animation — this JS block only marks the active link.
   HOW:   Pure CSS (::after + scaleX transform). JS only adds
          .nav-link--active on the link matching the current URL.
   ─────────────────────────────────────────────────────────────── */
(function initActiveNavLink() {
  var links = document.querySelectorAll('.nav-link');
  var path  = window.location.pathname;

  links.forEach(function (link) {
    var href = link.getAttribute('href') || '';
    // Match /blog/ exactly, otherwise match hash-less pathname
    if (href === path || (href !== '/' && path.startsWith(href.split('#')[0]) && href.split('#')[0] !== '/')) {
      link.classList.add('nav-link--active');
    }
  });
})();


/* ───────────────────────────────────────────────────────────────
   ANIMATION 5 — BUTTON PRESS FEEDBACK
   WHERE: Any element with class .btn — every page
   WHAT:  On mousedown the button scales to 0.97 for 60ms.
          Gives a physical "press" feel without JS animation loops.
   HOW:   CSS handles it entirely (.btn:active in main.css).
          No JS needed — this comment is just the location note.

   → See main.css under "ANIMATION 5 — BUTTON PRESS FEEDBACK"
   ─────────────────────────────────────────────────────────────── */


/* ───────────────────────────────────────────────────────────────
   ANIMATION 6 — STAT COUNTER
   WHERE: home.html → <div class="hero-stats"> → .hero-stat-val
          The three numbers (7+, 1, 5+) count up when they
          enter the viewport.
   WHAT:  Each number ticks from 0 up to its target value
          over ~900ms using easeOutQuart easing. Suffixes
          like "+" are preserved.
   HOW:   IntersectionObserver triggers a rAF-based counter loop.
   ─────────────────────────────────────────────────────────────── */
(function initStatCounters() {
  var stats = document.querySelectorAll('.hero-stat-val');
  if (!stats.length || !window.IntersectionObserver) return;

  function easeOutQuart(t) {
    return 1 - Math.pow(1 - t, 4);
  }

  function animateCount(el, target, suffix, duration) {
    var start = null;
    el.classList.add('stat-counting');

    function step(ts) {
      if (!start) start = ts;
      var elapsed  = ts - start;
      var progress = Math.min(elapsed / duration, 1);
      var eased    = easeOutQuart(progress);
      var current  = Math.round(eased * target);
      el.textContent = current + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }

    requestAnimationFrame(step);
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el   = entry.target;
      var raw  = el.textContent.trim();         // e.g. "7+" or "5+"
      var suffix = raw.replace(/[0-9]/g, '');   // "+" or ""
      var num    = parseInt(raw, 10);            // 7, 1, 5
      if (isNaN(num)) return;
      animateCount(el, num, suffix, 900);
      io.unobserve(el);
    });
  }, { threshold: 0.8 });

  stats.forEach(function (el) { io.observe(el); });
})();


/* ── MOBILE NAV ── */
(function initMobileNav() {
  var btn  = document.getElementById('nav-hamburger');
  var menu = document.getElementById('mobile-nav');
  if (!btn || !menu) return;

  btn.addEventListener('click', function () {
    var open = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-hidden', String(!open));
  });

  menu.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () {
      menu.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
      menu.setAttribute('aria-hidden', 'true');
    });
  });
})();


/* ── CONTACT FORM AJAX ── */
(function initContactForm() {
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
        feedback.textContent = data.message || "Message sent. I'll be in touch.";
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


/* ───────────────────────────────────────────────────────────────
   ANIMATION 7 — LIKE BUTTON (blog detail page)
   WHERE: templates/blog/detail.html → #like-btn
   WHAT:  Click toggles a like via AJAX (no page reload). The
          heart icon fills/pops, and the count updates instantly
          in both the inline button and the sidebar stats card.
   HOW:   fetch() POST to /blog/<slug>/like/, CSRF token read
          from the cookie Django sets automatically.
   ─────────────────────────────────────────────────────────────── */
(function initLikeButton() {
  var btn = document.getElementById('like-btn');
  if (!btn) return;

  function getCookie(name) {
    var re = new RegExp('(^|;\\s*)' + name + '\\s*=\\s*([^;]+)');
    var match = document.cookie.match(re);
    return match ? decodeURIComponent(match[2]) : '';
  }

  btn.addEventListener('click', async function () {
    var slug       = btn.dataset.slug;
    var countEl    = document.getElementById('like-count');
    var sidebarEl  = document.getElementById('sidebar-like-count');
    var icon       = btn.querySelector('.like-icon');

    btn.disabled = true;

    try {
      var res = await fetch('/blog/' + slug + '/like/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        },
      });
      var data = await res.json();

      btn.classList.toggle('liked', data.liked);
      btn.dataset.liked = data.liked ? '1' : '0';
      btn.title = data.liked ? 'Remove like' : 'Like this post';
      if (icon) icon.setAttribute('fill', data.liked ? 'currentColor' : 'none');
      if (countEl)   countEl.textContent   = data.count;
      if (sidebarEl) sidebarEl.textContent = data.count;

      btn.classList.remove('pop');
      requestAnimationFrame(function () { btn.classList.add('pop'); });
    } catch (_) {
      // Silent fail — like state simply doesn't update
    } finally {
      btn.disabled = false;
    }
  });
})();


/* ───────────────────────────────────────────────────────────────
   VIEW-ALL TOGGLE
   WHERE: any container with [data-toggle-list] — used for the
          Experience cards and Certifications grid on the homepage.
   WHAT:  Items beyond data-show-count are hidden by default.
          A "View all (N)" button reveals the rest; clicking again
          collapses back to the initial count.
   HOW:   Pure class toggling — .is-hidden on items, .is-expanded
          on the button to flip its chevron via CSS.
   ─────────────────────────────────────────────────────────────── */
(function initViewAllToggles() {
  var containers = document.querySelectorAll('[data-toggle-list]');

  containers.forEach(function (container) {
    var items     = Array.prototype.slice.call(container.querySelectorAll('[data-toggle-item]'));
    var showCount = parseInt(container.dataset.showCount, 10) || items.length;
    var btn       = container.parentElement.querySelector('[data-toggle-btn]');

    if (items.length <= showCount) {
      if (btn) btn.style.display = 'none';
      return;
    }

    items.forEach(function (item, i) {
      if (i >= showCount) item.classList.add('is-hidden');
    });

    if (!btn) return;

    var labelEl   = btn.querySelector('.view-all-label');
    var totalText = btn.dataset.labelMore || ('View all (' + items.length + ')');
    var lessText  = btn.dataset.labelLess || 'Show less';
    if (labelEl) labelEl.textContent = totalText;

    btn.addEventListener('click', function () {
      var expanded = btn.classList.toggle('is-expanded');
      items.forEach(function (item, i) {
        if (i >= showCount) item.classList.toggle('is-hidden', !expanded);
      });
      if (labelEl) labelEl.textContent = expanded ? lessText : totalText;
      if (!expanded) {
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  });
})();


/* ───────────────────────────────────────────────────────────────
   READING PROGRESS BAR
   WHERE: templates/blog/detail.html → .reading-progress-fill
   WHAT:  A thin accent line under the nav fills left-to-right as
          the reader scrolls through the article body.
   HOW:   Scroll listener computes percentage scrolled through
          .blog-detail-body specifically (not the whole page),
          so it reaches 100% right as the article ends.
   ─────────────────────────────────────────────────────────────── */
(function initReadingProgress() {
  var fill = document.querySelector('.reading-progress-fill');
  var article = document.querySelector('.blog-detail-body');
  if (!fill || !article) return;

  function update() {
    var rect      = article.getBoundingClientRect();
    var articleTop    = rect.top + window.scrollY;
    var articleHeight = rect.height;
    var viewportH = window.innerHeight;
    var scrolled  = window.scrollY - articleTop + viewportH * 0.3;
    var total     = articleHeight;
    var pct = Math.min(Math.max((scrolled / total) * 100, 0), 100);
    fill.style.width = pct + '%';
  }

  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
})();


/* ───────────────────────────────────────────────────────────────
   SHARE BUTTONS
   WHERE: templates/blog/detail.html → .share-btn[data-share]
   WHAT:  Twitter/LinkedIn open a share-intent popup. Copy-link
          copies the current URL and flashes a "Copied" state.
   ─────────────────────────────────────────────────────────────── */
(function initShareButtons() {
  var buttons = document.querySelectorAll('.share-btn[data-share]');
  if (!buttons.length) return;

  buttons.forEach(function (btn) {
    btn.addEventListener('click', async function () {
      var type = btn.dataset.share;
      var url  = window.location.href;
      var title = document.title;

      if (type === 'copy') {
        try {
          await navigator.clipboard.writeText(url);
          btn.classList.add('copied');
          setTimeout(function () { btn.classList.remove('copied'); }, 1800);
        } catch (_) { /* clipboard unavailable — silently ignore */ }
        return;
      }

      var shareUrl = '';
      if (type === 'twitter') {
        shareUrl = 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(title) + '&url=' + encodeURIComponent(url);
      } else if (type === 'linkedin') {
        shareUrl = 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url);
      }
      if (shareUrl) window.open(shareUrl, '_blank', 'noopener,width=600,height=500');
    });
  });
})();
