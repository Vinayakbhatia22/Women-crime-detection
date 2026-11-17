document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide icons
  if (window.lucide) {
    lucide.createIcons();
  }

  const rawData = window.CRIME_DATA || [];
  const crimeCols = window.CRIME_COLS || ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT'];
  const crimeLabels = window.CRIME_LABELS || {};

  // Color Palette tailored for dark theme
  const crimeColors = {
    'DV': '#EC4899',   // Pink / Domestic Violence
    'AoW': '#F59E0B',  // Amber / Assault on Women
    'K&A': '#6366F1',  // Indigo / Kidnap & Abduction
    'Rape': '#EF4444', // Red / Rape
    'AoM': '#10B981',  // Emerald / Insult to Modesty
    'DD': '#8B5CF6',   // Purple / Dowry Deaths
    'WT': '#06B6D4'    // Cyan / Trafficking
  };

  // State variables
  let currentFilters = {
    state: 'ALL',
    year: 'ALL',
    crime: 'ALL',
    search: ''
  };

  let sortConfig = {
    column: 'total',
    direction: 'desc'
  };

  // Chart instances
  let trendChartInstance = null;
  let compositionChartInstance = null;
  let hotspotsChartInstance = null;
  let growthChartInstance = null;

  // DOM Elements
  const stateSelect = document.getElementById('stateSelect');
  const yearSelect = document.getElementById('yearSelect');
  const stateSearch = document.getElementById('stateSearch');
  const resetFiltersBtn = document.getElementById('resetFiltersBtn');
  const exportCsvBtn = document.getElementById('exportCsvBtn');
  const crimePills = document.querySelectorAll('.pill-btn');
  const tableBody = document.getElementById('crimeTableBody');
  const tableMetaInfo = document.getElementById('tableMetaInfo');

  // Populate Dropdowns
  const allStates = [...new Set(rawData.map(r => r.state))].sort();
  allStates.forEach(st => {
    const opt = document.createElement('option');
    opt.value = st;
    opt.textContent = st;
    stateSelect.appendChild(opt);
  });

  const allYears = [...new Set(rawData.map(r => r.year))].sort((a,b) => a - b);
  allYears.forEach(y => {
    const opt = document.createElement('option');
    opt.value = y;
    opt.textContent = `Year ${y}`;
    yearSelect.appendChild(opt);
  });

  // Event Listeners
  stateSelect.addEventListener('change', (e) => {
    currentFilters.state = e.target.value;
    updateDashboard();
  });

  yearSelect.addEventListener('change', (e) => {
    currentFilters.year = e.target.value === 'ALL' ? 'ALL' : parseInt(e.target.value);
    updateDashboard();
  });

  stateSearch.addEventListener('input', (e) => {
    currentFilters.search = e.target.value.toLowerCase().trim();
    renderTable();
  });

  crimePills.forEach(pill => {
    pill.addEventListener('click', () => {
      crimePills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      currentFilters.crime = pill.dataset.crime;
      updateDashboard();
    });
  });

  resetFiltersBtn.addEventListener('click', () => {
    currentFilters = { state: 'ALL', year: 'ALL', crime: 'ALL', search: '' };
    stateSelect.value = 'ALL';
    yearSelect.value = 'ALL';
    stateSearch.value = '';
    crimePills.forEach(p => p.classList.remove('active'));
    document.querySelector('.pill-btn[data-crime="ALL"]').classList.add('active');
    updateDashboard();
  });

  // Table Sorting Listeners
  document.querySelectorAll('th[data-sort]').forEach(th => {
    th.addEventListener('click', () => {
      const col = th.dataset.sort;
      if (sortConfig.column === col) {
        sortConfig.direction = sortConfig.direction === 'asc' ? 'desc' : 'asc';
      } else {
        sortConfig.column = col;
        sortConfig.direction = 'desc';
      }
      renderTable();
    });
  });

  exportCsvBtn.addEventListener('click', exportFilteredCsv);

  // Core Data Filtering Logic
  function getFilteredData() {
    return rawData.filter(r => {
      if (currentFilters.state !== 'ALL' && r.state !== currentFilters.state) return false;
      if (currentFilters.year !== 'ALL' && r.year !== currentFilters.year) return false;
      return true;
    });
  }

  // Update Everything
  function updateDashboard() {
    const filtered = getFilteredData();
    updateKPIs(filtered);
    renderTrendChart();
    renderCompositionChart(filtered);
    renderHotspotsChart();
    renderGrowthChart();
    renderTable();
    if (window.lucide) lucide.createIcons();
  }

  // 1. Update KPIs (All 6 Cards Dynamic)
  function updateKPIs(filtered) {
    let total = 0;
    if (currentFilters.crime === 'ALL') {
      total = filtered.reduce((sum, r) => sum + r.total, 0);
    } else {
      total = filtered.reduce((sum, r) => sum + (r[currentFilters.crime] || 0), 0);
    }

    document.getElementById('valTotalCases').textContent = total.toLocaleString();

    let meta = "";
    if (currentFilters.state !== 'ALL' && currentFilters.year !== 'ALL') {
      meta = `${currentFilters.state} in ${currentFilters.year}`;
    } else if (currentFilters.state !== 'ALL') {
      meta = `${currentFilters.state} (2001–2021 Cumulative)`;
    } else if (currentFilters.year !== 'ALL') {
      meta = `All India Total for Year ${currentFilters.year}`;
    } else {
      meta = `All India Total (2001–2021 Cumulative)`;
    }

    if (currentFilters.crime !== 'ALL') {
      meta += ` • ${crimeLabels[currentFilters.crime] || currentFilters.crime}`;
    }
    document.getElementById('metaTotalCases').textContent = meta;

    // State-filtered rows across years for growth/surge/drop KPIs
    const stateRows = currentFilters.state === 'ALL'
      ? rawData
      : rawData.filter(r => r.state === currentFilters.state);
    const sortedYears = [...new Set(stateRows.map(r => r.year))].sort((a, b) => a - b);
    const firstYr = sortedYears[0] || 2001;
    const lastYr = sortedYears.includes(2019) && currentFilters.state !== 'ALL' ? 2019 : (sortedYears[sortedYears.length - 1] || 2021);

    // Compute per-crime growth between firstYr and lastYr
    const growthStats = crimeCols.map(col => {
      const early = stateRows.filter(r => r.year === firstYr).reduce((s, r) => s + (r[col] || 0), 0);
      const late = stateRows.filter(r => r.year === lastYr).reduce((s, r) => s + (r[col] || 0), 0);
      const pct = early > 0 ? ((late - early) / early) * 100 : (late > 0 ? 100 : 0);
      return { col, early, late, pct };
    });

    // Card 2: Fastest Growing Crime & Card 4: Most Decreasing Crime
    const fastestValEl = document.querySelector('#kpiFastest .kpi-value');
    const fastestMetaEl = document.querySelector('#kpiFastest .kpi-meta');
    const decValEl = document.querySelector('#kpiDecreasing .kpi-value');
    const decMetaEl = document.querySelector('#kpiDecreasing .kpi-meta');

    if (fastestValEl && decValEl) {
      const sortedByGrowth = [...growthStats].sort((a, b) => b.pct - a.pct);
      const topGrow = sortedByGrowth[0];
      const lowGrow = sortedByGrowth[sortedByGrowth.length - 1];

      const shortName = (col) => (crimeLabels[col] || col).split('(')[0].trim();
      fastestValEl.textContent = shortName(topGrow.col);
      fastestMetaEl.innerHTML = `<strong>${topGrow.pct >= 0 ? '+' : ''}${topGrow.pct.toFixed(1)}%</strong> (${topGrow.early.toLocaleString()} &rarr; ${topGrow.late.toLocaleString()}) • ${firstYr}–${lastYr}`;

      decValEl.textContent = shortName(lowGrow.col);
      decMetaEl.innerHTML = `<strong>${lowGrow.pct >= 0 ? '+' : ''}${lowGrow.pct.toFixed(1)}%</strong> (${lowGrow.early.toLocaleString()} &rarr; ${lowGrow.late.toLocaleString()}) • ${firstYr}–${lastYr}`;
    }

    // Card 3: Most Prevalent Category in current filtered selection
    const prevValEl = document.querySelector('#kpiPrevalent .kpi-value');
    const prevMetaEl = document.querySelector('#kpiPrevalent .kpi-meta');
    if (prevValEl && filtered.length > 0) {
      const colSums = crimeCols.map(col => ({
        col,
        sum: filtered.reduce((s, r) => s + (r[col] || 0), 0)
      })).sort((a, b) => b.sum - a.sum);
      const grandTotal = colSums.reduce((s, c) => s + c.sum, 0);
      const topCat = colSums[0];
      const share = grandTotal > 0 ? ((topCat.sum / grandTotal) * 100).toFixed(1) : '0.0';
      prevValEl.textContent = (crimeLabels[topCat.col] || topCat.col).split('(')[0].trim();
      prevMetaEl.innerHTML = `<strong>${share}%</strong> of all crimes &bull; ${topCat.sum.toLocaleString()} cases`;
    }

    // Card 5: Year of Peak Surge & Card 6: Year of Largest Drop
    const surgeValEl = document.querySelector('#kpiSurge .kpi-value');
    const surgeMetaEl = document.querySelector('#kpiSurge .kpi-meta');
    const dropValEl = document.querySelector('#kpiLockdown .kpi-value');
    const dropMetaEl = document.querySelector('#kpiLockdown .kpi-meta');

    if (surgeValEl && dropValEl && sortedYears.length >= 2) {
      const yearlyTotals = sortedYears.map(yr => {
        const rows = stateRows.filter(r => r.year === yr);
        const val = currentFilters.crime === 'ALL'
          ? rows.reduce((s, r) => s + r.total, 0)
          : rows.reduce((s, r) => s + (r[currentFilters.crime] || 0), 0);
        return { yr, val };
      });

      let maxSurge = null;
      let maxDrop = null;
      for (let i = 1; i < yearlyTotals.length; i++) {
        const prev = yearlyTotals[i - 1].val;
        const curr = yearlyTotals[i].val;
        if (prev <= 0) continue;
        const pct = ((curr - prev) / prev) * 100;
        const diff = curr - prev;
        if (!maxSurge || pct > maxSurge.pct) maxSurge = { yr: yearlyTotals[i].yr, pct, diff };
        if (!maxDrop || pct < maxDrop.pct) maxDrop = { yr: yearlyTotals[i].yr, pct, diff };
      }

      if (maxSurge) {
        surgeValEl.textContent = `Year ${maxSurge.yr} (${maxSurge.pct >= 0 ? '+' : ''}${maxSurge.pct.toFixed(1)}%)`;
        surgeMetaEl.textContent = `${maxSurge.diff >= 0 ? '+' : ''}${maxSurge.diff.toLocaleString()} cases vs prior year`;
      }
      if (maxDrop && maxDrop.pct < 0) {
        dropValEl.textContent = `Year ${maxDrop.yr} (${maxDrop.pct.toFixed(2)}%)`;
        dropMetaEl.textContent = `${maxDrop.diff.toLocaleString()} cases vs prior year`;
      } else if (maxDrop) {
        dropValEl.textContent = `Year ${maxDrop.yr} (+${maxDrop.pct.toFixed(1)}%)`;
        dropMetaEl.textContent = `Lowest YoY change in selected range`;
      }
    }
  }

  // 2. Trend Chart (Line)
  function renderTrendChart() {
    const ctx = document.getElementById('trendChart').getContext('2d');
    
    // Group by year for selected state
    const yearlyMap = {};
    allYears.forEach(y => {
      yearlyMap[y] = { total: 0 };
      crimeCols.forEach(c => yearlyMap[y][c] = 0);
    });

    rawData.forEach(r => {
      if (currentFilters.state === 'ALL' || r.state === currentFilters.state) {
        if (yearlyMap[r.year]) {
          yearlyMap[r.year].total += r.total;
          crimeCols.forEach(c => yearlyMap[r.year][c] += r[c]);
        }
      }
    });

    const years = allYears;
    let datasets = [];

    if (currentFilters.crime === 'ALL') {
      // Show total and top categories
      datasets.push({
        label: 'Total Crimes',
        data: years.map(y => yearlyMap[y].total),
        borderColor: '#6366F1',
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.3,
        pointBackgroundColor: '#6366F1',
        pointRadius: 4,
        pointHoverRadius: 7
      });

      // Also add top 3 individual lines
      ['DV', 'AoW', 'K&A'].forEach(c => {
        datasets.push({
          label: crimeLabels[c] || c,
          data: years.map(y => yearlyMap[y][c]),
          borderColor: crimeColors[c],
          borderWidth: 2,
          fill: false,
          tension: 0.3,
          pointRadius: 3
        });
      });
    } else {
      const c = currentFilters.crime;
      datasets.push({
        label: crimeLabels[c] || c,
        data: years.map(y => yearlyMap[y][c]),
        borderColor: crimeColors[c] || '#6366F1',
        backgroundColor: (crimeColors[c] || '#6366F1') + '22',
        borderWidth: 3,
        fill: true,
        tension: 0.3,
        pointBackgroundColor: crimeColors[c] || '#6366F1',
        pointRadius: 5
      });
    }

    if (trendChartInstance) trendChartInstance.destroy();

    trendChartInstance = new Chart(ctx, {
      type: 'line',
      data: { labels: years, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: { color: '#94A3B8', font: { family: 'Inter', size: 11 } }
          },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.95)',
            titleColor: '#F8FAFC',
            bodyColor: '#CBD5E1',
            borderColor: 'rgba(255,255,255,0.1)',
            borderWidth: 1,
            padding: 12,
            callbacks: {
              label: (ctx) => `${ctx.dataset.label}: ${ctx.raw.toLocaleString()} cases`
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255,255,255,0.04)' },
            ticks: { color: '#64748B' }
          },
          y: {
            grid: { color: 'rgba(255,255,255,0.06)' },
            ticks: {
              color: '#64748B',
              callback: (val) => val.toLocaleString()
            }
          }
        }
      }
    });
  }

  // 3. Composition Doughnut Chart
  function renderCompositionChart(filtered) {
    const ctx = document.getElementById('compositionChart').getContext('2d');
    const totalsByCrime = {};
    crimeCols.forEach(c => totalsByCrime[c] = 0);

    filtered.forEach(r => {
      crimeCols.forEach(c => totalsByCrime[c] += r[c]);
    });

    const labels = crimeCols.map(c => crimeLabels[c] || c);
    const data = crimeCols.map(c => totalsByCrime[c]);
    const bgColors = crimeCols.map(c => crimeColors[c]);

    if (compositionChartInstance) compositionChartInstance.destroy();

    compositionChartInstance = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: bgColors,
          borderWidth: 2,
          borderColor: '#111827'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
            labels: {
              color: '#94A3B8',
              font: { family: 'Inter', size: 11 },
              boxWidth: 12
            }
          },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.95)',
            padding: 10,
            callbacks: {
              label: (ctx) => {
                const total = data.reduce((a,b) => a+b, 0);
                const pct = total ? ((ctx.raw / total) * 100).toFixed(1) : 0;
                return `${ctx.label}: ${ctx.raw.toLocaleString()} (${pct}%)`;
              }
            }
          }
        },
        cutout: '65%'
      }
    });
  }

  // 4. Hotspots Chart (Horizontal Bar)
  function renderHotspotsChart() {
    const ctx = document.getElementById('hotspotsChart').getContext('2d');
    
    // Aggregate by state for the selected year (or all years <= 2019 baseline)
    const stateSum = {};
    rawData.forEach(r => {
      if (currentFilters.year !== 'ALL' && r.year !== currentFilters.year) return;
      if (currentFilters.year === 'ALL' && r.year > 2019) return; // Clean baseline for cumulative
      if (!stateSum[r.state]) stateSum[r.state] = 0;
      
      if (currentFilters.crime === 'ALL') {
        stateSum[r.state] += r.total;
      } else {
        stateSum[r.state] += r[currentFilters.crime] || 0;
      }
    });

    const topStates = Object.entries(stateSum)
      .sort((a,b) => b[1] - a[1])
      .slice(0, 10);

    const labels = topStates.map(x => x[0]);
    const data = topStates.map(x => x[1]);

    if (hotspotsChartInstance) hotspotsChartInstance.destroy();

    hotspotsChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: currentFilters.crime === 'ALL' ? 'Total Reported Crimes' : crimeLabels[currentFilters.crime],
          data: data,
          backgroundColor: '#F43F5E',
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.95)',
            callbacks: {
              label: (ctx) => `${ctx.raw.toLocaleString()} reported cases`
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: {
              color: '#64748B',
              callback: (val) => val.toLocaleString()
            }
          },
          y: {
            grid: { display: false },
            ticks: { color: '#CBD5E1', font: { weight: 500 } }
          }
        }
      }
    });
  }

  // 5. Growth Rates Comparison Chart
  function renderGrowthChart() {
    const ctx = document.getElementById('growthChart').getContext('2d');

    // Calculate growth between 2001 and 2019
    const y01 = {};
    const y19 = {};
    crimeCols.forEach(c => { y01[c] = 0; y19[c] = 0; });

    rawData.forEach(r => {
      if (currentFilters.state === 'ALL' || r.state === currentFilters.state) {
        if (r.year === 2001) crimeCols.forEach(c => y01[c] += r[c]);
        if (r.year === 2019) crimeCols.forEach(c => y19[c] += r[c]);
      }
    });

    const compareCols = ['K&A', 'DV', 'AoW', 'Rape', 'DD', 'AoM'];
    const rates = compareCols.map(c => {
      const v01 = y01[c] || 1;
      const v19 = y19[c] || 0;
      return parseFloat((((v19 - v01) / v01) * 100).toFixed(1));
    });

    const labels = compareCols.map(c => crimeLabels[c] || c);
    const bgColors = rates.map(r => r >= 0 ? '#10B981' : '#EF4444');

    if (growthChartInstance) growthChartInstance.destroy();

    growthChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: '% Change (2001 to 2019)',
          data: rates,
          backgroundColor: bgColors,
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.95)',
            callbacks: {
              label: (ctx) => `${ctx.raw > 0 ? '+' : ''}${ctx.raw}% growth`
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: {
              color: '#64748B',
              callback: (val) => `${val}%`
            }
          },
          y: {
            grid: { display: false },
            ticks: { color: '#94A3B8', font: { size: 10 } }
          }
        }
      }
    });
  }

  // 6. Data Table Render
  function renderTable() {
    let filtered = getFilteredData();

    if (currentFilters.search) {
      filtered = filtered.filter(r => 
        r.state.toLowerCase().includes(currentFilters.search) ||
        String(r.year).includes(currentFilters.search)
      );
    }

    // Sort
    const col = sortConfig.column;
    const dir = sortConfig.direction === 'asc' ? 1 : -1;

    filtered.sort((a,b) => {
      if (typeof a[col] === 'string') {
        return a[col].localeCompare(b[col]) * dir;
      }
      return ((a[col] || 0) - (b[col] || 0)) * dir;
    });

    tableMetaInfo.textContent = `Displaying ${filtered.length} matching state/year records`;

    // Limit to top 150 rows for smooth scrolling
    const displayRows = filtered.slice(0, 150);

    tableBody.innerHTML = '';
    displayRows.forEach(r => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>${r.state}</strong></td>
        <td>${r.year}</td>
        <td>${r.Rape.toLocaleString()}</td>
        <td>${r['K&A'].toLocaleString()}</td>
        <td>${r.DD.toLocaleString()}</td>
        <td>${r.AoW.toLocaleString()}</td>
        <td>${r.AoM.toLocaleString()}</td>
        <td>${r.DV.toLocaleString()}</td>
        <td>${r.WT.toLocaleString()}</td>
        <td class="table-highlight">${r.total.toLocaleString()}</td>
      `;
      tableBody.appendChild(tr);
    });
  }

  // 7. CSV Export
  function exportFilteredCsv() {
    const filtered = getFilteredData();
    if (!filtered.length) return alert('No data to export.');

    const headers = ['State', 'Year', 'Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT', 'Total'];
    const csvRows = [headers.join(',')];

    filtered.forEach(r => {
      csvRows.push([
        `"${r.state}"`,
        r.year,
        r.Rape,
        r['K&A'],
        r.DD,
        r.AoW,
        r.AoM,
        r.DV,
        r.WT,
        r.total
      ].join(','));
    });

    const blob = new Blob([csvRows.join('\n')], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `safeshield_crime_data_filtered.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }

  // Initial Load
  updateDashboard();
});
