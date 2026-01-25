/**
 * RC Section Calculator - Main Application
 * Converted from Python (ESC_RCSEC.py)
 */

const ROW_COUNT = 20;
const REBAR_DIAS = ['10', '13', '16', '19', '22', '25', '29', '32', '35'];

// Current calculation data
let currentCalcData = null;
let selectedRow = 0;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initTable();
    initEventListeners();
    loadSampleData();
    updateStatus('Ready');
});

// Initialize the data table
function initTable() {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';

    for (let i = 0; i < ROW_COUNT; i++) {
        const row = document.createElement('tr');
        row.dataset.row = i;

        // Name
        row.innerHTML += `<td class="col-name"><input type="text" data-col="0"></td>`;

        // Forces: Mu, Vu, Nu, Ms
        for (let j = 1; j <= 4; j++) {
            row.innerHTML += `<td class="col-force"><input type="number" data-col="${j}" step="0.1"></td>`;
        }

        // Section: H, B, Dc
        for (let j = 5; j <= 7; j++) {
            row.innerHTML += `<td class="col-sec"><input type="number" data-col="${j}" step="1"></td>`;
        }

        // Band rebar: As_Dia (dropdown), As_Num
        row.innerHTML += `<td class="col-band"><select data-col="8">${REBAR_DIAS.map(d => `<option value="${d}">${d}</option>`).join('')}</select></td>`;
        row.innerHTML += `<td class="col-band"><input type="number" data-col="9" step="1"></td>`;

        // Shear rebar: δ, Av_Dia (dropdown), Av_Leg, Av_Space
        row.innerHTML += `<td class="col-shear"><input type="number" data-col="10" step="0.01" value="1"></td>`;
        row.innerHTML += `<td class="col-shear"><select data-col="11">${REBAR_DIAS.map(d => `<option value="${d}">${d}</option>`).join('')}</select></td>`;
        row.innerHTML += `<td class="col-shear"><input type="number" data-col="12" step="1"></td>`;
        row.innerHTML += `<td class="col-shear"><input type="number" data-col="13" step="1"></td>`;

        // Results: As_req, As_used, ratio
        row.innerHTML += `<td class="col-result result-cell" data-col="14"></td>`;
        row.innerHTML += `<td class="col-result result-cell" data-col="15"></td>`;
        row.innerHTML += `<td class="col-result result-cell" data-col="16"></td>`;

        tbody.appendChild(row);

        // Set default values
        row.querySelector('[data-col="8"]').value = '13';
        row.querySelector('[data-col="11"]').value = '16';
    }

    // Add row click handler
    tbody.addEventListener('click', function(e) {
        const row = e.target.closest('tr');
        if (row) {
            selectedRow = parseInt(row.dataset.row);
            highlightRow(selectedRow);
        }
    });
}

function highlightRow(rowIndex) {
    const rows = document.querySelectorAll('#tableBody tr');
    rows.forEach((row, i) => {
        row.classList.toggle('selected', i === rowIndex);
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

    // Checkbox toggles
    document.getElementById('showForces').addEventListener('change', toggleColumns);
    document.getElementById('showSecInfo').addEventListener('change', toggleColumns);
    document.getElementById('showBandRebar').addEventListener('change', toggleColumns);
    document.getElementById('showShearRebar').addEventListener('change', toggleColumns);

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
}

// Load sample data
function loadSampleData() {
    const sampleData = ['Center', '100', '50', '5', '80', '800', '1000', '80', '25', '8', '1', '16', '2', '400'];
    const row = document.querySelector('#tableBody tr[data-row="0"]');

    row.querySelector('[data-col="0"]').value = sampleData[0];
    for (let i = 1; i <= 7; i++) {
        row.querySelector(`[data-col="${i}"]`).value = sampleData[i];
    }
    row.querySelector('[data-col="8"]').value = sampleData[8];
    row.querySelector('[data-col="9"]').value = sampleData[9];
    row.querySelector('[data-col="10"]').value = sampleData[10];
    row.querySelector('[data-col="11"]').value = sampleData[11];
    row.querySelector('[data-col="12"]').value = sampleData[12];
    row.querySelector('[data-col="13"]').value = sampleData[13];
}

// Toggle column visibility
function toggleColumns() {
    const showForces = document.getElementById('showForces').checked;
    const showSecInfo = document.getElementById('showSecInfo').checked;
    const showBandRebar = document.getElementById('showBandRebar').checked;
    const showShearRebar = document.getElementById('showShearRebar').checked;

    document.querySelectorAll('.col-force').forEach(el => {
        el.classList.toggle('hidden', !showForces);
    });
    document.querySelectorAll('.col-sec').forEach(el => {
        el.classList.toggle('hidden', !showSecInfo);
    });
    document.querySelectorAll('.col-band').forEach(el => {
        el.classList.toggle('hidden', !showBandRebar);
    });
    document.querySelectorAll('.col-shear').forEach(el => {
        el.classList.toggle('hidden', !showShearRebar);
    });
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
        Oc: parseFloat(document.getElementById('Oc').value) || 0.65,
        Os: parseFloat(document.getElementById('Os').value) || 0.7
    };
}

// Get row data
function getRowData(rowIndex) {
    const row = document.querySelector(`#tableBody tr[data-row="${rowIndex}"]`);
    if (!row) return null;

    const getValue = (col, defaultVal = 0) => {
        const input = row.querySelector(`[data-col="${col}"]`);
        if (!input) return defaultVal;
        const val = parseFloat(input.value);
        return isNaN(val) ? defaultVal : val;
    };

    const getTextValue = (col) => {
        const input = row.querySelector(`[data-col="${col}"]`);
        return input ? input.value.trim() : '';
    };

    const name = getTextValue(0);
    if (!name) return null;

    return {
        name: name,
        Mu: getValue(1),
        Vu: getValue(2),
        Nu: getValue(3),
        Ms: getValue(4),
        H: getValue(5),
        B: getValue(6),
        Dc: getValue(7),
        As_Dia: getValue(8, 13),
        As_Num: getValue(9),
        delta: getValue(10, 1),
        Av_Dia: getValue(11, 16),
        Av_Leg: getValue(12, 2),
        Av_Space: getValue(13, 300)
    };
}

// Set result cells
function setResultCells(rowIndex, Asreq, Asused, ratio) {
    const row = document.querySelector(`#tableBody tr[data-row="${rowIndex}"]`);
    if (!row) return;

    const cells = row.querySelectorAll('.result-cell');
    cells[0].textContent = Asreq.toFixed(1);
    cells[1].textContent = Asused.toFixed(1);
    cells[2].textContent = ratio.toFixed(2);

    // Color coding
    if (ratio >= 1) {
        cells[2].classList.add('result-ok');
        cells[2].classList.remove('result-ng');
    } else {
        cells[2].classList.add('result-ng');
        cells[2].classList.remove('result-ok');
    }
}

// Calculate all sections
function calculate() {
    try {
        const mat = getMaterialData();
        let calcCount = 0;

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
        }

        updateStatus(`계산 완료 (${calcCount}개 단면)`);
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
        document.getElementById('Oc').value = '0.65';
        document.getElementById('Os').value = '0.7';

        // Reset table
        for (let i = 0; i < ROW_COUNT; i++) {
            const row = document.querySelector(`#tableBody tr[data-row="${i}"]`);
            for (let j = 0; j <= 13; j++) {
                const input = row.querySelector(`[data-col="${j}"]`);
                if (input) {
                    if (j === 8) input.value = '13';
                    else if (j === 10) input.value = '1';
                    else if (j === 11) input.value = '16';
                    else if (input.tagName === 'INPUT') input.value = '';
                }
            }
            // Clear results
            row.querySelectorAll('.result-cell').forEach(cell => {
                cell.textContent = '';
                cell.classList.remove('result-ok', 'result-ng');
            });
        }

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
    document.getElementById('Oc').value = mat.Oc || 0.65;
    document.getElementById('Os').value = mat.Os || 0.7;

    // Clear table first
    for (let i = 0; i < ROW_COUNT; i++) {
        const row = document.querySelector(`#tableBody tr[data-row="${i}"]`);
        for (let j = 0; j <= 13; j++) {
            const input = row.querySelector(`[data-col="${j}"]`);
            if (input) {
                if (j === 8) input.value = '13';
                else if (j === 10) input.value = '1';
                else if (j === 11) input.value = '16';
                else if (input.tagName === 'INPUT') input.value = '';
            }
        }
        row.querySelectorAll('.result-cell').forEach(cell => {
            cell.textContent = '';
            cell.classList.remove('result-ok', 'result-ng');
        });
    }

    // Load sections
    const sections = data.sections || [];
    sections.forEach((section, i) => {
        if (i >= ROW_COUNT) return;

        const row = document.querySelector(`#tableBody tr[data-row="${i}"]`);

        row.querySelector('[data-col="0"]').value = section.name || '';
        row.querySelector('[data-col="1"]').value = section.forces?.Mu || '';
        row.querySelector('[data-col="2"]').value = section.forces?.Vu || '';
        row.querySelector('[data-col="3"]').value = section.forces?.Nu || '';
        row.querySelector('[data-col="4"]').value = section.forces?.Ms || '';
        row.querySelector('[data-col="5"]').value = section.geometry?.H || '';
        row.querySelector('[data-col="6"]').value = section.geometry?.B || '';
        row.querySelector('[data-col="7"]').value = section.geometry?.Dc || '';
        row.querySelector('[data-col="8"]').value = Math.round(section.flexure_rebar?.dia || 13);
        row.querySelector('[data-col="9"]').value = section.flexure_rebar?.num || '';
        row.querySelector('[data-col="10"]').value = section.delta || 1;
        row.querySelector('[data-col="11"]').value = Math.round(section.shear_rebar?.dia || 16);
        row.querySelector('[data-col="12"]').value = section.shear_rebar?.leg || '';
        row.querySelector('[data-col="13"]').value = section.shear_rebar?.space || '';
    });
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
