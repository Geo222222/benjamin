const THEME_KEY = 'benjamin-demo-theme';
type ThemeName = 'matrix' | 'light';

const iconPaths: Record<string, string> = {
  home: 'M3 11.5 12 4l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1Z',
  users: 'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75',
  wallet: 'M20 7V5a2 2 0 0 0-2-2H5a3 3 0 0 0 0 6h15v12H5a3 3 0 0 1-3-3V6M16 13h4',
  coins: 'M8 6c0 1.66-2.24 3-5 3S-2 7.66-2 6s2.24-3 5-3 5 1.34 5 3Zm0 0v4c0 1.66-2.24 3-5 3s-5-1.34-5-3V6m10 4v4c0 1.66-2.24 3-5 3s-5-1.34-5-3v-4M22 10c0 1.66-2.24 3-5 3s-5-1.34-5-3 2.24-3 5-3 5 1.34 5 3Zm0 0v4c0 1.66-2.24 3-5 3a7 7 0 0 1-2-.28M22 14v4c0 1.66-2.24 3-5 3a7 7 0 0 1-2-.28',
  chart: 'M3 3v18h18M7 16l4-5 4 3 5-7',
  briefcase: 'M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M4 7h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2Zm-2 5h20M10 12v2h4v-2',
  brain: 'M9.5 4A3.5 3.5 0 0 0 6 7.5v.3A3.5 3.5 0 0 0 4.5 14H5a4 4 0 0 0 4 4h1V4Zm5 0A3.5 3.5 0 0 1 18 7.5v.3a3.5 3.5 0 0 1 1.5 6.2H19a4 4 0 0 1-4 4h-1V4ZM10 8H8m6 0h2m-6 4H7m7 0h3m-7 4H9m5 0h1',
  send: 'm22 2-7 20-4-9-9-4Zm-11 11 11-11',
  shield: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Zm-3-10 2 2 4-4',
  layers: 'm12 2 9 5-9 5-9-5 9-5Zm-9 10 9 5 9-5M3 17l9 5 9-5',
  activity: 'M3 12h4l2-6 4 12 2-6h6',
  book: 'M4 4h6a4 4 0 0 1 4 4v12a4 4 0 0 0-4-4H4V4Zm16 0h-6a4 4 0 0 0-4 4v12a4 4 0 0 1 4-4h6V4Z',
  badge: 'm12 2 2.2 2.1 3-.2.8 2.9 2.5 1.7-.7 2.9.7 2.5-1.7.8-2.9 3 .2L12 22l-2.2-2.1-3 .2-.8-2.9-2.5-1.7.7-2.9-.7-2.5L6 6.4l.8-2.9 3 .2L12 2Zm-3 10 2 2 4-4',
  wrench: 'M14.7 6.3a4 4 0 0 0-5-5L12 3.6 9.6 6 7.3 3.7a4 4 0 0 0 5 5L5 16l3 3 7.3-7.3a4 4 0 0 0 5-5L18 9l-2.4-2.4 2.3-2.3a4 4 0 0 0-3.2 2Z',
  server: 'M4 4h16v6H4V4Zm0 10h16v6H4v-6Zm3-7h.01M7 17h.01',
  crown: 'm3 7 4 4 5-7 5 7 4-4-2 12H5L3 7Zm3 12h12',
  report: 'M4 2h11l5 5v15H4V2Zm11 0v6h5M8 17v-4m4 4V9m4 8v-6',
  history: 'M3 12a9 9 0 1 0 3-6.7L3 8m0-5v5h5M12 7v5l3 2',
  settings: 'M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Zm0-13 1 2.1 2.3.5 1.7-1.5 2.2 2.2-1.5 1.7.5 2.3L21.5 12l-2.1 1-.5 2.3 1.5 1.7-2.2 2.2-1.7-1.5-2.3.5-1 2.1h-3l-1-2.1-2.3-.5-1.7 1.5L3 17l1.5-1.7-.5-2.3-2.1-1 2.1-1 .5-2.3L3 7l2.2-2.2 1.7 1.5 2.3-.5 1-2.1h1.8Z',
  clock: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20Zm0-14v5l3 2',
  scroll: 'M6 3h12v14a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4h12M6 3a4 4 0 0 0-4 4v10',
  message: 'M21 15a4 4 0 0 1-4 4H8l-5 3v-7a4 4 0 0 1-1-2.7V7a4 4 0 0 1 4-4h11a4 4 0 0 1 4 4v8Z',
  help: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20Zm-3-12a3 3 0 1 1 5 2.2c-1.2.9-2 1.4-2 2.8M12 18h.01',
  receipt: 'M5 2 7 4l2-2 2 2 2-2 2 2 2-2 2 2v18l-2-2-2 2-2-2-2 2-2-2-2 2-2-2V2Zm3 7h8M8 13h6',
  bell: 'M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9Zm-8 12h4',
  userPlus: 'M15 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M8 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm11-4v6m-3-3h6'
};

function svg(path: string, size = 18) {
  return `<svg class="ben-icon" viewBox="0 0 24 24" width="${size}" height="${size}" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="${path}"/></svg>`;
}

function iconKey(label: string) {
  const value = label.toLowerCase();
  if (value.includes('client')) return 'users';
  if (value.includes('account')) return 'wallet';
  if (value.includes('capital') || value === 'money') return 'coins';
  if (value.includes('market') || value.includes('performance')) return 'chart';
  if (value.includes('investment case')) return 'briefcase';
  if (value.includes('decision') || value === 'benjamin') return 'brain';
  if (value.includes('execution') || value.includes('hand')) return 'send';
  if (value.includes('risk') || value.includes('watchman')) return 'shield';
  if (value.includes('strateg')) return 'layers';
  if (value.includes('intelligence') || value === 'activity') return 'activity';
  if (value.includes('book') || value.includes('evidence')) return 'book';
  if (value.includes('compliance')) return 'badge';
  if (value.includes('operations')) return 'wrench';
  if (value === 'system') return 'server';
  if (value.includes('owner command')) return 'crown';
  if (value.includes('report')) return 'report';
  if (value.includes('audit')) return 'history';
  if (value.includes('governance') || value.includes('settings')) return 'settings';
  if (value.includes('mandate')) return 'scroll';
  if (value.includes('document')) return 'report';
  if (value.includes('message')) return 'message';
  if (value.includes('support')) return 'help';
  if (value.includes('tax')) return 'receipt';
  if (value.includes('notification')) return 'bell';
  if (value.includes('join') || value.includes('onboarding')) return 'userPlus';
  if (value === 'home' || value === 'command') return 'home';
  return 'activity';
}

function currentTheme(): ThemeName {
  return document.documentElement.dataset.theme === 'light' ? 'light' : 'matrix';
}

function paintTheme(theme: ThemeName) {
  document.documentElement.dataset.theme = theme;
  localStorage.setItem(THEME_KEY, theme);
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'light' ? '#eef3fa' : '#020806');
  document.querySelectorAll<HTMLElement>('[data-theme-choice]').forEach((button) => {
    button.classList.toggle('active', button.dataset.themeChoice === theme);
    button.setAttribute('aria-pressed', String(button.dataset.themeChoice === theme));
  });
}

function mountAppearanceControl() {
  if (document.querySelector('.appearance-control')) return;
  const topbar = document.querySelector<HTMLElement>('.topbar, .client-topbar');
  if (!topbar) return;

  const wrap = document.createElement('div');
  wrap.className = 'appearance-control';
  wrap.innerHTML = `
    <button class="appearance-trigger" type="button" aria-haspopup="menu" aria-expanded="false" title="Appearance">
      ${svg('M12 3a9 9 0 1 0 9 9c0-1.1-.9-2-2-2h-1.2a2 2 0 0 1-1.8-2.9l.6-1.1A2 2 0 0 0 14.8 3H12ZM7.5 10.5h.01M10 6.5h.01M15 6.5h.01M17 11h.01M9 16h.01', 17)}
      <span>Appearance</span>
    </button>
    <div class="appearance-popover" role="menu" hidden>
      <div class="appearance-heading"><strong>Appearance</strong><small>Shared across Benjamin demos</small></div>
      <button type="button" data-theme-choice="matrix" role="menuitemradio"><i class="theme-swatch matrix"></i><span><b>Matrix</b><small>Primary command theme</small></span></button>
      <button type="button" data-theme-choice="light" role="menuitemradio"><i class="theme-swatch light"></i><span><b>Blue / White</b><small>Secondary institutional theme</small></span></button>
    </div>`;

  const anchor = topbar.querySelector('.owner-chip, .client-user');
  if (anchor) topbar.insertBefore(wrap, anchor);
  else topbar.appendChild(wrap);

  const trigger = wrap.querySelector<HTMLButtonElement>('.appearance-trigger')!;
  const popover = wrap.querySelector<HTMLElement>('.appearance-popover')!;
  trigger.addEventListener('click', () => {
    const open = !popover.hidden;
    popover.hidden = open;
    trigger.setAttribute('aria-expanded', String(!open));
  });
  wrap.addEventListener('click', (event) => {
    const target = (event.target as HTMLElement).closest<HTMLElement>('[data-theme-choice]');
    if (!target) return;
    paintTheme(target.dataset.themeChoice === 'light' ? 'light' : 'matrix');
    popover.hidden = true;
    trigger.setAttribute('aria-expanded', 'false');
  });
  document.addEventListener('click', (event) => {
    if (!wrap.contains(event.target as Node)) {
      popover.hidden = true;
      trigger.setAttribute('aria-expanded', 'false');
    }
  });
  paintTheme(currentTheme());
}

function upgradeNavigation() {
  document.querySelectorAll<HTMLElement>('.nav-item').forEach((button) => {
    if (button.dataset.iconReady) return;
    const label = button.textContent?.trim() || '';
    const glyph = button.querySelector<HTMLElement>('.nav-glyph');
    if (glyph) glyph.innerHTML = svg(iconPaths[iconKey(label)]);
    button.dataset.iconReady = 'true';
    button.setAttribute('title', label);
  });

  document.querySelectorAll<HTMLButtonElement>('.client-sidebar nav button').forEach((button) => {
    if (button.dataset.iconReady) return;
    const label = button.querySelector('b')?.textContent?.trim() || button.textContent?.trim() || '';
    const glyph = button.querySelector<HTMLElement>('span');
    if (glyph) glyph.innerHTML = svg(iconPaths[iconKey(label)]);
    button.dataset.iconReady = 'true';
    button.setAttribute('title', label);
  });
}

function addChartTracer(polyline: SVGPolylineElement) {
  if (polyline.dataset.motionReady) return;
  polyline.dataset.motionReady = 'true';
  try {
    const length = polyline.getTotalLength();
    polyline.style.strokeDasharray = `${length}`;
    polyline.style.strokeDashoffset = `${length}`;
    polyline.animate([{ strokeDashoffset: length }, { strokeDashoffset: 0 }], { duration: 1000, easing: 'cubic-bezier(.2,.75,.2,1)', fill: 'forwards' });
  } catch { /* SVG implementation may not expose geometry in tests. */ }

  const points = polyline.getAttribute('points')?.trim();
  const owner = polyline.ownerSVGElement;
  if (!points || !owner || owner.querySelector('[data-chart-tracer]')) return;
  const path = 'M ' + points.split(/\s+/).map((point) => point.replace(',', ' ')).join(' L ');
  const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  circle.setAttribute('r', '3.25');
  circle.setAttribute('class', 'chart-tracer');
  circle.setAttribute('data-chart-tracer', 'true');
  const motion = document.createElementNS('http://www.w3.org/2000/svg', 'animateMotion');
  motion.setAttribute('dur', '7s');
  motion.setAttribute('repeatCount', 'indefinite');
  motion.setAttribute('path', path);
  circle.appendChild(motion);
  owner.appendChild(circle);
}

function animateNumber(element: HTMLElement) {
  if (element.dataset.countReady) return;
  const raw = element.textContent?.trim() || '';
  const match = raw.match(/-?\d[\d,]*(?:\.\d+)?/);
  if (!match) return;
  const value = Number(match[0].replace(/,/g, ''));
  if (!Number.isFinite(value) || Math.abs(value) > 1_000_000_000) return;
  const decimals = match[0].includes('.') ? match[0].split('.')[1].length : 0;
  const prefix = raw.slice(0, match.index);
  const suffix = raw.slice((match.index || 0) + match[0].length);
  element.dataset.countReady = 'true';
  const start = performance.now();
  const duration = 700;
  const frame = (time: number) => {
    const progress = Math.min(1, (time - start) / duration);
    const eased = 1 - Math.pow(1 - progress, 3);
    const next = value * eased;
    const formatted = next.toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
    element.textContent = `${prefix}${formatted}${suffix}`;
    if (progress < 1) requestAnimationFrame(frame);
    else element.textContent = raw;
  };
  requestAnimationFrame(frame);
}

function animateVisuals() {
  document.querySelectorAll<SVGPolylineElement>('.line-chart polyline, .sparkline polyline, .equity-chart polyline').forEach(addChartTracer);
  document.querySelectorAll<HTMLElement>('.strategy-bars em, .horizontal-bars em, .risk-bars em, .month-bars i').forEach((bar, index) => {
    if (bar.dataset.motionReady) return;
    bar.dataset.motionReady = 'true';
    bar.style.animationDelay = `${Math.min(index * 55, 550)}ms`;
    bar.classList.add('motion-bar');
  });
  document.querySelectorAll<HTMLElement>('.donut, .strategy-donut, .allocation-donut, .risk-ring, .risk-circle').forEach((ring, index) => {
    if (ring.dataset.motionReady) return;
    ring.dataset.motionReady = 'true';
    ring.style.animationDelay = `${index * 80}ms`;
    ring.classList.add('motion-ring');
  });
  document.querySelectorAll<HTMLElement>('.metric strong, .client-metric strong, .big-number, .value-card > strong, .today-card > strong').forEach(animateNumber);
}

let queued = false;
function enhance() {
  if (queued) return;
  queued = true;
  requestAnimationFrame(() => {
    queued = false;
    mountAppearanceControl();
    upgradeNavigation();
    animateVisuals();
  });
}

export function installProductPolish() {
  const saved = localStorage.getItem(THEME_KEY);
  paintTheme(saved === 'light' ? 'light' : 'matrix');
  enhance();
  const observer = new MutationObserver(enhance);
  observer.observe(document.documentElement, { childList: true, subtree: true });
  window.addEventListener('pageshow', enhance);
}
