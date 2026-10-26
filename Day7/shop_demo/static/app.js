const descriptions = {
  sync: '재고 → 배송 → 리뷰 순서로 조회합니다. 일반 def 경로이므로 다른 손님의 요청은 처리할 수 있습니다.',
  async: 'asyncio.gather로 세 조회를 함께 시작합니다. await asyncio.sleep 동안 서로의 대기 시간을 겹칩니다.',
  blocking: 'async def 안에서 time.sleep을 호출합니다. 조회가 끝날 때까지 다른 손님의 상태 확인 요청도 밀립니다.'
};
const labels = {sync: '동기 · 순차', async: '비동기 · 동시', blocking: '서버 막힘'};
let mode = 'sync';
let records = [];
const $ = (id) => document.getElementById(id);
$('description').textContent = descriptions[mode];

document.querySelectorAll('.mode').forEach(button => {
  button.addEventListener('click', () => {
    mode = button.dataset.mode;
    document.querySelectorAll('.mode').forEach(item => {
      item.classList.toggle('active', item === button);
      item.setAttribute('aria-pressed', String(item === button));
    });
    $('description').textContent = descriptions[mode];
  });
});

// 같은 서버의 실제 API를 호출합니다. 화면 타이머는 브라우저 왕복 시간입니다.
async function request(path) {
  const response = await fetch(path, {cache: 'no-store', signal: AbortSignal.timeout(30000)});
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

function drawResults(data) {
  $('results').replaceChildren();
  $('timeline').replaceChildren();
  for (const result of data.results) {
    const row = document.createElement('div');
    row.textContent = result.name;
    const value = document.createElement('span');
    value.textContent = result.value;
    row.append(value);
    $('results').append(row);

    const trackRow = document.createElement('div');
    trackRow.className = 'track-row';
    const name = document.createElement('span');
    name.textContent = result.name;
    const track = document.createElement('div');
    track.className = 'track';
    const bar = document.createElement('div');
    bar.className = `bar ${data.mode}`;
    bar.style.left = `${result.started / data.elapsed * 100}%`;
    bar.style.width = `${(result.ended - result.started) / data.elapsed * 100}%`;
    track.append(bar);
    trackRow.append(name, track);
    const timing = document.createElement('p');
    timing.className = 'track-label';
    timing.textContent = `${result.started.toFixed(2)}초 시작 → ${result.ended.toFixed(2)}초 완료`;
    $('timeline').append(trackRow, timing);
  }
  $('server-time').textContent = `총 ${data.elapsed.toFixed(2)}초`;
}

function drawHistory() {
  $('history').replaceChildren();
  if (!records.length) {
    const row = $('history').insertRow();
    const cell = row.insertCell();
    cell.colSpan = 4;
    cell.textContent = '각 방식을 한 번씩 실행해 보세요.';
    cell.className = 'muted';
  }
  records.forEach(record => {
    const row = $('history').insertRow();
    [labels[record.mode], `${record.delay}초`, `${record.elapsed.toFixed(2)}초`, `${record.roundtrip.toFixed(2)}초`].forEach(value => {
      row.insertCell().textContent = value;
    });
  });
}

$('run').addEventListener('click', async () => {
  const selected = mode;
  const delay = Number($('delay').value);
  const controls = document.querySelectorAll('.mode, #run, #delay');
  controls.forEach(control => control.disabled = true);
  $('status').classList.remove('error');
  $('status').textContent = '조회 중입니다. 서버 응답 확인 버튼도 눌러 보세요.';
  $('server-time').textContent = '측정 중';
  $('timeline').replaceChildren();
  $('results').querySelectorAll('span').forEach(span => span.textContent = '조회 중…');
  const start = performance.now();
  const ticker = setInterval(() => $('timer').textContent = `${((performance.now() - start) / 1000).toFixed(2)}초`, 50);
  try {
    const data = await request(`/api/${selected}?delay=${delay}`);
    const roundtrip = (performance.now() - start) / 1000;
    drawResults(data);
    records.unshift({...data, delay, roundtrip});
    records = records.slice(0, 12);
    drawHistory();
    $('status').textContent = `${labels[selected]} 조회가 완료되었습니다.`;
  } catch (error) {
    $('status').textContent = `조회 실패: ${error.message}. 서버 실행 상태를 확인하세요.`;
    $('status').classList.add('error');
    $('server-time').textContent = '측정 실패';
    $('results').querySelectorAll('span').forEach(span => span.textContent = '조회 실패');
  } finally {
    clearInterval(ticker);
    $('timer').textContent = `${((performance.now() - start) / 1000).toFixed(2)}초`;
    controls.forEach(control => control.disabled = false);
  }
});

$('ping').addEventListener('click', async () => {
  $('ping').disabled = true;
  $('ping-result').textContent = '상태 확인 응답을 기다리는 중…';
  const start = performance.now();
  try {
    await request('/api/health');
    $('ping-result').textContent = `응답 도착 · ${((performance.now() - start) / 1000).toFixed(2)}초 소요`;
  } catch (error) {
    $('ping-result').textContent = `응답 실패: ${error.message}`;
  } finally {
    $('ping').disabled = false;
  }
});
$('clear').addEventListener('click', () => {records = []; drawHistory();});
