// This script is scoped to the student essay page only.
(() => {
  const buttons = [...document.querySelectorAll('[data-timeline-filter]')];
  for (const button of buttons) button.addEventListener('click', () => {
    const selected = button.dataset.timelineFilter;
    for (const item of buttons) item.setAttribute('aria-pressed', String(item === button));
    for (const entry of document.querySelectorAll('.ps-students .timeline-item'))
      entry.hidden = selected !== 'all' && entry.dataset.track !== selected;
  });
  const sections = [...document.querySelectorAll('.ps-students .story-section')];
  const links = [...document.querySelectorAll('.ps-students [data-sectionlink]')];
  if ('IntersectionObserver' in window && sections.length && links.length) {
    const io = new IntersectionObserver(entries => {
      for (const entry of entries) if (entry.isIntersecting)
        for (const link of links) link.classList.toggle('current', link.dataset.sectionlink === entry.target.id);
    }, { rootMargin: '-15% 0px -72% 0px' });
    for (const el of sections) io.observe(el);
  }
})();
