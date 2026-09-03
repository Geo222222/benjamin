(() => {
  'use strict';

  const root = document.querySelector('[data-onboarding]');
  if (!root) return;

  const steps = Array.from(root.querySelectorAll('[data-ob-step]'));
  const screens = Array.from(root.querySelectorAll('[data-ob-screen]'));
  const progress = root.querySelector('[data-ob-progress]');
  const currentLabel = root.querySelector('[data-ob-current]');
  const prev = root.querySelector('[data-ob-prev]');
  const next = root.querySelector('[data-ob-next]');
  const total = screens.length;

  const names = ['Identity', 'Financial profile', 'Mandate', 'Agreements', 'Custody', 'Activation'];

  function clamp(value) {
    return Math.max(0, Math.min(total - 1, value));
  }

  function requestedIndex() {
    const query = new URLSearchParams(window.location.search).get('step');
    const named = names.findIndex((name) => name.toLowerCase().replace(/\s+/g, '-') === String(query || '').toLowerCase());
    if (named >= 0) return named;
    const numeric = Number(query);
    return Number.isInteger(numeric) && numeric >= 1 && numeric <= total ? numeric - 1 : 0;
  }

  let active = clamp(requestedIndex());

  function render(index, updateUrl = true) {
    active = clamp(index);
    steps.forEach((step, stepIndex) => {
      step.classList.toggle('is-active', stepIndex === active);
      step.classList.toggle('is-complete', stepIndex < active);
      step.setAttribute('aria-current', stepIndex === active ? 'step' : 'false');
    });
    screens.forEach((screen, screenIndex) => screen.classList.toggle('is-active', screenIndex === active));
    if (progress) progress.style.setProperty('--progress', `${((active + 1) / total) * 100}%`);
    if (currentLabel) currentLabel.textContent = `STEP ${String(active + 1).padStart(2, '0')} OF ${String(total).padStart(2, '0')} · ${names[active].toUpperCase()}`;
    if (prev) prev.disabled = active === 0;
    if (next) {
      next.textContent = active === total - 1 ? 'Finish preview' : `Continue to ${names[active + 1]}`;
      next.dataset.finish = String(active === total - 1);
    }
    if (updateUrl) {
      const url = new URL(window.location.href);
      url.searchParams.set('step', names[active].toLowerCase().replace(/\s+/g, '-'));
      history.replaceState({}, '', url);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  steps.forEach((step, index) => step.addEventListener('click', () => render(index)));
  prev?.addEventListener('click', () => render(active - 1));
  next?.addEventListener('click', () => {
    if (active === total - 1) {
      window.location.href = '../sign-in/';
      return;
    }
    render(active + 1);
  });

  root.querySelectorAll('[data-preview-choice]').forEach((choice) => {
    choice.addEventListener('click', () => {
      const group = choice.closest('[data-preview-choice-group]');
      group?.querySelectorAll('[data-preview-choice]').forEach((node) => node.classList.remove('is-selected'));
      choice.classList.add('is-selected');
    });
  });

  render(active, false);
})();
