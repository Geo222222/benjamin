(() => {
  'use strict';
  const scriptUrl = document.currentScript?.src || new URL('./assets/app.js', window.location.href).href;
  const asset = (name) => new URL(name, scriptUrl).href;
  const demoHref = new URL('../demo/', scriptUrl).href;

  document.querySelectorAll('[data-year]').forEach((node) => { node.textContent = String(new Date().getFullYear()); });

  const menuToggle = document.querySelector('[data-menu-toggle]');
  const mobileNav = document.querySelector('[data-mobile-nav]');
  const headerActions = document.querySelector('.site-header .header-actions');

  if (headerActions && !headerActions.querySelector('[data-demo-link]')) {
    const demoLink = document.createElement('a');
    demoLink.className = 'text-link';
    demoLink.href = demoHref;
    demoLink.textContent = 'Demo consoles';
    demoLink.dataset.demoLink = 'true';
    headerActions.prepend(demoLink);
  }

  if (mobileNav && !mobileNav.querySelector('[data-demo-link]')) {
    const demoLink = document.createElement('a');
    demoLink.href = demoHref;
    demoLink.textContent = 'Demo consoles';
    demoLink.dataset.demoLink = 'true';
    mobileNav.appendChild(demoLink);
  }

  if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', () => {
      const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', String(!expanded));
      mobileNav.hidden = expanded;
    });
    mobileNav.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
      menuToggle.setAttribute('aria-expanded', 'false');
      mobileNav.hidden = true;
    }));
  }

  const header = document.querySelector('[data-header]');
  if (header && 'IntersectionObserver' in window) {
    const sentinel = document.createElement('div');
    sentinel.className = 'header-sentinel';
    header.before(sentinel);
    new IntersectionObserver(([entry]) => header.classList.toggle('scrolled', !entry.isIntersecting), { threshold: 1 }).observe(sentinel);
  }

  const glyphs = '010101011001001101011001';
  document.querySelectorAll('[data-matrix], .closing-matrix').forEach((field, fieldIndex) => {
    if (field.dataset.generated === 'true') return;
    field.dataset.generated = 'true';
    for (let index = 0; index < 28; index += 1) {
      const column = document.createElement('span');
      column.className = 'matrix-column';
      const length = 12 + ((index * 7 + fieldIndex * 5) % 18);
      column.textContent = Array.from({ length }, (_, charIndex) => glyphs[(index * 3 + charIndex * 5) % glyphs.length]).join('\n');
      column.style.setProperty('--column', String(index));
      field.appendChild(column);
    }
  });

  const invitationIdNode = document.querySelector('[data-invite-id]');
  if (invitationIdNode) {
    const previewId = new URLSearchParams(window.location.search).get('preview');
    if (previewId && /^[A-Za-z0-9_-]{4,48}$/.test(previewId)) invitationIdNode.textContent = `BEN-I-${previewId.toUpperCase()}`;
  }

  if (!document.querySelector('link[data-benjamin-brand]')) {
    const brandCss = document.createElement('link');
    brandCss.rel = 'stylesheet';
    brandCss.href = asset('brand.css');
    brandCss.dataset.benjaminBrand = 'true';
    document.head.appendChild(brandCss);
  }
  if (!document.querySelector('link[rel="icon"][data-benjamin-icon]')) {
    const icon = document.createElement('link');
    icon.rel = 'icon'; icon.type = 'image/webp'; icon.href = asset('benjamin-favicon.webp'); icon.dataset.benjaminIcon = 'true';
    document.head.appendChild(icon);
  }
  document.querySelectorAll('.brand-copy small').forEach((node) => { node.textContent = 'A CODEREIGN COMPANY'; });

  const addStory = (anchor, className, imageName, alt, caption) => {
    const target = document.querySelector(anchor);
    if (!target || document.querySelector(`.${className}`)) return;
    const figure = document.createElement('figure');
    figure.className = `brand-story ${className}`;
    const image = document.createElement('img');
    image.src = asset(imageName); image.alt = alt; image.loading = 'lazy'; image.decoding = 'async'; image.width = 640; image.height = 360;
    const figcaption = document.createElement('figcaption');
    figcaption.textContent = caption;
    figure.append(image, figcaption);
    target.after(figure);
  };

  addStory('#philosophy .account-model', 'brand-story-account', 'benjamin-account.webp', 'Benjamin wolf guardian behind separate client account vaults, illustrating individually owned and privately stewarded capital.', 'Your capital stays yours · individually managed · privately stewarded');
  addStory('#governance .mandate-layout', 'brand-story-growth', 'benjamin-growth.webp', 'Benjamin robotic wolf beside an ascending market chart and protection shields, illustrating automated intelligence under disciplined risk controls.', 'Automated · intelligent · disciplined');
})();
