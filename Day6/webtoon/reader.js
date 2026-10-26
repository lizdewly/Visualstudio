const host = document.getElementById('episodes');
const menu = document.getElementById('chapter-select');
const links = document.getElementById('chapter-links');
// 생성 삽화의 실제 가로 경계에 맞춰 각 컷을 표시한다.
const rowEdges = [
  [0, 512 / 1536, 1001 / 1536, 1],
  [0, 1 / 3, 2 / 3, 1],
  [0, 512 / 1536, 1005 / 1536, 1],
  [0, 510 / 1536, 1015 / 1536, 1],
  [0, 505 / 1536, 993 / 1536, 1],
  [0, 477 / 1536, 959 / 1536, 1],
  [0, 490 / 1536, 978 / 1536, 1],
];

function element(tag, className, text) {
  const item = document.createElement(tag);
  if (className) item.className = className;
  if (text !== undefined) item.textContent = text;
  return item;
}

episodes.forEach((episode, index) => {
  const number = index + 1;
  const id = `ep${number}`;
  const option = element('option', '', `${number}화 · ${episode.short}`);
  option.value = id;
  menu.append(option);
  const link = element('a', 'chapter-link');
  link.href = `#${id}`;
  link.append(element('b', '', `0${number}`), element('span', '', episode.title));
  links.append(link);

  const section = element('section', 'episode');
  section.id = id;
  section.setAttribute('aria-labelledby', `${id}-title`);
  const header = element('header', 'episode-header');
  const heading = element('h2', '', episode.title);
  heading.id = `${id}-title`;
  header.append(element('span', 'number', `EPISODE 0${number} / ${episode.topic}`), heading, element('p', '', episode.intro));
  section.append(header);

  episode.panels.forEach((panel, p) => {
    const article = element('article', 'panel');
    article.append(element('p', 'scene-label', `${number}-${p + 1}  ${panel.scene}`));
    const art = element('div', 'art');
    art.style.backgroundImage = `url('assets/episode-${number}.png')`;
    const row = Math.floor(p / 2);
    const top = rowEdges[index][row];
    const height = rowEdges[index][row + 1] - top;
    art.style.aspectRatio = String((1 / 3) / height);
    art.style.backgroundSize = `200% ${100 / height}%`;
    art.style.backgroundPosition = `${(p % 2) * 100}% ${100 * top / (1 - height)}%`;
    art.setAttribute('role', 'img');
    art.setAttribute('aria-label', panel.alt);
    art.append(element('span', 'sfx', panel.sfx));
    article.append(art);
    const dialogue = element('div', 'dialogue');
    panel.talk.forEach(([speaker, words]) => {
      const bubble = element('div', `bubble${speaker === '파이' ? ' robot' : ''}`);
      bubble.append(element('span', 'speaker', speaker), element('p', '', words));
      dialogue.append(bubble);
    });
    article.append(dialogue);
    if (panel.code) article.append(element('pre', 'note', panel.code));
    if (panel.caption) article.append(element('p', 'panel-caption', panel.caption));
    section.append(article);
  });

  const checkpoint = element('aside', 'checkpoint');
  checkpoint.append(element('p', 'eyebrow', '잠깐, 하루의 질문!'), element('p', 'question', episode.quiz[0]));
  const answer = element('details');
  answer.append(element('summary', '', '파이의 답변 펼치기'), element('p', '', episode.quiz[1]));
  checkpoint.append(answer);
  section.append(checkpoint);
  const source = element('details', 'source');
  source.append(element('summary', '', '이 화의 원작 코드 · 실습 상태'));
  const files = element('ul');
  episode.files.forEach(([path, description]) => {
    const row = element('li');
    const fileLink = element('a', '', path);
    fileLink.href = `../${path}`;
    row.append(fileLink, document.createTextNode(` — ${description}`));
    files.append(row);
  });
  source.append(files, element('p', '', episode.sourceNote));
  section.append(source);
  host.append(section);
});

menu.addEventListener('change', () => { location.hash = menu.value; });
document.getElementById('type-toggle').addEventListener('click', event => {
  const large = document.body.classList.toggle('large-type');
  event.currentTarget.setAttribute('aria-pressed', String(large));
  event.currentTarget.textContent = large ? '기본 글씨' : '큰 글씨';
});
const progressBar = document.getElementById('progress-bar');
let scheduled = false;
function updateProgress() {
  const distance = document.documentElement.scrollHeight - innerHeight;
  progressBar.style.width = `${distance > 0 ? (scrollY / distance) * 100 : 0}%`;
  scheduled = false;
}
window.addEventListener('scroll', () => {
  if (!scheduled) { scheduled = true; requestAnimationFrame(updateProgress); }
}, { passive: true });
window.addEventListener('resize', updateProgress);
updateProgress();
