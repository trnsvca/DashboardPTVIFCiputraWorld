const SHEET_ID = "1i_6rgY7qA5Qovq2_RHFX369y4KvC4O7EcFagofBXgmM";
const SHEET_NAME = "Sheet1";

const URL = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?sheet=${SHEET_NAME}`;

let headers = [];
let allData = [];
let chart;

async function fetchData() {
  const res = await fetch(URL);
  const text = await res.text();

  const json = JSON.parse(text.substr(47).slice(0, -2));

  headers = json.table.cols.map(col => col.label);
  allData = json.table.rows.map(row =>
    row.c.map(cell => (cell ? cell.v : ""))
  );

  initFilter();
  updateDashboard(allData);
}

function initFilter() {
  const select = document.getElementById("filterColumn");
  headers.forEach((h, i) => {
    const option = document.createElement("option");
    option.value = i;
    option.textContent = h;
    select.appendChild(option);
  });
}

function updateDashboard(data) {
  renderTable(headers, data);
  updateKPI(data);
  renderChart(data);
}

function renderTable(headers, data) {
  const thead = document.querySelector("#table thead");
  const tbody = document.querySelector("#table tbody");

  thead.innerHTML = "";
  tbody.innerHTML = "";

  const trHead = document.createElement("tr");
  headers.forEach(h => {
    const th = document.createElement("th");
    th.textContent = h;
    trHead.appendChild(th);
  });
  thead.appendChild(trHead);

  data.forEach(row => {
    const tr = document.createElement("tr");
    row.forEach(cell => {
      const td = document.createElement("td");
      td.textContent = cell;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
}

function updateKPI(data) {
  document.getElementById("totalData").textContent = allData.length;
  document.getElementById("filteredData").textContent = data.length;
}

function renderChart(data) {
  const ctx = document.getElementById("chart");

  const colIndex = document.getElementById("filterColumn").value;

  const counts = {};

  data.forEach(row => {
    const key = row[colIndex];
    counts[key] = (counts[key] || 0) + 1;
  });

  const labels = Object.keys(counts);
  const values = Object.values(counts);

  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Jumlah Data",
        data: values
      }]
    }
  });
}

document.getElementById("search").addEventListener("input", applyFilter);
document.getElementById("filterColumn").addEventListener("change", applyFilter);

function applyFilter() {
  const keyword = document.getElementById("search").value.toLowerCase();
  const colIndex = document.getElementById("filterColumn").value;

  const filtered = allData.filter(row => {
    return String(row[colIndex]).toLowerCase().includes(keyword);
  });

  updateDashboard(filtered);
}

fetchData();
