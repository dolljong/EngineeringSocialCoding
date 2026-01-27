/**
 * RC Section Calculator - Main Application
 * Converted from Python (ESC_RCSEC.py)
 * Using jspreadsheet for Excel-like interface
 */

const ROW_COUNT = 20;
const REBAR_DIAS = ['10', '13', '16', '19', '22', '25', '29', '32', '35'];

// Current calculation data
let currentCalcData = null;
let selectedRow = 0;
let spreadsheet = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initSpreadsheet();
    initEventListeners();
    updateStatus('Ready');
});

// Initialize jspreadsheet
function initSpreadsheet() {
    const container = document.getElementById('spreadsheet');

    // Sample data
    const data = [
        ['Center', 1000, 50, 5, 80, 800, 1000, 80, '25', 8, 1, '16', 2, 400, '', '', '']
    ];

    // Fill remaining rows with empty data
    for (let i = 1; i < ROW_COUNT; i++) {
        data.push(['', '', '', '', '', '', '', '', '13', '', 1, '16', '', '', '', '', '']);
    }

    spreadsheet = jspreadsheet(container, {
        data: data,
        columns: [
            { title: 'Name', type: 'text', width: 120 },
            { title: 'Mu\n(kN.m)', type: 'numeric', width: 70, decimal: '.' },
            { title: 'Vu\n(kN)', type: 'numeric', width: 70, decimal: '.' },
            { title: 'Nu\n(kN)', type: 'numeric', width: 70, decimal: '.' },
            { title: 'Ms\n(kN.m)', type: 'numeric', width: 70, decimal: '.' },
            { title: 'H\n(mm)', type: 'numeric', width: 60, decimal: '.' },
            { title: 'B\n(mm)', type: 'numeric', width: 60, decimal: '.' },
            { title: 'Dc\n(mm)', type: 'numeric', width: 60, decimal: '.' },
            { title: 'As_Dia\n(mm)', type: 'dropdown', width: 70, source: REBAR_DIAS },
            { title: 'As_Num\n(EA)', type: 'numeric', width: 70, decimal: '.' },
            { title: 'δ', type: 'numeric', width: 50, decimal: '.' },
            { title: 'Av_Dia\n(mm)', type: 'dropdown', width: 70, source: REBAR_DIAS },
            { title: 'Av_Leg\n(EA)', type: 'numeric', width: 70, decimal: '.' },
            { title: 'Av_Space\n(mm)', type: 'numeric', width: 80, decimal: '.' },
            { title: 'As_req\n(mm²)', type: 'text', width: 80, readOnly: true },
            { title: 'As_used\n(mm²)', type: 'text', width: 80, readOnly: true },
            { title: 'As_used\n/As_req', type: 'text', width: 80, readOnly: true }
        ],
        defaultColWidth: 70,
        tableOverflow: true,
        tableWidth: '100%',
        tableHeight: '400px',
        rowResize: true,
        columnDrag: false,
        allowInsertRow: false,
        allowDeleteRow: false,
        allowInsertColumn: false,
        allowDeleteColumn: false,
        selectionCopy: true,
        onselection: function(instance, x1, y1, x2, y2, origin) {
            selectedRow = y1;
        },
        updateTable: function(instance, cell, col, row, val, label, cellName) {
            // Style result columns
            if (col >= 14) {
                cell.style.backgroundColor = '#f0f8ff';
                cell.style.fontWeight = 'bold';

                // Color coding for ratio column
                if (col === 16 && val !== '' && val !== null) {
                    const ratio = parseFloat(val);
                    if (!isNaN(ratio)) {
                        if (ratio >= 1) {
                            cell.style.backgroundColor = '#e6ffe6';
                            cell.style.color = '#006600';
                        } else if (ratio > 0) {
                            cell.style.backgroundColor = '#ffe6e6';
                            cell.style.color = '#cc0000';
                        }
                    }
                }
            }
        }
    });

    // 드롭다운 셀 싱글 클릭으로 열기 (mouseup 이벤트 사용)
    container.addEventListener('mouseup', function(e) {
        const td = e.target.closest('td');
        if (td && td.dataset && td.dataset.x !== undefined) {
            const x = parseInt(td.dataset.x);
            const y = parseInt(td.dataset.y);
            // 드롭다운 컬럼(As_Dia:8, Av_Dia:11)인 경우
            if ((x === 8 || x === 11) && !isNaN(y)) {
                setTimeout(function() {
                    if (spreadsheet.records[y] && spreadsheet.records[y][x]) {
                        spreadsheet.openEditor(spreadsheet.records[y][x], true);
                    }
                }, 50);
            }
        }
    });
}

// Initialize event listeners
function initEventListeners() {
    // Toolbar buttons
    document.getElementById('calcBtn').addEventListener('click', calculate);
    document.getElementById('viewBtn').addEventListener('click', viewCalc);
    document.getElementById('exportBtn').addEventListener('click', exportToText);

    // Menu buttons
    document.getElementById('calcMenuBtn').addEventListener('click', calculate);
    document.getElementById('viewCalcBtn').addEventListener('click', viewCalc);
    document.getElementById('newBtn').addEventListener('click', newFile);
    document.getElementById('openBtn').addEventListener('click', openFile);
    document.getElementById('saveBtn').addEventListener('click', saveFile);
    document.getElementById('exportTextBtn').addEventListener('click', exportToText);

    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.dataset.tab;
            switchTab(tabId);
        });
    });

    // Modal
    document.getElementById('closeModal').addEventListener('click', closeModal);
    document.getElementById('closeCalcBtn').addEventListener('click', closeModal);
    document.getElementById('copyCalcBtn').addEventListener('click', copyCalcText);
    document.getElementById('saveCalcBtn').addEventListener('click', saveCalcText);

    // Calc tab switching
    document.querySelectorAll('.calc-tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.dataset.calcTab;
            switchCalcTab(tabId);
        });
    });

    // File input
    document.getElementById('fileInput').addEventListener('change', handleFileOpen);

    // Help menu
    document.getElementById('releaseBtn').addEventListener('click', showReleaseNotes);
    document.getElementById('closeReleaseModal').addEventListener('click', closeReleaseModal);
    document.getElementById('closeReleaseBtn').addEventListener('click', closeReleaseModal);
}

// Switch main tabs
function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabId);
    });
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('hidden', content.id !== tabId);
    });
}

// Switch calculation tabs in modal
function switchCalcTab(tabId) {
    document.querySelectorAll('.calc-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.calcTab === tabId);
    });

    const tabs = ['full', 'moment', 'shear', 'service'];
    tabs.forEach(t => {
        const el = document.getElementById(t + 'Calc');
        el.classList.toggle('hidden', t !== tabId);
    });
}

// Get material data
function getMaterialData() {
    return {
        fck: parseFloat(document.getElementById('fck').value) || 35,
        fy: parseFloat(document.getElementById('fy').value) || 400,
        Oc: parseFloat(document.getElementById('Oc').value) || 0.85,
        Os: parseFloat(document.getElementById('Os').value) || 0.85
    };
}

// Get row data from spreadsheet
function getRowData(rowIndex) {
    const data = spreadsheet.getRowData(rowIndex);
    if (!data || !data[0] || data[0].toString().trim() === '') return null;

    const getValue = (val, defaultVal = 0) => {
        if (val === '' || val === null || val === undefined) return defaultVal;
        const num = parseFloat(val);
        return isNaN(num) ? defaultVal : num;
    };

    return {
        name: data[0].toString().trim(),
        Mu: getValue(data[1]),
        Vu: getValue(data[2]),
        Nu: getValue(data[3]),
        Ms: getValue(data[4]),
        H: getValue(data[5]),
        B: getValue(data[6]),
        Dc: getValue(data[7]),
        As_Dia: getValue(data[8], 13),
        As_Num: getValue(data[9]),
        delta: getValue(data[10], 1),
        Av_Dia: getValue(data[11], 16),
        Av_Leg: getValue(data[12], 2),
        Av_Space: getValue(data[13], 300)
    };
}

// Set result cells in spreadsheet
function setResultCells(rowIndex, Asreq, Asused, ratio) {
    spreadsheet.setValueFromCoords(14, rowIndex, Asreq.toFixed(1), true);
    spreadsheet.setValueFromCoords(15, rowIndex, Asused.toFixed(1), true);
    spreadsheet.setValueFromCoords(16, rowIndex, ratio.toFixed(2), true);
}

// Calculate all sections
function calculate() {
    try {
        const mat = getMaterialData();
        let calcCount = 0;
        let insufficientSections = [];

        for (let i = 0; i < ROW_COUNT; i++) {
            const rowData = getRowData(i);
            if (!rowData || rowData.H <= 0 || rowData.B <= 0) continue;

            // Prepare data lists
            const datalist = [mat.fck, mat.fy];
            const datalist1 = [mat.Oc, mat.Os];
            const datalist2 = [rowData.H, rowData.B];
            const datalist3 = [
                Math.round(rowData.As_Dia), Math.round(rowData.As_Num), rowData.Dc,
                0, 0, 0,
                0, 0, 0
            ];
            const datalist4 = [
                Math.round(rowData.Av_Dia), Math.round(rowData.Av_Leg), rowData.Av_Space,
                3, 0, 90
            ];
            const datalist5 = [rowData.Mu, rowData.Vu, rowData.Nu, rowData.Ms, rowData.Ms, 1];

            // Create calculator and run
            const sec = new SecBack(datalist, datalist1, datalist2, datalist3, datalist4, datalist5);
            sec.delta = rowData.delta;
            sec.calmoment();
            sec.calshear();

            // Update results
            const ratio = sec.Asreq > 0 ? sec.Asuse / sec.Asreq : 0;
            setResultCells(i, sec.Asreq, sec.Asuse, ratio);
            calcCount++;

            // Collect insufficient sections
            if (ratio > 0 && ratio < 1.0) {
                insufficientSections.push({
                    name: rowData.name,
                    As_req: sec.Asreq,
                    As_used: sec.Asuse,
                    ratio: ratio
                });
            }
        }

        updateStatus(`계산 완료 (${calcCount}개 단면)`);

        // Alert for insufficient sections
        if (insufficientSections.length > 0) {
            let msg = '철근량이 부족한 단면이 있습니다.\n\n';
            msg += '단면명\t\t필요철근량\t사용철근량\t비율\n';
            msg += '─'.repeat(25) + '\n';
            for (const sec of insufficientSections) {
                msg += `${sec.name}\t\t${sec.As_req.toFixed(1)}\t\t${sec.As_used.toFixed(1)}\t\t${sec.ratio.toFixed(2)}\n`;
            }
            alert(msg);
        }
    } catch (e) {
        console.error('Calculation error:', e);
        updateStatus('계산 오류: ' + e.message);
    }
}

// View calculation for selected row
function viewCalc() {
    try {
        const rowData = getRowData(selectedRow);
        if (!rowData) {
            alert('계산과정을 볼 행을 선택하세요.');
            return;
        }

        if (rowData.H <= 0 || rowData.B <= 0) {
            alert('단면 치수가 유효하지 않습니다.');
            return;
        }

        const mat = getMaterialData();

        // Prepare data lists
        const datalist = [mat.fck, mat.fy];
        const datalist1 = [mat.Oc, mat.Os];
        const datalist2 = [rowData.H, rowData.B];
        const datalist3 = [
            Math.round(rowData.As_Dia), Math.round(rowData.As_Num), rowData.Dc,
            0, 0, 0,
            0, 0, 0
        ];
        const datalist4 = [
            Math.round(rowData.Av_Dia), Math.round(rowData.Av_Leg), rowData.Av_Space,
            3, 0, 90
        ];
        const datalist5 = [rowData.Mu, rowData.Vu, rowData.Nu, rowData.Ms, rowData.Ms, 1];

        // Create calculator and run
        const sec = new SecBack(datalist, datalist1, datalist2, datalist3, datalist4, datalist5);
        sec.delta = rowData.delta;
        sec.calmoment();
        sec.calshear();
        sec.calservice();

        currentCalcData = sec;

        // Update modal
        document.getElementById('modalTitle').textContent = `계산과정 - ${rowData.name}`;
        document.getElementById('fullCalc').textContent = getFullCalcText(sec);
        document.getElementById('momentCalc').textContent = getMomentText(sec);
        document.getElementById('shearCalc').textContent = getShearText(sec);
        document.getElementById('serviceCalc').textContent = getServiceText(sec);

        // Show modal
        document.getElementById('calcViewerModal').classList.add('show');
        switchCalcTab('full');
    } catch (e) {
        console.error('View calc error:', e);
        alert('계산과정 표시 오류: ' + e.message);
    }
}

// Close modal
function closeModal() {
    document.getElementById('calcViewerModal').classList.remove('show');
}

// Copy calculation text
function copyCalcText() {
    const text = document.getElementById('fullCalc').textContent;
    navigator.clipboard.writeText(text).then(() => {
        alert('계산과정이 클립보드에 복사되었습니다.');
    }).catch(err => {
        console.error('Copy failed:', err);
    });
}

// Save calculation text
function saveCalcText() {
    const rowData = getRowData(selectedRow);
    const text = document.getElementById('fullCalc').textContent;
    downloadFile(text, `${rowData.name}_계산서.txt`, 'text/plain');
}

// Export all to text
function exportToText() {
    try {
        const mat = getMaterialData();
        let allText = [];

        allText.push('='.repeat(80));
        allText.push('RC 단면 검토 계산서');
        allText.push('='.repeat(80));
        allText.push('');
        allText.push('재료 물성:');
        allText.push(`  - 콘크리트 설계기준강도 fck = ${mat.fck} MPa`);
        allText.push(`  - 철근 항복강도 fy = ${mat.fy} MPa`);
        allText.push(`  - 콘크리트 강도감소계수 Øc = ${mat.Oc}`);
        allText.push(`  - 철근 강도감소계수 Øs = ${mat.Os}`);
        allText.push('');

        let sectionCount = 0;

        for (let i = 0; i < ROW_COUNT; i++) {
            const rowData = getRowData(i);
            if (!rowData || rowData.H <= 0 || rowData.B <= 0) continue;

            const datalist = [mat.fck, mat.fy];
            const datalist1 = [mat.Oc, mat.Os];
            const datalist2 = [rowData.H, rowData.B];
            const datalist3 = [
                Math.round(rowData.As_Dia), Math.round(rowData.As_Num), rowData.Dc,
                0, 0, 0, 0, 0, 0
            ];
            const datalist4 = [
                Math.round(rowData.Av_Dia), Math.round(rowData.Av_Leg), rowData.Av_Space,
                3, 0, 90
            ];
            const datalist5 = [rowData.Mu, rowData.Vu, rowData.Nu, rowData.Ms, rowData.Ms, 1];

            const sec = new SecBack(datalist, datalist1, datalist2, datalist3, datalist4, datalist5);
            sec.delta = rowData.delta;
            sec.calmoment();
            sec.calshear();
            sec.calservice();

            allText.push('');
            allText.push('='.repeat(80));
            allText.push(`[${rowData.name}]`);
            allText.push('='.repeat(80));
            allText.push('');
            allText.push(getFullCalcText(sec));

            sectionCount++;
        }

        if (sectionCount === 0) {
            alert('출력할 단면 데이터가 없습니다.');
            return;
        }

        downloadFile(allText.join('\n'), 'RC_Section_Calc.txt', 'text/plain');
        updateStatus(`텍스트 저장 완료 (${sectionCount}개 단면)`);
    } catch (e) {
        console.error('Export error:', e);
        alert('텍스트 저장 오류: ' + e.message);
    }
}

// New file
function newFile() {
    if (confirm('모든 데이터를 초기화하시겠습니까?')) {
        // Reset material
        document.getElementById('fck').value = '35';
        document.getElementById('fy').value = '400';
        document.getElementById('Oc').value = '0.85';
        document.getElementById('Os').value = '0.85';

        // Reset spreadsheet
        const emptyData = [];
        for (let i = 0; i < ROW_COUNT; i++) {
            emptyData.push(['', '', '', '', '', '', '', '', '13', '', 1, '16', '', '', '', '', '']);
        }
        spreadsheet.setData(emptyData);

        updateStatus('새 파일');
    }
}

// Save file
function saveFile() {
    try {
        const mat = getMaterialData();
        const sections = [];

        for (let i = 0; i < ROW_COUNT; i++) {
            const rowData = getRowData(i);
            if (!rowData) continue;

            sections.push({
                name: rowData.name,
                forces: {
                    Mu: rowData.Mu,
                    Vu: rowData.Vu,
                    Nu: rowData.Nu,
                    Ms: rowData.Ms
                },
                geometry: {
                    H: rowData.H,
                    B: rowData.B,
                    Dc: rowData.Dc
                },
                flexure_rebar: {
                    dia: rowData.As_Dia,
                    num: rowData.As_Num
                },
                delta: rowData.delta,
                shear_rebar: {
                    dia: rowData.Av_Dia,
                    leg: rowData.Av_Leg,
                    space: rowData.Av_Space
                }
            });
        }

        const data = {
            version: '1.0',
            material: mat,
            sections: sections
        };

        downloadFile(JSON.stringify(data, null, 2), 'section_data.rcsec', 'application/json');
        updateStatus('파일 저장 완료');
    } catch (e) {
        console.error('Save error:', e);
        alert('파일 저장 오류: ' + e.message);
    }
}

// Open file
function openFile() {
    document.getElementById('fileInput').click();
}

// Handle file open
function handleFileOpen(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            loadData(data);
            updateStatus('파일 불러오기 완료');
        } catch (err) {
            console.error('Load error:', err);
            alert('파일 형식 오류: ' + err.message);
        }
    };
    reader.readAsText(file);

    // Reset input
    e.target.value = '';
}

// Load data from JSON
function loadData(data) {
    // Load material
    const mat = data.material || {};
    document.getElementById('fck').value = mat.fck || 35;
    document.getElementById('fy').value = mat.fy || 400;
    document.getElementById('Oc').value = mat.Oc || 0.85;
    document.getElementById('Os').value = mat.Os || 0.85;

    // Prepare spreadsheet data
    const sheetData = [];
    for (let i = 0; i < ROW_COUNT; i++) {
        sheetData.push(['', '', '', '', '', '', '', '', '13', '', 1, '16', '', '', '', '', '']);
    }

    // Load sections
    const sections = data.sections || [];
    sections.forEach((section, i) => {
        if (i >= ROW_COUNT) return;

        sheetData[i] = [
            section.name || '',
            section.forces?.Mu || '',
            section.forces?.Vu || '',
            section.forces?.Nu || '',
            section.forces?.Ms || '',
            section.geometry?.H || '',
            section.geometry?.B || '',
            section.geometry?.Dc || '',
            String(Math.round(section.flexure_rebar?.dia || 13)),
            section.flexure_rebar?.num || '',
            section.delta || 1,
            String(Math.round(section.shear_rebar?.dia || 16)),
            section.shear_rebar?.leg || '',
            section.shear_rebar?.space || '',
            '', '', ''
        ];
    });

    spreadsheet.setData(sheetData);
}

// Download file helper
function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType + ';charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Update status bar
function updateStatus(message) {
    document.getElementById('statusText').textContent = message;
}

// Show release notes
function showReleaseNotes() {
    const releaseContent = `# ESC_RCSEC WEB Release Notes

## v1.2 (2026-01-26)
- Excel 스타일 스프레드시트 UI 적용 (jspreadsheet)
- 셀 복사/붙여넣기, 드래그 선택 등 Excel 기능 지원

## v1.1 (2026-01-26)
- phi_c, phi_s 기본값 0.85로 변경
- 예제 데이터 Mu 값 1000으로 변경
- 철근량 부족(As_used/As_req < 1.0) 시 경고 알림창 추가
- Release Notes 보기 기능 추가

## v1.0 (2026-01-25)
- 초기 WEB APP 버전
- Python ESC_RCSEC.py를 JavaScript로 변환
- 휨모멘트, 전단력, 사용성 검토 기능
- 계산과정 뷰어 (전체/휨모멘트/전단력/사용성 탭)
- 텍스트 내보내기 기능
- 데이터 저장/불러오기 기능 (.rcsec)`;

    document.getElementById('releaseContent').textContent = releaseContent;
    document.getElementById('releaseModal').classList.add('show');
}

// Close release notes modal
function closeReleaseModal() {
    document.getElementById('releaseModal').classList.remove('show');
}
