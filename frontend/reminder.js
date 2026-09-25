const API = "http://127.0.0.1:5000";

// ---------------- USER ----------------
const user = JSON.parse(localStorage.getItem("medicineUser"));
document.getElementById("userName").textContent = user?.name || "User";

// ---------------- ELEMENTS ----------------
const form = document.getElementById("medicineForm");
const tableBody = document.querySelector("#medicineTable tbody");
const reminderSound = document.getElementById("reminderSound");

let medicines = [];
let editId = null;

// ---------------- LOGOUT ----------------
document.getElementById("logoutBtn").onclick = () => {
  localStorage.clear();
  window.location.href = "/";
};

// ---------------- LOAD ----------------
function loadMedicines() {
  fetch(`${API}/medicines`)
    .then(res => res.json())
    .then(data => {
      medicines = data;
      renderTable();
    });
}
loadMedicines();

// ---------------- ADD / UPDATE ----------------
form.addEventListener("submit", (e) => {
  e.preventDefault();

  const payload = {
    name: medicineName.value.trim(),
    dosage: dosage.value.trim(),
    time: medicineTime.value
  };

  if (!payload.name || !payload.dosage || !payload.time) {
    alert("Fill all fields");
    return;
  }

  if (editId) {
    fetch(`${API}/update-medicine/${editId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(() => {
      editId = null;
      form.reset();
      loadMedicines();
    });
  } else {
    fetch(`${API}/add-medicine`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(() => {
      form.reset();
      loadMedicines();
    });
  }
});

// ---------------- TABLE ----------------
function renderTable() {
  tableBody.innerHTML = "";

  medicines.forEach(m => {
    const statusText = m.taken ? "Taken" : "Pending";
    const statusClass = m.taken ? "status-taken" : "status-pending";

    const takenBtn = m.taken
      ? ""
      : `<button class="action-btn" onclick="markTaken(${m.id})">✔ Taken</button>`;

    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${m.name}</td>
      <td>${m.dosage}</td>
      <td>${m.time}</td>
      <td class="${statusClass}">${statusText}</td>
      <td>
        ${takenBtn}
        <button class="edit-btn" onclick="editMedicine(${m.id})">✏️ Edit</button>
        <button class="delete-btn" onclick="deleteMedicine(${m.id})">🗑 Delete</button>
      </td>
    `;
    tableBody.appendChild(row);
  });

  updateSummary();
}

// ---------------- EDIT ----------------
function editMedicine(id) {
  const med = medicines.find(m => m.id === id);
  if (!med) return;

  medicineName.value = med.name;
  dosage.value = med.dosage;
  medicineTime.value = med.time;
  editId = id;
}

// ---------------- DELETE ----------------
function deleteMedicine(id) {
  if (!confirm("Delete this medicine?")) return;
  fetch(`${API}/delete-medicine/${id}`, { method: "DELETE" })
    .then(loadMedicines);
}

// ---------------- TAKEN ----------------
function markTaken(id) {
  fetch(`${API}/take-medicine/${id}`, {
    method: "PUT"
  }).then(loadMedicines);
}

// ---------------- SUMMARY ----------------
function updateSummary() {
  const total = medicines.length;
  const taken = medicines.filter(m => m.taken).length;
  const pending = total - taken;

  totalMeds.textContent = total;
  takenMeds.textContent = taken;
  pendingMeds.textContent = pending;
}

// ---------------- REMINDER ----------------
setInterval(() => {
  const now = new Date();
  const currentTime =
    String(now.getHours()).padStart(2, "0") + ":" +
    String(now.getMinutes()).padStart(2, "0");

  medicines.forEach(m => {
    if (m.time === currentTime && !m.taken) {
      reminderSound.play();
      alert(`💊 Time to take medicine: ${m.name} (${m.dosage})`);
    }
  });
}, 60000);
