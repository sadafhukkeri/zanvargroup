document.getElementById('tempForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    await fetch('/submit', {
        method: 'POST',
        body: formData
    });
    this.reset();
    fetchData();
});

document.getElementById('filterBtn').addEventListener('click', fetchData);

async function fetchData() {
    const start = document.getElementById('start').value;
    const end = document.getElementById('end').value;
    const min_temp = document.getElementById('min_temp').value;
    const max_temp = document.getElementById('max_temp').value;

    const params = new URLSearchParams();

    if (start) params.append('start', start);
    if (end) params.append('end', end);
    if (min_temp) params.append('min_temp', min_temp);
    if (max_temp) params.append('max_temp', max_temp);

    const res = await fetch('/fetch?' + params.toString());
    const data = await res.json();

    const tableBody = document.getElementById('dataTable');
    tableBody.innerHTML = '';
    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${row.temperature}</td><td>${row.timestamp}</td>`;
        tableBody.appendChild(tr);
    });
}



// Initial fetch
fetchData();
