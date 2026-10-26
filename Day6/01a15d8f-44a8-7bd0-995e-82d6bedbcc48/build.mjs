import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
import sharp from 'sharp';

const out = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(out, '../..');
const source = await fs.readFile(path.join(root, 'glossary/2026-10-21-day6-code-reference.md'), 'utf8');
const sections = source.split(/^## /m).slice(1).map(s => ({title:s.split('\n')[0].trim(), body:s.slice(s.indexOf('\n')+1)}));
const names = ['학습 안내','01 기초 문법','02 클래스와 타입','03 Field 입력 조건','04 Validator','05 중첩 모델','06 변환과 부분 수정','07 FastAPI','08 저장소와 검색','09 연결 예제','혼동과 원본 주의점'];
const selected = sections.filter(s=>s.title==='답변'||/^\d\./.test(s.title)||s.title==='헷갈리기 쉬운 점');
selected[0].body += '\n' + sections.find(s=>s.title==='참고 자료').body;
const clean = s => s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_,label,url)=>`${label} (${url})`).replace(/`/g,'').replace(/\*\*/g,'').replace(/\\\|/g,'|').trim();
const safe = s => s.startsWith('=') ? "'"+s : s;
const wb=Workbook.create();
const metadata=[];
let tableId=0, sourceRows=0, writtenRows=0;
function height(cells) {
  const widths=[48,60,60];
  return Math.max(42,...cells.map((s,i)=>{
    const n=s.split('\n').reduce((sum,line)=>sum+Math.max(1,Math.ceil([...line].reduce((a,c)=>a+(c.charCodeAt(0)>255?2:1),0)/widths[i])),0);
    return n*17+16;
  }));
}
for (let idx=0;idx<selected.length;idx++) {
  const section=selected[idx], sheet=wb.worksheets.add(names[idx]);
  sheet.showGridLines=false;
  sheet.getRange('A1:C500').format.font={name:'Arial',size:11,color:'#243247'};
  sheet.getRange('A1:A500').format.columnWidth=52;
  sheet.getRange('B1:C500').format.columnWidth=65;
  sheet.getRange('A2').values=[[idx===0?'Day_6 코드·문법 정리':section.title]];
  sheet.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:'#243E63'};
  sheet.getRange('A2:C2').format.rowHeight=30;
  sheet.getRange('A3:C3').format.borders={bottom:{style:'thin',color:'#9FB1CA'}};
  let row=5;
  const lines=section.body.split(/\r?\n/);
  const writeNote=(label,text)=>{
    const vals=[label,safe(clean(text)),''];
    sheet.getRange(`A${row}:C${row}`).values=[vals];
    sheet.getRange(`A${row}:C${row}`).format.wrapText=true;
    sheet.getRange(`A${row}:C${row}`).format.verticalAlignment='top';
    sheet.getRange(`A${row}:C${row}`).format.rowHeight=height(vals);
    sheet.getRange(`A${row}`).format.font.bold=true;
    row++;
  };
  // Tables are placed first so the opening view is a useful reference.
  const notes=[];
  for(let i=0;i<lines.length;i++) {
    if(lines[i].startsWith('|')) {
      const block=[];
      while(i<lines.length&&lines[i].startsWith('|')) {
        const cells=lines[i].slice(1,-1).split(/(?<!\\)\|/).map(clean);
        if(!cells.every(c=>/^[- :]+$/.test(c))) block.push(cells);
        i++;
      }
      i--;
      if(block.some(c=>c.length>3)) throw new Error('Unexpected table width');
      const ncols=block[0].length, last=ncols===2?'B':'C';
      const first=row;
      sheet.getRange(`A${row}:${last}${row+block.length-1}`).values=block.map(c=>c.map(safe));
      const table=sheet.tables.add(`A${row}:${last}${row+block.length-1}`,true,`Reference${++tableId}`);
      table.showFilterButton=true;
      for(let k=0;k<block.length;k++) {
        const rg=sheet.getRange(`A${row+k}:${last}${row+k}`);
        rg.format.wrapText=true; rg.format.verticalAlignment='top';
        rg.format.rowHeight=k===0?32:height(block[k]);
        rg.format.fill=k===0?'#243E63':(k%2?'#F0F4F9':'#FFFFFF');
        if(k===0) {rg.format.font={name:'Arial',size:11,bold:true,color:'#FFFFFF'};rg.format.horizontalAlignment='center';}
      }
      const saved=sheet.getRange(`A${row+1}:${last}${row+block.length-1}`).values;
      if(saved.length!==block.length-1) throw new Error('Range count mismatch');
      sourceRows+=block.length-1;writtenRows+=saved.length;
      if(first===5) sheet.freezePanes.freezeRows(5);
      row+=block.length+2;
    } else if(lines[i].startsWith('```')) {
      let code=[];i++;
      while(i<lines.length&&!lines[i].startsWith('```')) code.push(lines[i++]);
      notes.push(['코드 예제',code.join('\n')]);
    } else if(lines[i].trim()) notes.push(['설명',lines[i]]);
  }
  for(const [label,txt] of notes) writeNote(label,txt);
  metadata.push({sheet:sheet.name,rows:row-1});
}
if(sourceRows!==writtenRows) throw new Error('Table count mismatch');
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:"'02 클래스와 타입'!A5:C8",include:'values,formulas',maxChars:1600,tableMaxRows:4,tableMaxCols:3})).ndjson);
await fs.mkdir(path.join(out,'previews'),{recursive:true});
const thumbs=[];
for(let i=0;i<metadata.length;i++) {
  const blob=await wb.render({sheetName:metadata[i].sheet,range:'A1:C10',scale:1,format:'png'});
  const bytes=new Uint8Array(await blob.arrayBuffer());
  await fs.writeFile(path.join(out,'previews',`${i}.png`),bytes);
  thumbs.push(await sharp(bytes).resize({width:700}).png().toBuffer());
}
let y=0;const composite=[];
for(const b of thumbs) {const m=await sharp(b).metadata();composite.push({input:b,left:0,top:y});y+=m.height;}
await sharp({create:{width:700,height:y,channels:3,background:'#ffffff'}}).composite(composite).png().toFile(path.join(out,'previews/contact.png'));
const file=path.join(out,'Day_6_코드_문법_정리.xlsx');
await (await SpreadsheetFile.exportXlsx(wb)).save(file);
console.log(JSON.stringify({file,sourceRows,writtenRows,sheets:metadata},null,2));
