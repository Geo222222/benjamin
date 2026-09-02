(() => {
  'use strict';

  const yearNodes = document.querySelectorAll('[data-year]');
  const year = new Date().getFullYear();
  yearNodes.forEach((node) => { node.textContent = String(year); });

  const menuToggle = document.querySelector('[data-menu-toggle]');
  const mobileNav = document.querySelector('[data-mobile-nav]');
  if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', () => {
      const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', String(!expanded));
      mobileNav.hidden = expanded;
    });
    mobileNav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        menuToggle.setAttribute('aria-expanded', 'false');
        mobileNav.hidden = true;
      });
    });
  }

  const header = document.querySelector('[data-header]');
  if (header && 'IntersectionObserver' in window) {
    const sentinel = document.createElement('div');
    sentinel.className = 'header-sentinel';
    header.before(sentinel);
    const observer = new IntersectionObserver(([entry]) => {
      header.classList.toggle('scrolled', !entry.isIntersecting);
    }, { threshold: 1 });
    observer.observe(sentinel);
  }

  const matrixFields = document.querySelectorAll('[data-matrix], .closing-matrix');
  const glyphs = '010101011001001101011001';
  matrixFields.forEach((field, fieldIndex) => {
    if (field.dataset.generated === 'true') return;
    field.dataset.generated = 'true';
    const columns = 28;
    for (let index = 0; index < columns; index += 1) {
      const column = document.createElement('span');
      column.className = 'matrix-column';
      const length = 12 + ((index * 7 + fieldIndex * 5) % 18);
      let text = '';
      for (let charIndex = 0; charIndex < length; charIndex += 1) {
        text += glyphs[(index * 3 + charIndex * 5) % glyphs.length] + '\n';
      }
      column.textContent = text;
      column.style.setProperty('--column', String(index));
      field.appendChild(column);
    }
  });

  const invitationIdNode = document.querySelector('[data-invite-id]');
  if (invitationIdNode) {
    const params = new URLSearchParams(window.location.search);
    const previewId = params.get('preview');
    if (previewId && /^[A-Za-z0-9_-]{4,48}$/.test(previewId)) {
      invitationIdNode.textContent = `BEN-I-${previewId.toUpperCase()}`;
    }
  }
})();
